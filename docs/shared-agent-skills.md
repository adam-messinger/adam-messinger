# Shared developer skills

Verified 2026-10-10. `adam-messinger/adam-messinger` is the canonical authoring
repository. Geddy and Cashflow contain committed copies of one source revision:

```text
.agents/shared-skills.json        # source commit + per-file SHA-256 and Git modes
.agents/skills/go/SKILL.md
.agents/skills/simplify/{SKILL.md,PROVENANCE.md,LICENSE}
.agents/skills/triage-and-go/SKILL.md
.claude/skills/go                 -> ../../.agents/skills/go
.claude/skills/simplify           -> ../../.agents/skills/simplify
.claude/skills/triage-and-go       -> ../../.agents/skills/triage-and-go
```

Skill use needs only this checkout. No home-directory skill, submodule,
cross-repository fetch, package installer, or startup network is required.
Geddy's top-level `skills/` remains its public historical-research plugin.

## Invocation and authorization

| Host | Invocation |
| --- | --- |
| Claude Code | `/go <task or issue>`, `/simplify [PR/diff] [report-only]`, `/triage-and-go` |
| Codex CLI / IDE | `$go <task or issue>`, `$simplify [target] [report-only]`, `$triage-and-go`; `/skills` also selects skills |
| Current Codex/ChatGPT desktop selectors | Select the project skill with `@` where offered; use an explicit project file reference if ambiguous |
| Any capable agent host | Ask it to read the corresponding `.agents/skills/<name>/SKILL.md` and execute that workflow |

`/go` in the portable descriptions denotes the workflow; a plain slash command is
not the documented Codex CLI invocation syntax. `go` and `triage-and-go` explicitly
read the shared sibling files, so they cannot accidentally substitute Claude's
bundled `/simplify`. The shared simplify is an adaptation of the separately
published Anthropic code-simplifier prompt, with no fixed cleanup reviewer count.
Its [provenance](../skills/simplify/PROVENANCE.md) records the exact upstream commit
and its Apache-2.0 license accompanies every copy.

Explicit delivery invocation authorizes task-related GitHub/implementation/eligible
merge actions described by the skill; narrower user requests and repository rules
remain in force. Creating, editing, installing, or testing metadata does not invoke
these workflows. Skill installation grants no tool permissions or credentials.

## Update both consumers with one command

Edit and commit this source first. Select a reviewed full 40-character commit SHA,
available in this checkout's object database. Run from the canonical source root:

```sh
python3 scripts/update-shared-skills.py --revision <FULL_SOURCE_COMMIT_SHA> --repos /Users/adam/github/geddy /Users/adam/github/cashflow
```

Replace the two paths with clean worktrees when preparing installation PRs. The
command validates the source and both fetch/push origins, exports exactly the
selected commit once, installs identical regular files and relative links in both
consumers, records source SHA/hashes/modes, and verifies them. It has no runtime package
dependencies beyond Python 3 and Git and performs no network access. It ignores
uncommitted source edits. A source branch, tag, abbreviated SHA, unsafe symlink,
unknown old skill tree, modified managed tree, or staged managed paths is refused.
Both consumers are checked before writing either; ordinary I/O failures restore
the managed paths from a temporary backup. If rollback itself fails, the command
retains that backup and reports its absolute recovery path. Process termination or disk failure can
interrupt rollback: retain Git recovery and rerun verification before claiming a
complete update. Unrelated skills, settings, lockfiles, staging, and work are not
managed by the updater.

For a first installation with old same-name directories, preserve them outside
skill discovery first, then remove only those conflicting paths. Never pass a
force flag or erase unrelated `.agents/` or `.claude/` content. The initial task
backs up existing project/global copies separately; future local customization
should be upstreamed rather than overwritten.

Append `--check` to the same command for non-mutating SHA/content/link verification.
Review and commit the three `.agents/skills/` trees, `.agents/shared-skills.json`,
and three `.claude/skills/` links in **both** consumer repositories. Commit required
instruction/ignore changes separately or with the initial installation. The
updater deliberately does not stage, commit, push, merge, or edit ignore rules.
Fresh checkouts become available once those installation commits are checked out;
default-branch cloud sessions require the consumer PRs to merge.

## Skills CLI discovery and verified lock behavior

