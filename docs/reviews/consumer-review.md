# Independent consumer integration review

Read-only review of `/private/tmp/shared-skills-cashflow` and `/private/tmp/shared-skills-geddy`. No consumer source edits, workflow invocation, real issue mutation, or production access was performed by this reviewer. Root is running required repository checks independently.

## Findings

### Resolved P2: Update active documentation links to the new canonical instruction file

Cashflow replaces the 628-line CLAUDE.md with a three-line `@AGENTS.md` shim, but these active documents still send human readers to sections that the shim no longer contains:

- README.md:103: full grouped table list in CLAUDE.md's Database Schema section.
- docs/DESIGN.md:149: full grouped table list in CLAUDE.md → Database Schema.
- docs/runbook-migrations.md:3: authoritative Database Migrations rules in CLAUDE.md; additional named-section references at :43 and :68.
- docs/REVIEW-CHECKLIST.md:122: auth manual-merge rule in CLAUDE.md.

The shim is valid for Claude's instruction import behavior, but ordinary Markdown readers do not expand imports. Updating these current operational links to AGENTS.md makes the consolidation concrete and avoids leaving documentation pointing to absent sections. Historical proposals/audits can retain their historical CLAUDE references. This finding was sent to root and **resolved**: all listed active references now name AGENTS.md; scripts/setup-cloud.sh's instruction reference was also corrected without changing behavior.

## Verified preservation

- Cashflow migrated reference body from `## Project Overview` onward is byte-for-byte identical to `git show HEAD:CLAUDE.md`, with only the unique Next.js agent-rules block appended. No current repository instruction was lost or broadened in that body.
- Cashflow primary checkout's existing untracked AGENTS.md still hashes to `e930e745c79222ca44222b29043d1af62dd0e4f5ac45b197f663ed1c2db8cfe4`, identical to the initial audit. Unrelated primary-checkout flows implementation/test edits remain outside these worktrees.
- Cashflow's early policy header requires reading the entire file and documents the Codex 32 KiB default automatic budget. It preserves early production-write approval, required validation/checks, migration/manual sequencing, real preview sign-in/connector gate, autonomous triage exclusions, actual merge/deployment verification, partial-issue preservation, and protections against weakening gates. Full precise manual-merge/migration/auth rules remain in the identical reference body.
- Geddy's full original AGENTS text is unchanged; the only diff appends shared developer skill instructions and protects the top-level public plugin skills directory.
- Both CLAUDE.md shims use supported `@AGENTS.md`; no duplicated independent instruction source was created.

## Ignore and plugin boundaries

`git check-ignore --no-index -v` verified:

- Cashflow ignores local settings, worktrees, credentials, agent operational workspace directories, env files, and managed-agent secrets; existing tracked reusable settings/hooks are retained.
- Geddy ignores local/private Claude settings, worktrees, credentials, and unrelated skill directories while exposing exactly the three named .claude skill entries. The .agents real skill paths remain trackable.
- Geddy `scripts/package-plugin.mjs` is unchanged and has an explicit package-entry allowlist of `.codex-plugin`, `.mcp.json`, and top-level `skills`. Developer .agents/.claude paths cannot enter that bundle through the current packaging code.
- `git diff --check` passed in both worktrees at review time.

## Test changes

Cashflow existing `docs-drift.test.ts` DD4/DD5/DD8 and `identity-import-boundary.test.ts` IB2 assertions are preserved; only their canonical instruction-file input and descriptions changed from CLAUDE to AGENTS. These tests now exercise the actual full content rather than silently scanning the short shim. Their existing semantic invariants (tool/category documentation, retired paths, pin claims, identity facade retirement) are meaningful, and no assertion was weakened to accommodate consolidation.

Reviewed these test changes against docs/REVIEW-CHECKLIST.md: no falsy fallback, catch, data mutation, shared behavior duplication, date math, fail-open gate, progress-marker, compact/output-key, or framework-input assumption is introduced.

## Final installed-artifact verification

The final installed files in both consumers use source revision `6f552f4e9a7a2734e2c1b19dc6e9c5b9fed523aa`. Independently verified with a read-only Python/Git comparison:

- Both `.agents/shared-skills.json` files are byte-identical and record that exact revision/source.
- Both consumers contain the exact complete five-file source inventory, with no missing or extra files in the three managed skill directories.
- All files are regular files, byte-identical to `git show <revision>:skills/...`, and their actual SHA-256 hashes and modes match each manifest.
- Files checked: go/SKILL.md, simplify/SKILL.md, simplify/PROVENANCE.md, simplify/LICENSE, and triage-and-go/SKILL.md. The upstream attribution/full license travel with both installed copies.
- All three `.claude/skills/<name>` entries are actual symlinks whose targets are exactly `../../.agents/skills/<name>`; each resolves inside its own consumer and yields the same SKILL.md bytes.
- Cashflow original tracked CLAUDE reference body is still exact, followed only by the preserved Next.js block. Primary local AGENTS hash remains unchanged. Geddy original AGENTS body remains exact.
- Cashflow early policy now explicitly says both migration and sign-in changes require manual merge; production approval and no-human triage exclusion stay early.
- Both new consumer `docs/shared-agent-skills.md` files coherently describe invocation, source revision, manifest, relative layout, pinned one-command updates, check-only verification, permissions, independent review, cloud setup, and no workflow invocation as installation test. Canonical source guide and current validation record are consistent with those descriptions.
- `tar -tzf public/downloads/geddy-plugin.tar.gz` after the actual build contains only `.mcp.json`, `.codex-plugin`, and capture-family-history public skill/reference/script entries. No developer go/simplify/triage files or .agents/.claude paths enter the bundle.

All independent preservation/content/hash/mode/link/inventory comparisons produced zero errors. No remaining introduced actionable bug was found in this integration.

## Handoff limits

Root reports Cashflow lint/typecheck passed and full offline suite finished 7,113 passed / 0 failed / 1 skipped. This reviewer did not rerun those checks. Root is resolving a Geddy large-inventory test timeout; actual full-suite and required latest-commit hosted CI results remain the delivery gate, not something this read-only review can mark passed.

Geddy's temporary test `node_modules` symlink is currently untracked because the directory-style ignore does not match a symlink; it must be excluded/removed before commit. Root was notified. This is a transient validation artifact, not an intended installation file.

Consumer docs state obsolete matching globals were backed up outside discovery. Root must ensure this authorized cleanup is complete before final reporting; the reviewer did not perform or independently re-check global mutation. Git index link mode 120000 will be verified after root stages/commits; filesystem symlink types and exact targets are already verified.
