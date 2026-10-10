---
name: simplify
description: Simplify a supplied PR, branch diff, or current changes for clarity, reuse, simplicity, and efficiency while preserving intended behavior. Use for the shared simplify workflow, /simplify or $simplify where supported, or a cleanup pass before validation. Applies supported improvements by default; supports report-only mode.
license: Apache-2.0
---

# Shared simplify

This file defines the shared `simplify` skill. When another workflow requests this skill, read and follow the repository's `.agents/skills/simplify/SKILL.md` (or its `.claude/skills/simplify` link). Do not substitute a host's bundled command with the same name. This is a portable adaptation of Anthropic's published `code-simplifier` agent prompt, a separate artifact from Claude Code's bundled `/simplify` command. See [PROVENANCE.md](PROVENANCE.md) and [LICENSE](LICENSE).

Modified from the upstream prompt: removed provider/model declarations and provider-specific tooling; replaced imported language-specific style rules with repository standards; added complete-diff scoping, reuse and efficiency review, report-only behavior, and validation requirements.

## Scope and constraints

- Follow the user's constraints and applicable repository instructions, including `AGENTS.md` and any other instruction files the host loads. Repository standards take precedence over stylistic preferences imported from the upstream prompt. Use the repository's language, formatting, error handling, module, and testing conventions.
- Improve the changed implementation while preserving intended behavior, public contracts, error semantics, security boundaries, concurrency guarantees, transaction behavior, and runtime compatibility. Clarity matters more than fewer lines.
- Honor `report-only` or equivalent instructions: inspect and report findings and proposed improvements without editing source, staging, committing, pushing, or opening PRs. Use non-mutating checks where available and disclose checks that cannot be run safely in this mode.
- Preserve unrelated work and existing staging choices. Creating or installing this skill does not invoke it. A cleanup pass does not itself authorize commits, pushes, publication, or PR creation; those may be authorized by the enclosing delivery workflow.

## Gather the complete diff

1. Resolve the repository root and inspect its Git status and applicable instructions before selecting a baseline.
2. If a PR is supplied, read its actual base and head refs/commits and obtain the entire PR diff against its base, including every changed file and every commit in the PR. A latest-commit diff is insufficient. If a branch or explicit range is supplied, use that target and the intended PR base or supplied baseline. Identify the base and head in the result. Do not treat a branch's tracking ref as the PR base without verifying it.
3. With no target, review current staged and unstaged changes plus relevant untracked source files. If the current branch is being prepared for a PR or the enclosing workflow supplies its PR boundary, also review the complete branch diff against that PR's verified base. Do not invent an arbitrary previous-commit baseline or silently expand into a whole-repository refactor. If there are no current changes and no known PR boundary, report that there is nothing to simplify.
4. Read the complete diff and surrounding code, relevant callers, tests, and existing helpers. Include task-owned changes made since the selected head so the cleanup covers the implementation that will actually be submitted. Use paginated APIs or local Git when a tool truncates a diff; disclose any scope that cannot be inspected instead of claiming a complete review.
5. Read binary/generated changes through their source inputs or suitable tools where relevant. Keep repository-generated outputs consistent with their sources; do not manually refactor generated files. State the selected scope and any limitations.

## Review for supported improvements

Examine all of these angles; no fixed number of reviewers is required. Use independent read-only subagents when available and useful, giving them the same complete scope and constraints. If delegation is unavailable, perform these cleanup passes locally and describe the actual review performed. This optional cleanup delegation does not replace the independent plan review required by the shared `go` workflow.

- **Clarity and simplicity:** reduce unnecessary nesting, redundant state, repeated logic, dead task-owned code, and abstractions that add no useful boundary. Improve confusing names and remove comments that merely restate obvious code while keeping comments that explain intent. Prefer explicit control flow when compact expressions obscure meaning. Preserve useful abstractions and separate concerns.
- **Reuse:** search existing helpers, types, constants, and adjacent code before introducing another implementation. Reuse only when contracts and semantics match. Do not force similar-looking but different operations into one abstraction.
- **Efficiency:** remove demonstrably redundant computation, allocation, I/O, or retention introduced by the change. Inspect hot paths and startup costs where relevant. Parallelize only genuinely independent operations within existing rate limits and ordering requirements. Avoid speculative caches, unbounded concurrency, and claims of measured gains without measurements.
- **Appropriate structure:** place behavior in the module or layer that owns it, and prefer correcting a task-related shared mechanism when it clearly replaces repeated workarounds. Keep local behavior local when appropriate; greater generality is not automatically an improvement.

Require concrete evidence and a specific behavior-preserving improvement for each finding. Do not manufacture findings to meet a quota. Do not turn cleanup into unrelated redesigns, dependency upgrades, speculative abstractions, or correctness changes. Record discovered correctness concerns separately for the enclosing workflow to resolve through its normal review and validation.

## Apply and validate

1. Verify findings against the code and deduplicate them. Resolve competing suggestions in favor of the smallest clear improvement. Skip false positives and suggestions whose safety cannot be established; explain material skips briefly.
2. In report-only mode, return evidence, locations, and proposed changes without applying them. Otherwise apply supported improvements within the selected task scope. Coordinate edits centrally if subagents reviewed the code.
3. Run repository-required checks and validation appropriate to the affected behavior. Focused coverage is useful when it protects a meaningful invariant; tests that merely mirror a mechanical refactor add little value. Respect report-only constraints and available host capabilities.
4. Read the final complete diff again for unintended behavior changes and unrelated edits. If fixes create additional cleanup or validation concerns, resolve those before finishing.
5. Report the scope, improvements applied or proposed, material skipped findings, and actual validation results and limitations. If the code is already clear, say so without manufacturing edits. Do not imply checks passed when they were unavailable or failed.
