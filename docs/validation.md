# Validation evidence

This installation does not invoke the new workflows, execute backlog tasks, close
real issues, or write production data. Verification date: 2026-10-10.

## Source and workflow checks

- Official skill-creator `quick_validate.py` accepted all three final packages
  using PyYAML 6.0.3 from a temporary dependency directory.
- Skills CLI 1.7.2 `add . --list` discovered exactly `go`, `simplify`, and
  `triage-and-go` with their real metadata. Its isolated multi-agent install with
  empty home created the requested layout; changing local source then restoring
  proved its computedHash lock does not enforce an immutable source revision.
- An actual installed Codex app-server `skills/list` request (no model turn)
  discovered all three inert project fixtures with repository scope and no errors.
- [Independent plan review and 15 go/simplify decisions](reviews/go-simulations.md)
  passed: multi-PR merge ordering, material re-review, latest-head failed CI,
  concurrent heads, pending auto-merge/queue, missing required approval, partial
  completion, rollout gates, unavailable independent review/archive, interruption
  resume, bundled-command collision, report-only, and supported no-op cleanup.
- [Independent triage decisions](reviews/triage-simulations.md) passed seven
  scenarios covering evidence-based ROI, human-dependent exclusions, unique
  duplicate requirements, merged-but-undeployed/partial fixes, resume, hidden
  blockers/replacement, and missing capabilities. Minor endpoint/replacement
  clarifications were incorporated. These are read-only instruction simulations,
  not proof of live autonomous execution or cloud credentials.
- [Independent source review](reviews/source-review.md) found archive-substitution,
  rollback-recovery, provenance-edit, and local tar-mode risks. All were fixed,
  covered by executable fixtures, and accepted in focused independent re-review.
  Pinned [CLI behavior](reviews/cli-behavior.json) and inert
  [Codex discovery](reviews/codex-discovery.json) summaries retain observed results.
- Simplify's upstream Apache-2.0 LICENSE Git blob is exactly
  `d645695673349e3947e8e5ae42332d0ac3164cd7`. Attribution and modified-file notice
  travel with each package. The exact upstream revision is in its PROVENANCE.md.

## Installer and consumer validation

All **32** installer integration tests passed on the final script (131.430s).
Executable installer tests use disposable Git repositories, empty home, no network,
and inert fixtures. They exercise full revision/source integrity, regular files,
ancillary files, mode preservation, relative links and Git mode 120000, fresh clones,
source worktree isolation, idempotence, updates/removals, changed/staged/unknown
managed-file refusals, all-consumer preflight, expected fetch/push remotes, unsafe
parent/file/manifest links, unrelated skills/settings/staging preservation,
check-only tampering detection, export omissions, and I/O rollback.

Final test counts, consumer check results, installation revision, fresh-checkout
proof, review disposition, backup inventory, and PRs are recorded below after
the ordinary installation validation finishes. Pending work is not recorded as
passing evidence.

## Boundaries

No live cloud task was provisioned. Default-branch cloud availability requires
consumer PR merge, correct environment setup, actual GitHub/check/rollout rights,
and a host supporting independent review. Personal Mac skills do not supply cloud
skills or permissions. Existing sessions may cache old skill catalogs; reopen them.
Prepared installation PRs are reviewable; creating the skills does not invoke go
or authorize treating a queue entry/partial delivery as completed backlog work.
