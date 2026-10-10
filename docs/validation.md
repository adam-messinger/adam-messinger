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

Verified installed source revision: `6f552f4e9a7a2734e2c1b19dc6e9c5b9fed523aa`
in both primary consumer checkouts and both clean installation PR worktrees.
[Fresh actual committed checkouts](reviews/fresh-checkouts.json) had clean Git
status, unchanged empty home, five exact regular files with matching hashes/modes,
three resolving relative links recorded as Git mode 120000, identical manifests,
and no network. This proof used actual installation commits rather than only
inert fixture packages.

[Independent consumer review](reviews/consumer-review.md) accepted instruction
preservation, active documentation/test migration, private ignores, exact
installation content, and Geddy public-plugin boundaries. The primary Cashflow
untracked AGENTS.md remains byte-identical; unrelated primary work was excluded
from the installation commits.

Cashflow lint and TypeScript passed on installation commit
`efff215a24b1445d2fabe4fa0eeb72c1fbb46b65`, before the current-main merge. The initial
sandboxed test launch hit a tsx local IPC EPERM; the full suite outside that
restriction passed **7,113 tests, zero failures, one skipped** (333.720s).
Latest-head validation after conflict resolution is recorded separately below.
Required hosted PostgreSQL, build/HTTP and aggregate CI checks remain in force.

Geddy typecheck, lint, and build passed; its built public-plugin tar includes only
the research skill and no developer skills. Initial parallel offline tests hit
four archive/PGlite timeouts. A serialized full rerun passed 1,725 tests with one
existing 50,000-object restore test exceeding its unchanged 30s timeout. An isolated
rerun of that file passed eight cases and again timed out on that large inventory.
No Geddy `src/` or `tests/` file differs from the PR base, and the reused dependency
versions match its lockfile. No test, assertion, or timeout was changed. This is a
documented local validation failure; required hosted CI is checked independently.

After both primary installations and fresh checkouts were verified, obsolete
global Codex go/simplify/backlog-go and Claude go/simplify symlinks were moved to
the recoverable backup at
`/Users/adam/github/worktree-backups/shared-skills-2026-10-10`. Inventories record
original paths, file hashes and link targets. Old same-name project go copies were
separately copied/verified before replacement. Other global/project skills,
credentials/settings, and unrelated work were preserved.

Prepared PRs:

- [Canonical source #1](https://github.com/adam-messinger/adam-messinger/pull/1).
- [Geddy installation #118](https://github.com/adam-messinger/geddy/pull/118),
  commit `784a01b7675a87aeb8360ddea1a005fd4cc7e167`.
- [Cashflow installation #1965](https://github.com/adam-messinger/cashflow/pull/1965),
  commit `51827e73fd98c2b943802fdb19c210afbff49fa4` after resolving newer
  main instruction changes without losing the write-once Blob guidance.

PRs are prepared for review; this installation does not invoke go or merge them.
Default-branch cloud activation requires consumer PR merge. Canonical source CI
passed on the installed source commit and subsequent evidence commit.
[Geddy required hosted CI](https://github.com/adam-messinger/geddy/actions/runs/38085521672)
passed the complete typecheck, lint, build, and offline suite on its installed
commit. Cashflow conflict resolution preserves the complete latest main guidance,
received focused independent review, and passed all ten focused docs/identity tests.
Its original [hosted CI](https://github.com/adam-messinger/cashflow/actions/runs/38084654532)
passed on conflict-resolved commit `fef42738caff5e9bbae831cd4c4e966c27c5a0e1`.
Latest [required hosted CI](https://github.com/adam-messinger/cashflow/actions/runs/38085654605)
passed on the follow-up head listed above: static/migration/schema checks, all
four test shards, PostgreSQL contracts and built HTTP application, Turso
build/HTTP checks, coverage aggregation, and the required aggregate `check`.
Both consumers' Vercel previews passed. Production-deployment verification is correctly skipped for these PRs;
no production deployment was invoked. Recorded hosted results retain consumer
head SHAs, run links, and job outcomes in [the evidence summary](reviews/hosted-ci.json).

After hosted checks completed, both clean task-created installation worktrees and
their temporary dependency links were removed. Committed, pushed PR branches and
the verified primary installations remain recoverable. Task-created CI watchers
completed; unrelated branches, worktrees and primary work were preserved.

## Follow-up: remove CLAUDE.md compatibility shims

At the user's request, root CLAUDE.md shims were removed from all three PRs.
Repository instructions remain solely in AGENTS.md. The source and both consumer
AGENTS files are byte-for-byte unchanged from their preceding installation heads,
as are all skill files, manifests, relative skill links, application source/tests,
settings and hooks. The guide records current Claude version/reader conditions
and cloud limits; no new home-directory dependency was introduced.

Independent read-only review accepted all three removal heads without findings.
All ten Cashflow focused docs/identity tests passed again on the follow-up head.
Fresh actual committed empty-home checkouts verified the root shims are absent,
AGENTS contents are preserved, installed content/hashes/modes remain identical,
and the three Claude skill symlinks still resolve. The primary installations also
passed pinned verification again. Both follow-up worktrees and disposable clones
were cleaned up while retaining their pushed PR branches and unrelated work.

## Boundaries

No live cloud task was provisioned. Default-branch cloud availability requires
consumer PR merge, correct environment setup, actual GitHub/check/rollout rights,
and a host supporting independent review. Personal Mac skills do not supply cloud
skills or permissions. Existing sessions may cache old skill catalogs; reopen them.
Prepared installation PRs are reviewable; creating the skills does not invoke go
or authorize treating a queue entry/partial delivery as completed backlog work.
