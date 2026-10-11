# Shared delivery skills implementation plan

This is installation work, not an invocation of the new delivery workflows.
No backlog task, issue closure, production write, or session archival is a test.

## Acceptance criteria

- Author `go`, `simplify`, and `triage-and-go` once under `skills/` in
  `adam-messinger/adam-messinger`, preserving the existing GitHub profile purpose
  and history (the checked-out default branch is an empty reset).
- Commit identical copies from one immutable source commit in both Geddy and
  Cashflow under `.agents/skills/`, with tracked relative Claude links.
- Provide an offline, revision-explicit updater, provenance and content hashes;
  verify the skills CLI's actual discovery/install/lock behavior separately.
- Preserve repository guidance, existing unrelated work, private ignores, and
  Geddy's public research plugin. Keep applicable repository guidance in
  `AGENTS.md`, read directly by current Claude Code and Codex.
- Validate metadata, full installed trees, fresh checkouts with empty home,
  updater preservation/refusal behavior, official documentation, and independent
  decision simulations covering the requested failure and resume cases.
- Back up and disable only obsolete global `go`, `simplify`, `triage-and-go`,
  and legacy `backlog-go` installations after verifying project installations.

## Implementation and PR boundaries

1. Source PR: portable skill packages, upstream Apache-2.0 attribution/license,
   stdlib Python updater and meaningful installer tests, host compatibility docs,
   and independent review/simulation evidence. Commit and push this source first.
2. Geddy installation PR from current `origin/main`: pinned real files and
   relative links, narrow ignore exceptions, and shared-skill guidance.
   Do not touch top-level public `skills/` or the unrelated active branch.
3. Cashflow installation PR from current `origin/main`: same pinned files/links,
   narrow private ignores, move the full tracked `CLAUDE.md` instructions into
   `AGENTS.md`. Migrate docs-drift and identity-boundary
   tests to read the authoritative file without weakening assertions. Add critical
   policy guidance before the large body to account for Codex's default 32KiB
   instruction budget. The primary checkout's pre-existing
   untracked `AGENTS.md` and unrelated skill/audit work remain intact.

Also install and verify identical source copies in the primary consumer checkouts;
back up existing same-name project skills before replacement. Preserve the primary
Cashflow `AGENTS.md` unchanged; the clean PR carries the instruction migration.
Cloud default-branch activation requires merging the prepared consumer PRs. Global
disable follows verification in the primary checkouts and fresh PR checkouts.

Consumer PRs depend on availability of the pushed source commit, not on a startup
fetch. They are prepared for review; this installation request does not invoke
`go`, merge these PRs, or close backlog issues.

The initial implementation retained `@AGENTS.md` compatibility shims. The user's
follow-up removes them after official verification of direct AGENTS support;
the guide records current-version/configuration requirements for Claude hosts.

## Validation and rollout

Use the official skills CLI in disposable fixtures for discovery and install
behavior. Validate metadata and updater integration with disposable Git
repositories, including revision mismatch, dirty managed files, existing links,
remote mismatch, staged managed paths, idempotent update, preservation of unrelated
files, and rollback after I/O failures. Preflight both destinations before writes.
Reject archive export omissions, traversal, and symlinks. Test
fresh consumer checkouts against source hashes with empty home and no network.
Run Geddy's `npm run check` and build/public-bundle inspection. Run Cashflow's
lint, typecheck, docs-drift tests and full suite; its PR CI supplies required
PostgreSQL and built HTTP gates. Report actual failures and environmental limits.
No live archive quota or production data access is needed for this change.

Independent reviewers receive the actual plan/skills and synthetic scenarios,
operate read-only, and provide findings with evidence. Revise material findings
and obtain focused re-review. A prompt review/simulation is evidence of instruction
quality, not proof of future autonomous delivery or live cloud permissions.

After project verification, move obsolete globals to a timestamped recoverable
backup outside discovery roots. Record their original paths and hashes. Existing
sessions may retain cached skill catalogs; reopen sessions after installation.
Cloud hosts need GitHub/test/rollout credentials and independent review support;
missing capabilities remain blockers and are documented, never assumed granted.
