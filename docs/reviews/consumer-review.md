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

## Handoff limits at the initial review

Root reports Cashflow lint/typecheck passed and full offline suite finished 7,113 passed / 0 failed / 1 skipped on the original installation commit, before the current-main merge. This reviewer did not rerun those checks. At the initial review, root was investigating a Geddy large-inventory test timeout. Its local timeout and subsequent complete hosted CI pass are recorded in [validation evidence](../validation.md); this read-only review does not substitute for required checks.

Geddy's temporary test `node_modules` symlink is currently untracked because the directory-style ignore does not match a symlink; it must be excluded/removed before commit. Root was notified. This is a transient validation artifact, not an intended installation file.

Consumer docs state obsolete matching globals were backed up outside discovery. Root must ensure this authorized cleanup is complete before final reporting; the reviewer did not perform or independently re-check global mutation. Git index link mode 120000 was independently verified in both committed consumers after the final focused review; filesystem symlink types and exact targets are also verified.

## Focused review after current-main conflict resolution

Reviewed Cashflow installation head `fef42738caff5e9bbae831cd4c4e966c27c5a0e1` against current origin/main `80046c5e4e3135c3b35a4855f2fe74c0a7e05e13`. Main had advanced with the equal-length account-name fix and write-once Blob store behavior while installation was in progress. Root merged current main, resolved CLAUDE consolidation by retaining the import shim, and rebuilt the AGENTS reference from the complete current-main CLAUDE body while preserving the existing shared policy header and Next.js block.

Independent read-only comparisons confirm:

- The AGENTS reference from `## Project Overview` through the original final `Not in Scope` paragraph is **byte-for-byte identical** to current `origin/main:CLAUDE.md`, including the new write-once Blob rule: same bytes resolve, other bytes under an existing key throw, replacement requires delete-then-put. Reference body SHA-256 is `f42d1c64684af84f0e41c4eb46d3bca747fc146da0f6791b7c36dc37d37f80cb`.
- Every current-main instruction was retained. No applicable content was lost during conflict resolution, and the critical early production/manual-merge/validation policy remains intact.
- `git diff origin/main...HEAD -- src` is empty: merged unrelated application behavior remains part of main, not the installation PR diff.
- Installed five files, hashes/modes, provenance revision `6f552f4e9a7a2734e2c1b19dc6e9c5b9fed523aa`, and all three link targets remain unchanged and valid.
- Both consumer Git indexes record the three Claude links as mode **120000**, with matching link blobs in Cashflow and Geddy.
- Primary Cashflow untracked AGENTS still hashes to `e930e745c79222ca44222b29043d1af62dd0e4f5ac45b197f663ed1c2db8cfe4`; unrelated local work remains preserved.
- Cashflow worktree is clean. `git diff --check origin/main...HEAD` passes. Canonical-documentation test changes still preserve their original assertions; root reports all 10 focused docs/identity tests passed after the merge.

**Conflict disposition: accepted. No remaining actionable preservation/integration finding or review blocker.** Actual full CI/deployment results are recorded by root separately; this focused read-only review does not substitute for required checks.