The existing [Vercel skills CLI](https://github.com/vercel-labs/skills) was tested
at version **1.7.2**, source revision `bc7742451b64f2c2460a2c2c4289cdda03b9a08e`.
Use it to discover this portable source:

```sh
npx --yes skills@1.7.2 add . --list
```

An isolated empty-home install was also tested with:

```sh
npx --yes skills@1.7.2 add <LOCAL_SOURCE_CHECKOUT> --skill go simplify triage-and-go --agent codex claude-code --yes
```

With both agents and default symlink mode it creates precisely the real `.agents`
files and relative Claude links requested here. Do not add `--copy`, `--global`,
or `--all`. The local-source lock records `source`, `sourceType`, and `computedHash`,
**not a source Git SHA**. Changing source and running `experimental_install`
restored changed bytes and rewrote the hash without rejecting it; restoration also
does not reconstruct Claude links from that local lock. The hash is not an
immutable-revision guarantee. See the pinned upstream
[lock implementation](https://github.com/vercel-labs/skills/blob/bc7742451b64f2c2460a2c2c4289cdda03b9a08e/src/local-lock.ts)
and [restore command](https://github.com/vercel-labs/skills/blob/bc7742451b64f2c2460a2c2c4289cdda03b9a08e/src/install.ts).

Therefore production updates use the committed offline exporter and explicit
provenance manifest, while CLI fixture/discovery checks validate compatibility.
Existing consumer `skills-lock.json` entries for unrelated installed skills are
preserved. Do not run a generic CLI restore as a substitute for the pinned updater.

## Provider discovery, instructions, and precedence

[Codex skill docs](https://learn.chatgpt.com/docs/build-skills) describe project
`.agents/skills` discovery from the current directory through repository ancestors,
required name/description metadata, symlink support, and explicit `$skill` use.
Same-name skills are not merged and may both appear. An actual no-model local
app-server `skills/list` check discovered all three inert project fixtures with
repository scope and no errors, under an empty home.

[Claude skill docs](https://code.claude.com/docs/en/skills) support project
`.claude/skills` and symlinked skill directories. Enterprise skills precede personal
skills, which precede project skills; project skills override same-name bundled
commands. Remove obsolete same-name personal copies only after project verification.
Reopen sessions after installation/removal because their discovered catalogs may
be cached. Other enterprise/personal/plugin overrides must be inspected on each
executing host; installed files cannot override organizational policy.

[Codex instruction docs](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
use `AGENTS.md`, closer instruction precedence, and a default aggregate 32 KiB
budget. Cashflow has a larger preserved reference, so its critical rules and a
mandatory full-file read appear first. Trusted local projects may raise the limit,
for example `codex -c project_doc_max_bytes=131072`; cloud project-config trust is
not assumed. The instructions do not depend on a Mac home setting.

[Claude memory docs](https://code.claude.com/docs/en/memory#remove-an-earlier-agentsmd-workaround)
explicitly allow removing an import-only `CLAUDE.md`. These repositories use
`AGENTS.md` directly, with no root compatibility shim. Direct loading requires
Claude Code 2.1.277 or newer; use 2.1.281 or newer to avoid earlier provider and
telemetry exceptions. Keep the AGENTS reader enabled and Project instructions at
its default or “both” setting. A project/ancestor `CLAUDE.md`, `.claude/CLAUDE.md`,
or `CLAUDE.local.md` suppresses default AGENTS loading; a global
`~/.claude/CLAUDE.md` does not. Older runtimes or a first session after an upgrade
may require upgrading/restarting or explicitly reading the repository's AGENTS
file. Cashflow's entire tracked guidance is preserved with file references updated
and its instruction-reading tests migrated; the primary checkout's pre-existing
untracked AGENTS remains untouched by this installation.

## Cloud prerequisites and actual limits

[Codex cloud docs](https://learn.chatgpt.com/docs/environments/cloud-environments)
make checked-in repository skills available; personal Mac skills are not synced.
[Claude Code web docs](https://code.claude.com/docs/en/claude-code-on-the-web)
describe separate cloud runtime, network, setup, and credential configuration.
Check out the installation commit or merge its PR into the configured branch.
No startup fetch of this canonical repository is needed.
The Claude cloud runtime must meet the same version and AGENTS-reader conditions
above; the cloud documentation does not guarantee its installed version.

Configure the intended GitHub repository and network access for GitHub API/source,
package registries, and required deployment services. `api.github.com` may need an
explicit allowlist entry. Supply scoped GitHub, test, and rollout credentials through
the host's secret mechanism. Verify push, merge, approvals, latest-commit checks,
independent subagent review, and rollout capabilities at invocation. A clone/push
credential alone does not prove merge or deployment permission.

Geddy needs Node 22 and `npm ci`; offline check/build is sufficient for installation.
Cashflow's existing Claude SessionStart bootstrap and production guard remain
intact. Its hook is gated by `CLAUDE_CODE_REMOTE=true` and does not automatically
bootstrap Codex cloud; configure the Codex environment's repository setup with
`npm ci` explicitly. Cashflow tests force local test data and need no production
secrets. Live delivery must honor its manual migration/sign-in gates and explicit
production-write approval. No live cloud environment, credential provisioning,
backlog delivery, production operation, or live archive test was performed here.
Missing independent review blocks `go`; unavailable archival is reported after
other supported completion/cleanup. There is no silent self-review fallback.

See [validation evidence](validation.md) and the [implementation plan](implementation-plan.md).
