#!/usr/bin/env python3
"""Install committed shared skills offline; never fetch, stage, commit, or push."""

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import tarfile
import tempfile

NAMES = ("go", "simplify", "triage-and-go")
SOURCE = "adam-messinger/adam-messinger"
CONSUMERS = {"geddy", "cashflow"}
MANIFEST = ".agents/shared-skills.json"


def git(root, *args):
    return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE)


def github_repo(remote):
    match = re.fullmatch(r"(?:git@github\.com:|https://github\.com/|ssh://git@github\.com/)([^/]+/[^/]+?)(?:\.git)?/?", remote)
    if not match:
        raise ValueError("Expected an explicit github.com repository remote")
    return match.group(1)


def identity(root):
    actual = Path(git(root, "rev-parse", "--show-toplevel").decode().strip()).resolve()
    if actual != root.resolve():
        raise ValueError(f"Not a repository root: {root}")
    repo = github_repo(git(root, "remote", "get-url", "origin").decode().strip())
    push_repo = github_repo(git(root, "remote", "get-url", "--push", "origin").decode().strip())
    if push_repo != repo:
        raise ValueError("Fetch and push remotes must identify the same repository")
    return repo


def digest(data):
    return hashlib.sha256(data).hexdigest()


def snapshot(source, revision):
    if identity(source) != SOURCE:
        raise ValueError("Source origin must be adam-messinger/adam-messinger")
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("Pass a full immutable 40-character commit SHA, not a branch or tag")
    resolved = git(source, "rev-parse", f"{revision}^{{commit}}").decode().strip()
    if resolved != revision:
        raise ValueError("Revision did not resolve to the requested commit")
    archive = git(source, "archive", revision, "--", *[f"skills/{n}" for n in NAMES])
    files = {}
    with tarfile.open(fileobj=io.BytesIO(archive)) as tree:
        for member in tree.getmembers():
            if member.isdir():
                continue
            path = Path(member.name)
            if not member.isfile() or path.is_absolute() or ".." in path.parts:
                raise ValueError("Skill snapshot must contain only regular files")
            if len(path.parts) < 3 or path.parts[0] != "skills" or path.parts[1] not in NAMES:
                raise ValueError("Unexpected archive path")
            dest = Path(".agents") / path
            files[dest.as_posix()] = (tree.extractfile(member).read(), 0o755 if member.mode & 0o111 else 0o644)
    for name in NAMES:
        entry = f".agents/skills/{name}/SKILL.md"
        if entry not in files:
            raise ValueError(f"Missing {name}/SKILL.md in source revision")
    entries = git(source, "ls-tree", "-rz", revision, "--",
                  *[f"skills/{n}" for n in NAMES]).split(b"\0")
    tracked = {}
    for entry in entries:
        if entry:
            metadata, path = entry.split(b"\t", 1)
            mode, kind, blob = metadata.split()
            if mode not in (b"100644", b"100755") or kind != b"blob":
                raise ValueError("Committed skills must be regular files")
            tracked[".agents/" + path.decode()] = (mode, blob.decode())
    if set(files) != set(tracked):
        raise ValueError("Archive omitted tracked skill files; check export-ignore attributes")
    for path, (data, _) in files.items():
        mode, blob = tracked[path]
        original = git(source, "cat-file", "blob", blob)
        if data != original:
            raise ValueError("Archive changed committed skill bytes; check export-subst attributes")
        files[path] = (data, 0o755 if mode == b"100755" else 0o644)
    return files


def safe_parents(root):
    for rel in (".agents", ".agents/skills", ".claude", ".claude/skills"):
        path = root / rel
        if path.is_symlink() or (path.exists() and not path.is_dir()):
            raise ValueError(f"Refusing unsafe destination parent: {path}")
    if (root / MANIFEST).is_symlink():
        raise ValueError(f"Refusing linked manifest: {root / MANIFEST}")


def installed_files(root):
    files = {}
    for name in NAMES:
        folder = root / ".agents/skills" / name
        if folder.is_symlink() or (folder.exists() and not folder.is_dir()):
            raise ValueError(f"Expected real skill directory: {folder}")
        if folder.exists():
            for path in folder.rglob("*"):
                if path.is_symlink():
                    raise ValueError(f"Expected real skill files: {path}")
                if path.is_file():
                    files[path.relative_to(root).as_posix()] = digest(path.read_bytes())
    return files


def expected_manifest(revision, files):
    return {
        "schema": 1,
        "source": "https://github.com/" + SOURCE,
        "revision": revision,
        "files": {p: digest(data) for p, (data, _) in sorted(files.items())},
        "modes": {p: mode for p, (_, mode) in sorted(files.items())},
        "claude_links": {n: f"../../.agents/skills/{n}" for n in NAMES},
    }


