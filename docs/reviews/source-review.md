# Independent source review

Reviewer: independent read-only subagent `simplify_upstream`.
Date: 2026-10-10.
Scope: the complete draft addition set under adam-messinger, relative to its initial empty default-branch tree; the updater, tests, CI workflow, root README/instructions/ignores, compatibility documentation and implementation plan, all three skills, and simplify license/provenance. Git diff against HEAD is empty because these additions were still untracked, so each added file was read explicitly. This is an ordinary independent source review, not invocation of the newly authored simplify/go/triage skills. No repository files were edited and no backlog workflow was executed.

Reviewed updater SHA-256: `b78c92ca447b803dbd50ba0e2a73bce7d261e465f9e08d5194b4925d8a996fa1`. The coordinator and test agent are modifying files concurrently; locations refer to the captured review snapshot and require focused re-review after repairs.

Comparison base: `30b9f10c1607c655e37caad75cbe0a9f852e4ab7` (empty tracked tree).

## Findings requiring changes

### [P1] Compare archive bytes with committed blobs, not just names

Location: scripts/update-shared-skills.py, snapshot(), lines 57-77.

The exporter checks that the archive's paths equal the selected Git tree's paths, but it accepts each archived file's bytes without comparing them to the corresponding blob. `git archive` applies export-subst: placeholders can be replaced while the path set remains identical. Such attributes can also be supplied locally through `.git/info/attributes`, so the same source SHA can yield transformed bytes without any new source commit. This breaks the promised exact immutable-source export and can make fresh-source verification disagree with an installation. [Git's official archive documentation](https://git-scm.com/docs/git-archive#_attributes) documents both substitution and local attribute overrides.

Suggested repair: obtain each selected tree entry's blob ID and Git file mode using a NUL-safe ls-tree read; compare archive bytes with those committed blobs (or reject any transformed archive). Compute executable normalization from the Git mode rather than local tar.umask. Add inert coverage for both committed export-subst and a local info/attributes override; both consumers must remain untouched on refusal.

The existing export-ignore test correctly detects omitted files, but its path-set assertion does not cover content substitution.

### [P1] Retain the recovery directory when rollback itself fails

Location: scripts/update-shared-skills.py, update_all(), lines 170-202.

The backup is owned by TemporaryDirectory. If an install raises and restoration also raises—for example because the same persistent permission/I/O problem prevents a restore—the context manager deletes the recovery directory while unwinding. The destinations may retain a partial update, and the only copy of prior untracked managed files is then discarded. Git cannot recover a pre-existing untracked installation, so a blanket instruction to retain Git recovery does not cover this failure.

Suggested repair: create an explicitly managed backup directory and delete it only after installation verification succeeds or rollback fully restores every managed path. If restoration fails, retain the directory, print its absolute recovery path, report the original install error and restoration error, and fail. Add a failure fixture that injects an install error followed by a restoration error and confirms recoverable prior content remains. The existing successful-rollback fixture is valuable but covers only the restoration-success path.

### [P2] Refuse unstaged edits to a tracked provenance manifest

Location: scripts/update-shared-skills.py, preflight(), lines 121-136.

The update path refuses staged managed paths and mismatched installed file hashes/modes. It does not refuse a tracked manifest's unstaged edits when its files/modes still match installed content. Editing only prior.revision or adding a local manifest field therefore passes update preflight and is silently overwritten. MANIFEST is explicitly listed as a managed path; this loses related unfinished work and weakens provenance validation.

Suggested repair: refuse unstaged changes to an already tracked manifest while allowing the intended idempotent first installation whose manifest is untracked. Validate the prior revision's immutable-SHA format as well. Add update-mode refusal/preservation coverage for a changed tracked revision and for a locally added manifest field. The current tampered-manifest test exercises --check only.

## Coverage and supported design choices

- Source identity plus matching fetch/push identities, full-SHA selection, all-consumer preflight, real-file destinations, exact Claude link targets, staged managed-path refusal, and preservation of unrelated directories are appropriate.
- The executable-mode map and normalized installed permissions address the prior mode finding. Tests should confirm fresh clone modes and mode-only local changes.
- Using the CLI for discovery/behavior fixtures and the committed offline updater for exact revisions is coherent. It avoids representing a computed lock hash as a Git revision pin.
- Skill text preserves full-PR simplification, report-only mode, independent plan review/material re-review, latest-head merge gates, partial issue scope, resumability, and capability blockers. It does not require a fixed cleanup reviewer count.
- Simplify's attribution, immutable upstream revision, prominent modification notice, and verbatim Apache-2.0 license are preserved. Root README keeps the source repository's existing profile/history purpose.
- The revised implementation plan appropriately distinguishes immediate primary-checkout installation from default-branch cloud activation after consumer PR merge. Documentation states actual cloud prerequisites and avoids claiming skills grant credentials.
- Source workflow checks remain offline and do not invoke delivery. Test execution is owned by the coordinator's test agent; this review does not claim runtime test results.

No speculative refactors or extra cleanup findings are requested. The three fixes above should receive focused independent re-review and relevant fixture validation before installation.

## Focused correction re-review

Reviewed actual corrected script after the coordinator's follow-up request. This remains read-only inspection; the test agent owns executable fixture validation.

Corrected updater SHA-256 at re-review: `af2efe246c2750c7870867891cf25b66a31e3586c9ee8b393d02abaddf138580`.

- **Archive substitution finding: resolved for bytes.** snapshot() lines 78-81 compare every archive entry against `git show <SHA>:<path>` and reject transformed content before consumer writes. Both committed and local export-subst therefore cannot silently alter the installed bytes. The complete path-set omission check remains intact.
- **Rollback-backup loss finding: resolved.** update_all() now uses mkdtemp, keeps the backup when restoration raises, includes both the update and restoration errors plus the absolute recovery path, and deletes the backup only after successful verification or full restoration. A failure while initially building the backup still cleans that incomplete backup before any consumer writes, which is safe. RuntimeError is caught by the CLI for a readable failure message. No further backup preservation flaw was found.
- **Tracked manifest edit finding: resolved.** preflight() rejects a tracked manifest's unstaged changes unless its parsed content already equals the requested verified snapshot, which supports a safe idempotent rerun. Prior manifests require the exact schema keys, expected source, full immutable SHA format, expected relative links, and matching installed content/modes. Added local fields and changed historical revision values therefore cannot be overwritten silently by a different revision update.
- **Remaining mode follow-up [P2]:** normalized executable status still comes from the archive member mode, not the committed Git file mode. A local Git tar.umask configuration can remove executable bits and produce a different mode map for the same source SHA. Use committed ls-tree mode for 644/755 normalization or verify/reject a differing archive mode. Existing skill packages currently contain Markdown/license files; this chiefly affects executable ancillary files covered by the updater's generic fixture support. [Git's archive configuration documentation](https://git-scm.com/docs/git-archive#_configuration) describes tar.umask.

The three original findings are addressed in the corrected design; complete immutable-mode handling and the test agent's new refusal/retained-backup fixtures remain the final confirmation steps.

## Final focused re-review

Final reviewed updater SHA-256: `6905d2e81f0920b0269f8d2815f5ce847a941eb0d8ca209f27cde321ee8d3045`.

**All review findings resolved; no remaining actionable finding in the reviewed changes.**

snapshot() now reads recursive NUL-delimited ls-tree entries, accepts only committed regular-file modes 100644/100755 and blob objects, compares archive bytes directly with each committed cat-file blob, and derives installed 644/755 permissions from the Git mode. Local tar.umask can no longer change the manifest's executable status. Filename-set verification still rejects archive omissions, and archive-path/type checks remain intact. This resolves the remaining mode follow-up and completes the original immutable-source finding.

Rechecked the retained-backup path: failed restoration bypasses cleanup and emits the absolute backup directory in a caught RuntimeError; successful update or completed restoration removes it. The backup remains outside project skill discovery. The tracked-manifest refusal, exact schema/source/full-SHA/link checks, staged-path refusal, complete installed hashes/modes, and all-consumer preflight remain present.

The final result is approved on code inspection. The test agent's fixture/suite results remain separate evidence; this reviewer did not execute the skills or live delivery actions.
