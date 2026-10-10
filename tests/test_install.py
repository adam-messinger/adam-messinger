"""Offline integration coverage for the shared-skill updater.

Every repository, home directory, and failure artifact belongs to a temporary
fixture. These tests never invoke a skill or contact a GitHub repository.
"""

import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/update-shared-skills.py"
NAMES = ("go", "simplify", "triage-and-go")
MANIFEST = ".agents/shared-skills.json"


def tree_state(root):
    """Capture user-visible content, links, and modes, excluding Git internals."""
    result = {}
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if ".git" in relative.parts:
            continue
        mode = stat.S_IMODE(path.lstat().st_mode)
        if path.is_symlink():
            result[relative.as_posix()] = ("link", os.readlink(path))
        elif path.is_file():
            result[relative.as_posix()] = ("file", mode, path.read_bytes())
        elif path.is_dir():
            result[relative.as_posix()] = ("directory", mode)
    return result


class InstallIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="shared-skills-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.home = self.root / "empty-home"
        self.home.mkdir()
        self.env = dict(
            os.environ,
            HOME=str(self.home),
            XDG_CONFIG_HOME=str(self.home / ".config"),
            XDG_STATE_HOME=str(self.home / ".state"),
            GIT_CONFIG_NOSYSTEM="1",
            GIT_CONFIG_GLOBAL=os.devnull,
            GIT_TERMINAL_PROMPT="0",
        )
        self.source = self.make_repo("canonical", "adam-messinger")
        self.geddy = self.make_repo("geddy", "geddy")
        self.cashflow = self.make_repo("cashflow", "cashflow")
        self.repos = (self.geddy, self.cashflow)
        for name in NAMES:
            folder = self.source / "skills" / name
            (folder / "references").mkdir(parents=True)
            (folder / "SKILL.md").write_text(
                f"---\nname: {name}\ndescription: Inert {name} integration fixture.\n---\n"
                "\nVersion one. Do not execute any task.\n"
            )
            (folder / "LICENSE").write_text("Fixture license and attribution.\n")
            (folder / "references/context.md").write_text("Useful fixture reference.\n")
        runner = self.source / "skills/go/fixture.sh"
        runner.write_text("#!/bin/sh\nexit 0\n")
        runner.chmod(0o755)
        self.commit(self.source, "Add portable fixtures")
        self.revision = self.git(self.source, "rev-parse", "HEAD").stdout.strip()

    def git(self, root, *args, check=True):
        return subprocess.run(
            ["git", "-C", str(root), *args], env=self.env, text=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check,
        )

    def make_repo(self, directory, remote_name):
        root = self.root / directory
        root.mkdir()
        self.git(root, "init", "--quiet")
        self.git(root, "config", "user.name", "Shared Skills Test")
        self.git(root, "config", "user.email", "shared-skills@example.invalid")
        self.git(root, "config", "core.symlinks", "true")
        self.git(root, "config", "core.autocrlf", "false")
        self.git(root, "remote", "add", "origin",
                 f"https://github.com/adam-messinger/{remote_name}.git")
        (root / "README.md").write_text("Existing repository purpose.\n")
        self.commit(root, "Initialize fixture")
        return root

    def commit(self, root, message):
        self.git(root, "add", "--all")
        self.git(root, "commit", "--quiet", "-m", message)

    def run_update(self, *, revision=None, repos=None, check=False, expect_success=True):
        args = [sys.executable, str(SCRIPT), "--source", str(self.source),
                "--revision", revision or self.revision, "--repos",
                *(str(p) for p in (repos or self.repos))]
        if check:
            args.append("--check")
        result = subprocess.run(args, env=self.env, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, timeout=20)
        output = result.stdout + result.stderr
        if expect_success:
            self.assertEqual(result.returncode, 0, output)
        else:
            self.assertNotEqual(result.returncode, 0, output)
        return result

    def install_and_commit(self):
        self.run_update()
        for root in self.repos:
            self.commit(root, "Install shared fixtures")

    def next_revision(self):
        (self.source / "skills/go/SKILL.md").write_text(
            (self.source / "skills/go/SKILL.md").read_text().replace("Version one", "Version two")
        )
        (self.source / "skills/simplify/references/new.md").write_text("New committed evidence.\n")
        (self.source / "skills/triage-and-go/references/context.md").unlink()
        self.commit(self.source, "Update fixtures")
        return self.git(self.source, "rev-parse", "HEAD").stdout.strip()

    def assert_refusal_preserves_both(self, **kwargs):
        before = [tree_state(root) for root in self.repos]
        self.run_update(expect_success=False, **kwargs)
        self.assertEqual([tree_state(root) for root in self.repos], before)

    def assert_install_matches(self, root, revision):
        manifest = json.loads((root / MANIFEST).read_text())
        self.assertEqual(manifest["revision"], revision)
        self.assertEqual(manifest["source"], "https://github.com/adam-messinger/adam-messinger")
        tracked = self.git(self.source, "ls-tree", "-r", "--name-only", revision,
                           "--", "skills").stdout.splitlines()
        self.assertEqual(set(manifest["files"]), {".agents/" + name for name in tracked})
        for relative in tracked:
            content = subprocess.check_output(
                ["git", "-C", str(self.source), "show", f"{revision}:{relative}"],
                env=self.env,
            )
            installed = root / ".agents" / relative
            self.assertFalse(installed.is_symlink())
            self.assertEqual(installed.read_bytes(), content)
            self.assertEqual(manifest["files"][".agents/" + relative],
                             hashlib.sha256(content).hexdigest())
        self.assertTrue((root / ".agents/skills/go/fixture.sh").stat().st_mode & stat.S_IXUSR)
        for name in NAMES:
            link = root / ".claude/skills" / name
            self.assertTrue(link.is_symlink())
            self.assertEqual(os.readlink(link), f"../../.agents/skills/{name}")
            self.assertEqual(link.resolve(), (root / ".agents/skills" / name).resolve())

    def test_fresh_clones_keep_real_files_and_git_symlinks_with_empty_home(self):
        self.install_and_commit()
        clones = []
        for original in self.repos:
            clone = self.root / (original.name + "-fresh")
            subprocess.run(["git", "clone", "--quiet", "--no-hardlinks", str(original), str(clone)],
                           env=self.env, check=True, capture_output=True)
            self.git(clone, "remote", "set-url", "origin",
                     f"git@github.com:adam-messinger/{original.name}.git")
            clones.append(clone)
            self.assert_install_matches(clone, self.revision)
            for name in NAMES:
                entry = self.git(clone, "ls-files", "--stage", ".claude/skills/" + name).stdout
                self.assertTrue(entry.startswith("120000 "), entry)
        before = [tree_state(root) for root in clones]
        self.run_update(repos=clones, check=True)
        self.assertEqual([tree_state(root) for root in clones], before)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_immutable_commit_ignores_source_worktree_edits(self):
        source_skill = self.source / "skills/go/SKILL.md"
        source_skill.write_text("Uncommitted accidental source edit.\n")
        (self.source / "skills/go/local-only.md").write_text("Never distribute this file.\n")
        self.run_update()
        for root in self.repos:
            self.assert_install_matches(root, self.revision)
            self.assertFalse((root / ".agents/skills/go/local-only.md").exists())

    def test_repeat_install_is_idempotent(self):
        self.run_update()
        before = [tree_state(root) for root in self.repos]
        status = [self.git(root, "status", "--porcelain=v1").stdout for root in self.repos]
        self.run_update()
        self.assertEqual([tree_state(root) for root in self.repos], before)
        self.assertEqual([self.git(root, "status", "--porcelain=v1").stdout for root in self.repos], status)

    def test_new_revision_updates_both_and_removes_obsolete_managed_files(self):
        self.install_and_commit()
        next_revision = self.next_revision()
        self.run_update(revision=next_revision)
        for root in self.repos:
            self.assert_install_matches(root, next_revision)
            self.assertFalse((root / ".agents/skills/triage-and-go/references/context.md").exists())
        self.assertEqual((self.geddy / MANIFEST).read_bytes(), (self.cashflow / MANIFEST).read_bytes())

    def test_unmanaged_named_skill_in_second_repo_blocks_all_writes(self):
        path = self.cashflow / ".agents/skills/go/SKILL.md"
        path.parent.mkdir(parents=True)
        path.write_text("An existing independently authored skill.\n")
        self.assert_refusal_preserves_both()

    def test_dirty_managed_skill_in_second_repo_blocks_all_updates(self):
        self.install_and_commit()
        next_revision = self.next_revision()
        path = self.cashflow / ".agents/skills/go/SKILL.md"
        path.write_text(path.read_text() + "Local unfinished work.\n")
        self.assert_refusal_preserves_both(revision=next_revision)

    def test_staged_change_is_preserved_even_when_worktree_matches_manifest(self):
        self.install_and_commit()
        next_revision = self.next_revision()
        relative = ".agents/skills/go/SKILL.md"
        path = self.cashflow / relative
        original = path.read_bytes()
        path.write_text("User's staged replacement.\n")
        self.git(self.cashflow, "add", relative)
        path.write_bytes(original)
        staged_before = self.git(self.cashflow, "diff", "--cached", "--binary").stdout
        self.assert_refusal_preserves_both(revision=next_revision)
        self.assertEqual(self.git(self.cashflow, "diff", "--cached", "--binary").stdout, staged_before)

    def test_consumer_fetch_remote_mismatch_preserves_both(self):
        self.git(self.cashflow, "remote", "set-url", "origin", "https://github.com/someone/cashflow.git")
        self.assert_refusal_preserves_both()

    def test_consumer_push_remote_mismatch_preserves_both(self):
        self.git(self.cashflow, "remote", "set-url", "--push", "origin",
                 "https://github.com/someone/cashflow.git")
        self.assert_refusal_preserves_both()

    def test_source_remote_mismatch_preserves_both(self):
        self.git(self.source, "remote", "set-url", "origin", "https://github.com/someone/adam-messinger.git")
        self.assert_refusal_preserves_both()

    def test_requires_one_checkout_of_each_consumer(self):
        self.assert_refusal_preserves_both(repos=(self.geddy, self.geddy))

    def test_branch_or_short_commit_cannot_select_mutable_source(self):
        for revision in ("HEAD", self.revision[:12]):
            with self.subTest(revision=revision):
                self.assert_refusal_preserves_both(revision=revision)

    def test_destination_parent_symlinks_do_not_write_external_targets(self):
        for relative in (".agents", ".agents/skills", ".claude", ".claude/skills"):
            with self.subTest(parent=relative):
                external = self.root / "external"
                external.mkdir()
                (external / "private.txt").write_text("Private unrelated state.\n")
                target = self.cashflow / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.symlink_to(external, target_is_directory=True)
                external_before = tree_state(external)
                self.assert_refusal_preserves_both()
                self.assertEqual(tree_state(external), external_before)
                target.unlink()
                shutil.rmtree(external)

    def test_destination_parent_file_conflicts_preserve_all_content(self):
        for relative in (".agents", ".agents/skills", ".claude", ".claude/skills"):
            with self.subTest(parent=relative):
                target = self.cashflow / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("A user file at a destination parent.\n")
                self.assert_refusal_preserves_both()
                target.unlink()

    def test_canonical_skill_directory_link_is_rejected(self):
        target = self.cashflow / ".agents/skills/go"
        target.parent.mkdir(parents=True)
        external = self.root / "external-skill"
        external.mkdir()
        (external / "SKILL.md").write_text("Existing linked private skill.\n")
        target.symlink_to(external, target_is_directory=True)
        self.assert_refusal_preserves_both()

    def test_canonical_skill_file_link_is_rejected(self):
        self.install_and_commit()
        target = self.cashflow / ".agents/skills/go/LICENSE"
        target.unlink()
        target.symlink_to(self.source / "skills/go/LICENSE")
        self.assert_refusal_preserves_both(revision=self.next_revision())

    def test_claude_legacy_directory_and_wrong_link_are_not_overwritten(self):
        target = self.cashflow / ".claude/skills/go"
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("Old skill with distinct instructions.\n")
        self.assert_refusal_preserves_both()
        shutil.rmtree(target)
        target.symlink_to("../../outside")
        self.assert_refusal_preserves_both()

    def test_manifest_symlink_is_not_followed(self):
        target = self.cashflow / MANIFEST
        target.parent.mkdir(parents=True)
        external = self.root / "external-manifest.json"
        external.write_text("{}\n")
        target.symlink_to(external)
        self.assert_refusal_preserves_both()
        self.assertEqual(external.read_text(), "{}\n")

    def test_unrelated_skills_settings_instructions_and_staging_survive_update(self):
        expected = {}
        for root in self.repos:
            entries = {
                ".agents/skills/unrelated/SKILL.md": "Unrelated personal team workflow.\n",
                ".claude/settings.local.json": '{"private": true}\n',
                ".codex/config.toml": 'model = "existing-model"\n',
                "AGENTS.md": "Existing repository instructions.\n",
                ".gitignore": ".env\n.worktrees/\n",
                ".env": "PRIVATE_FIXTURE=do-not-copy\n",
                "README.md": "User's staged unrelated edit.\n",
            }
            for relative, content in entries.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
                expected[(root.name, relative)] = path.read_bytes()
            self.git(root, "add", "README.md")
        staged_before = [self.git(root, "diff", "--cached", "--binary").stdout for root in self.repos]
        self.run_update()
        self.run_update(revision=self.next_revision())
        for root in self.repos:
            for (repo, relative), content in expected.items():
                if repo == root.name:
                    self.assertEqual((root / relative).read_bytes(), content)
        self.assertEqual([self.git(root, "diff", "--cached", "--binary").stdout for root in self.repos], staged_before)

    def test_check_detects_content_change_without_repairing_it(self):
        self.install_and_commit()
        path = self.cashflow / ".agents/skills/go/SKILL.md"
        path.write_text(path.read_text() + "Changed after installation.\n")
        self.assert_refusal_preserves_both(check=True)

    def test_check_detects_wrong_link_without_repairing_it(self):
        self.install_and_commit()
        path = self.cashflow / ".claude/skills/go"
        path.unlink()
        path.symlink_to("../../.agents/skills/simplify")
        self.assert_refusal_preserves_both(check=True)

    def test_check_detects_extra_managed_file_without_removing_it(self):
        self.install_and_commit()
        (self.cashflow / ".agents/skills/go/private.md").write_text("Unfinished local addition.\n")
        self.assert_refusal_preserves_both(check=True)

    def test_check_detects_changed_executable_flags_without_repairing_them(self):
        self.install_and_commit()
        for relative, changed_mode in ((".agents/skills/go/fixture.sh", 0o644),
                                       (".agents/skills/go/LICENSE", 0o755)):
            with self.subTest(path=relative):
                path = self.cashflow / relative
                original_mode = stat.S_IMODE(path.stat().st_mode)
                path.chmod(changed_mode)
                self.assert_refusal_preserves_both(check=True)
                path.chmod(original_mode)

    def test_local_executable_flag_change_blocks_update_before_other_repo_write(self):
        self.install_and_commit()
        next_revision = self.next_revision()
        (self.cashflow / ".agents/skills/go/fixture.sh").chmod(0o644)
        self.assert_refusal_preserves_both(revision=next_revision)

    def test_check_detects_tampered_manifest(self):
        self.install_and_commit()
        path = self.cashflow / MANIFEST
        manifest = json.loads(path.read_text())
        manifest["revision"] = "0" * 40
        path.write_text(json.dumps(manifest))
        self.assert_refusal_preserves_both(check=True)

    def test_source_symlinks_are_not_distributed(self):
        (self.source / "skills/go/linked-license").symlink_to("LICENSE")
        self.commit(self.source, "Add unsupported source link")
        self.assert_refusal_preserves_both(revision=self.git(self.source, "rev-parse", "HEAD").stdout.strip())

    def test_export_ignore_cannot_silently_drop_required_attribution(self):
        (self.source / ".gitattributes").write_text("skills/simplify/LICENSE export-ignore\n")
        self.commit(self.source, "Add archive omission")
        self.assert_refusal_preserves_both(revision=self.git(self.source, "rev-parse", "HEAD").stdout.strip())

    def test_archive_substitution_cannot_change_committed_skill_bytes(self):
        relative = "skills/go/SKILL.md"
        path = self.source / relative
        path.write_text(path.read_text() + "\nCommitted marker: $Format:%H$\n")
        self.commit(self.source, "Add literal format marker")
        for location in (".gitattributes", ".git/info/attributes"):
            with self.subTest(attributes=location):
                attributes = self.source / location
                attributes.write_text(f"{relative} export-subst\n")
                if location == ".gitattributes":
                    self.commit(self.source, "Enable committed archive substitution")
                revision = self.git(self.source, "rev-parse", "HEAD").stdout.strip()
                blob = subprocess.check_output(
                    ["git", "-C", str(self.source), "show", f"{revision}:{relative}"], env=self.env
                )
                archive = subprocess.check_output(
                    ["git", "-C", str(self.source), "archive", revision, "--", relative], env=self.env
                )
                with tarfile.open(fileobj=io.BytesIO(archive)) as tree:
                    substituted = tree.extractfile(relative).read()
                self.assertNotEqual(substituted, blob, "Fixture must exercise a real Git archive transform")
                self.assertIn(revision.encode(), substituted)
                self.assert_refusal_preserves_both(revision=revision)
                attributes.unlink()
                if location == ".gitattributes":
                    self.commit(self.source, "Remove committed archive substitution")

    def test_archive_umask_cannot_strip_committed_executable_flag(self):
        self.git(self.source, "config", "tar.umask", "0777")
        self.run_update()
        for root in self.repos:
            self.assert_install_matches(root, self.revision)
            manifest = json.loads((root / MANIFEST).read_text())
            self.assertEqual(manifest["modes"][".agents/skills/go/fixture.sh"], 0o755)
            self.assertEqual(manifest["modes"][".agents/skills/go/LICENSE"], 0o644)
        self.run_update(check=True)

    def test_unstaged_manifest_edits_survive_refused_update(self):
        self.install_and_commit()
        next_revision = self.next_revision()
        path = self.cashflow / MANIFEST
        original = path.read_bytes()
        for key, value in (("revision", "f" * 40), ("user_note", "Preserve this local provenance investigation")):
            with self.subTest(edited_field=key):
                manifest = json.loads(original)
                manifest[key] = value
                path.write_text(json.dumps(manifest, indent=2) + "\n")
                diff_before = self.git(self.cashflow, "diff", "--binary", "--", MANIFEST).stdout
                self.assertTrue(diff_before)
                self.assert_refusal_preserves_both(revision=next_revision)
                self.assertEqual(self.git(self.cashflow, "diff", "--binary", "--", MANIFEST).stdout,
                                 diff_before)
                path.write_bytes(original)

    def test_second_consumer_write_failure_rolls_back_both_installations(self):
        self.install_and_commit()
        next_revision = self.next_revision()
        before = [tree_state(root) for root in self.repos]
        status_before = [self.git(root, "status", "--porcelain=v1").stdout for root in self.repos]
        spec = importlib.util.spec_from_file_location("shared_skills_updater_test", SCRIPT)
        updater = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(updater)
        with mock.patch.dict(os.environ, self.env, clear=True):
            files = updater.snapshot(self.source, next_revision)
            manifest = updater.expected_manifest(next_revision, files)
            original_install = updater.install

            def install_then_fail(root, files, manifest):
                original_install(root, files, manifest)
                if root == self.cashflow:
                    raise OSError("Injected second-consumer I/O failure")

            with mock.patch.object(updater, "install", side_effect=install_then_fail):
                with self.assertRaises(OSError):
                    updater.update_all(list(self.repos), files, manifest)
        self.assertEqual([tree_state(root) for root in self.repos], before)
        self.assertEqual([self.git(root, "status", "--porcelain=v1").stdout for root in self.repos], status_before)
        self.run_update(check=True)

    def test_persistent_restore_failure_keeps_recoverable_backups_and_reports_path(self):
        self.install_and_commit()
        next_revision = self.next_revision()
        originals = [(root / MANIFEST).read_bytes() for root in self.repos]
        original_skills = [(root / ".agents/skills/go/SKILL.md").read_bytes() for root in self.repos]
        retained = self.root / "retained-recovery-backups"
        retained.mkdir()
        self.addCleanup(shutil.rmtree, retained, ignore_errors=True)
        spec = importlib.util.spec_from_file_location("shared_skills_restore_failure_test", SCRIPT)
        updater = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(updater)
        with mock.patch.dict(os.environ, self.env, clear=True):
            files = updater.snapshot(self.source, next_revision)
            manifest = updater.expected_manifest(next_revision, files)
            original_install = updater.install
            original_copytree = updater.shutil.copytree
            restoring = False

            def install_then_fail(root, files, manifest):
                nonlocal restoring
                original_install(root, files, manifest)
                if root == self.cashflow:
                    restoring = True
                    raise OSError("Injected second-consumer write failure")

            def copytree_with_restore_failure(source, destination, *args, **kwargs):
                if restoring:
                    raise OSError("Injected persistent restore I/O failure")
                return original_copytree(source, destination, *args, **kwargs)

            with mock.patch.object(updater.tempfile, "mkdtemp", return_value=str(retained)), \
                    mock.patch.object(updater, "install", side_effect=install_then_fail), \
                    mock.patch.object(updater.shutil, "copytree", side_effect=copytree_with_restore_failure):
                with self.assertRaises(RuntimeError) as raised:
                    updater.update_all(list(self.repos), files, manifest)
        self.assertIn(str(retained), str(raised.exception))
        self.assertIsInstance(raised.exception.__cause__, OSError)
        self.assertTrue(retained.is_dir(), "The only recoverable originals must remain on disk")
        for index, root in enumerate(self.repos):
            backup = retained / str(index)
            self.assertEqual((backup / MANIFEST).read_bytes(), originals[index])
            self.assertEqual((backup / ".agents/skills/go/SKILL.md").read_bytes(), original_skills[index])
            for name in NAMES:
                link = backup / ".claude/skills" / name
                self.assertTrue(link.is_symlink())
                self.assertEqual(os.readlink(link), f"../../.agents/skills/{name}")
                self.assertTrue((backup / ".agents/skills" / name / "LICENSE").is_file())
        shutil.rmtree(retained)


if __name__ == "__main__":
    unittest.main()