def preflight(root, manifest, check):
    repo = identity(root)
    if repo not in {f"adam-messinger/{n}" for n in CONSUMERS}:
        raise ValueError(f"Unexpected consumer origin: {repo}")
    safe_parents(root)
    managed = [MANIFEST] + [f"{base}/{n}" for base in (".agents/skills", ".claude/skills") for n in NAMES]
    if not check and git(root, "diff", "--cached", "--name-only", "--", *managed).strip():
        raise ValueError(f"Managed skill paths have staged changes: {root}; preserve staging before updating")
    current = installed_files(root)
    prior_path = root / MANIFEST
    prior = json.loads(prior_path.read_text()) if prior_path.exists() else None
    if prior_path.exists() and not isinstance(prior, dict):
        raise ValueError(f"Expected provenance object: {prior_path}")
    modes = {p: stat.S_IMODE((root / p).stat().st_mode) for p in current}
    if not check and prior != manifest and git(root, "diff", "--name-only", "--", MANIFEST).strip():
        raise ValueError(f"Managed manifest has local changes: {root}; preserve them before updating")
    if check:
        if prior != manifest or current != manifest["files"] or modes != manifest["modes"]:
            raise ValueError(f"Installed content/provenance mismatch: {root}")
    elif prior:
        if (set(prior) != set(manifest) or prior.get("schema") != 1
                or prior.get("source") != manifest["source"]
                or not re.fullmatch(r"[0-9a-f]{40}", str(prior.get("revision", "")))
                or prior.get("claude_links") != manifest["claude_links"]
                or current != prior.get("files") or modes != prior.get("modes")):
            raise ValueError(f"Managed skills have local changes: {root}; preserve them before updating")
    elif current and (current != manifest["files"] or modes != manifest["modes"]):
        raise ValueError(f"Existing unmanaged skills: {root}; back them up and remove only these names first")
    for name, target in manifest["claude_links"].items():
        path = root / ".claude/skills" / name
        if path.is_symlink():
            if os.readlink(path) != target:
                raise ValueError(f"Unexpected Claude link: {path}; preserve it before replacing")
        elif path.exists() or check:
            raise ValueError(f"Expected relative Claude link: {path}; preserve any legacy directory first")
    return repo


def install(root, files, manifest):
    # Preflight of every consumer completed before the first write. Only these
    # named skill directories and the dedicated manifest are managed here.
    for name in NAMES:
        folder = root / ".agents/skills" / name
        if folder.exists():
            shutil.rmtree(folder)
    for rel, (data, mode) in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        path.chmod(mode)
    for name, target in manifest["claude_links"].items():
        path = root / ".claude/skills" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.is_symlink():
            path.symlink_to(target, target_is_directory=True)
    (root / MANIFEST).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def update_all(roots, files, manifest):
    """Restore managed paths on an I/O failure; unrelated files are never touched."""
    managed = [MANIFEST] + [f"{base}/{n}" for base in (".agents/skills", ".claude/skills") for n in NAMES]
    backups = Path(tempfile.mkdtemp(prefix="shared-skills-rollback-"))
    try:
        for index, root in enumerate(roots):
            for rel in managed:
                path = root / rel
                backup = backups / str(index) / rel
                backup.parent.mkdir(parents=True, exist_ok=True)
                if path.is_symlink():
                    backup.symlink_to(os.readlink(path))
                elif path.is_dir():
                    shutil.copytree(path, backup)
                elif path.exists():
                    shutil.copy2(path, backup)
    except Exception:
        shutil.rmtree(backups)
        raise
    try:
        for root in roots:
            install(root, files, manifest)
            preflight(root, manifest, True)
    except Exception as update_error:
        try:
            for index, root in enumerate(roots):
                for rel in managed:
                    path = root / rel
                    backup = backups / str(index) / rel
                    if path.is_symlink() or path.is_file():
                        path.unlink()
                    elif path.exists():
                        shutil.rmtree(path)
                    if backup.is_symlink():
                        path.symlink_to(os.readlink(backup))
                    elif backup.is_dir():
                        shutil.copytree(backup, path)
                    elif backup.exists():
                        shutil.copy2(backup, path)
        except Exception as restore_error:
            raise RuntimeError(f"Update failed: {update_error}. Rollback failed: {restore_error}. "
                               f"Recoverable backups retained at {backups}") from restore_error
        shutil.rmtree(backups)
        raise
    shutil.rmtree(backups)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--revision", required=True)
    parser.add_argument("--repos", nargs=2, type=Path, required=True, metavar="REPO")
    parser.add_argument("--check", action="store_true", help="Verify only; do not write")
    args = parser.parse_args()
    roots = [p.resolve() for p in args.repos]
    files = snapshot(args.source.resolve(), args.revision)
    manifest = expected_manifest(args.revision, files)
    repos = [preflight(root, manifest, args.check) for root in roots]
    if set(repos) != {f"adam-messinger/{n}" for n in CONSUMERS}:
        raise ValueError("Provide exactly one Geddy and one Cashflow checkout")
    if not args.check:
        update_all(roots, files, manifest)
    for root in roots:
        print(f"Verified {root}: {args.revision} ({len(files)} files, 3 relative links)")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, RuntimeError, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error)) from error
