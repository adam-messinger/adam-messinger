# Independent read-only triage simulation

Reviewed the draft files at `/Users/adam/github/adam-messinger/skills/triage-and-go/SKILL.md`, `go/SKILL.md`, and `simplify/SKILL.md`. All issue numbers, PRs, user counts, repositories, and evidence below are fictional. No GitHub mutation, workflow invocation, backlog execution, credentials acquisition, or production operation occurred. This is a prompt-level decision simulation, not an end-to-end provider execution test.

Line evidence refers to the draft as read during this review (triage 105 lines; go 84 lines).

## Scenario 1: Highest eligible ROI beats the tiny newest issue

**Hypothetical inputs:** A fictional archive server has 235 open issues. REST issues pages contain 100/100/35 records after excluding pull_request entries; open-pulls pages are inspected separately. Candidate #231 is newest and proposes renaming a barely used button (a quick edit with negligible observed user impact). Candidate #84 fixes repeated duplicate upstream requests consuming the same tight runtime/quota budget on a popular tool. A focused trace and existing test reproduce the duplicate work; an existing helper supports a small implementation and meaningful regression check, with no schema change or backfill. Candidate #19 proposes a potentially valuable cache redesign, but evidence is uncertain and rollout risk/dependencies are larger. None has active implementation PRs. Independent plan review, tests, push/merge, and transport-only rollout checks are available.

**Predicted decision:** Rank #84 first: meaningful demonstrated impact, high confidence, bounded implementation/validation, and low rollout cost. Put #231 below it despite being smaller/newer; put #19 below it because uncertainty and total delivery cost reduce expected return. Select only #84 and pass the no-human-intervention constraint into the go plan/review. Do not fabricate precise ROI scores.

**Evidence:** triage lines 25–33 demand a complete paginated inventory, separate open PR inspection, and disclose incomplete retrieval. Lines 35–38 demand complete candidate investigation. Lines 42–46 compare impact/confidence against implementation, validation, risk, dependencies, rollout/backfill and explicitly reject newest/smallest heuristics. Lines 56–60 select the highest-ROI eligible task, normally one. Lines 87–91 pass the constraint to shared go.

**Verdict:** PASS. The draft does not guarantee a mathematical ordering without real evidence, appropriately; the supplied evidence establishes a clear qualitative ordering.

## Scenario 2: Exclude human approval and manual migration even with high impact

**Hypothetical inputs:** Candidate #92 could eliminate a major sign-in regression, but repository instructions require a real preview sign-in with a fresh Google account/private window and a manual merge afterward. Candidate #77 requires a production schema migration before merge, and the repository requires separately authorized production DB writes. Candidate #65 is independently valuable, acceptance criteria are clear, it changes a pure formatting helper, existing offline tests cover the behavior, current policy permits automated eligible merge, and deployment verification needs no human. A fourth candidate #120 has clear implementation but a required human codeowner review that cannot be obtained autonomously.

**Predicted decision:** Exclude #92, #77, and #120 from autonomous delivery regardless of theoretical impact or small implementation size. Record their concrete gates in the shortlist. Select #65 if its impact makes it worthwhile; do not ask the user for new permissions/sign-in just because these blocked candidates exist. If #65 did not exist, report the strongest candidates and blockers without starting implementation. Never enable a premature migration auto-merge or bypass required human approvals.

**Evidence:** triage lines 48–54 explicitly exclude manual sign-in, manual migrations, separately authorized production writes, and required external approval unavailable autonomously; zero-review policy is not assumed. Lines 57–60 require blockers if none qualifies and avoid involving the user when an alternative exists. Go lines 12 and 60 preflight/inspect actual merge/rollout requirements, and line 69 forbids protection bypass, admin merge, dismissed required human approvals, or changed CI policy.

**Verdict:** PASS. These exclusions also match the actual Cashflow repository's preserved migration/sign-in instructions.

## Scenario 3: Duplicate report contains a unique acceptance criterion

**Hypothetical inputs:** Issue #42 says exported dates must be stable across time zones. Issue #106 has a similar title/common root cause but additionally requires the zero-result export to retain its header row. Discussion confirms this second criterion is real and absent from #42. There is no existing contradictory implementation promise. The initial common symptom alone is insufficient equivalence evidence.

**Predicted decision:** Read both full reports/discussions and current behavior. Do not close #106 merely because the titles or common root cause match. If investigation confirms a coherent canonical scope covering both requirements, first preserve the zero-result/header criterion in #42, explicitly describe the material scope change if any, and verify the canonical issue actually contains it. Only then comment on #106 with #42's link and equivalence/requirement-preservation evidence, close as duplicate, and verify the resulting state. If the zero-result criterion turns out independent or the scope relationship remains unclear, leave #106 open. If a canonical issue/closure request times out, read state before retrying to avoid duplicate additions/comments.

**Evidence:** triage lines 66–72 require equivalent scope, every unique requirement preserved before closure, a linking/evidence comment, explicit material scope changes, and leaving uncertain overlaps open. Lines 80–83 require actual resulting state and reconciliation after uncertain mutation responses. Go line 17 independently rejects title-only equivalence and line 23 preserves the original report in durable checkpoints.

**Verdict:** PASS. “Preserve every unique requirement … before closing” supplies the critical ordering; the simulation makes no actual issue update.

## Scenario 4: Merged fix is still undeployed

**Hypothetical inputs:** Issue #59 requires users' live deployed exports to use corrected dates. A fixing PR is merged to main and its focused regression test passes, but the deployed health commit is still the parent commit; deployment is pending. A comment on the issue says “fixed.” Another issue #61 has a partly relevant merged PR that handles CSV but leaves OFX acceptance criteria unimplemented.

**Predicted decision:** Leave #59 open until required deployment is verified against the fixing commit and the live behavior/required rollout check passes. Leave #61 open for its remaining OFX requirement. Do not treat the old fixed comment, merged state alone, or one green test as full completion. Record concrete evidence/blockers. Once #59's deployment and full acceptance are verified, a future real invocation could record merged PR/commit and meaningful validation before closure.

**Evidence:** triage lines 73–78 require complete acceptance against target/default merged code AND required deployment/rollout, with fixing PR/commit and meaningful evidence. Go line 54 says use non-closing references when completion requires post-merge rollout; line 71 says merge alone is insufficient for deployed criteria. Go line 75 leaves partial, blocked, or queued issues open.

**Verdict:** PASS. Both an undeployed full fix and a deployed partial fix remain unresolved.

## Scenario 5: Resume an interrupted two-PR workflow

**Hypothetical inputs:** Durable issue checkpoint #84 contains acceptance criteria A/B, independent review disposition, PR1 #300 targeting main, PR2 planned after PR1, validation logs, and “PR1 auto-merge enabled; not yet merged.” The agent was interrupted. On resume, GitHub now reports PR1 merged at commit M1. A task-owned PR2 #302 actually already exists from a later recovered session, with new head H2. Checkpoint lists older head H1 as green, but H2's latest CI is failing. Local worktree also contains an unrelated uncommitted audit note. No plan boundary change occurred.

**Predicted decision:** Reconcile checkpoint with current GitHub/Git state, record verified PR1 merge, identify and reuse #302, and inspect H2's actual diff/checks. Preserve the audit note. Do not recreate PR1/PR2, re-run unchanged completed work, trust H1's checks, or close #84. Run shared simplify on the full PR2 comparison including task-owned changes, fix actionable H2 failures, validate/latest checks, merge when eligible, verify deployment/criteria, then close. If newly discovered plan changes materially alter dependencies/boundaries, independently re-review before continuing.

**Evidence:** go line 23 enumerates durable checkpoint fields and specifically requires actual GitHub/Git reconciliation on resume. Lines 46/50 require verified preceding merge before dependent PR work. Line 53 reuses task-owned PRs. Lines 51/55/60 require full PR scope and latest commit reviews/checks; pending/missing/stale/failed results are not passing. Lines 42/50 require another independent review for material plan redesign. Lines 54/75 prevent partial closure. Triage lines 89–91 explicitly hand checkpoint/resume delivery to this shared workflow.

**Verdict:** PASS. The resume behavior treats checkpoint prose as a journal to reconcile, not a source of truth overriding actual states.

## Scenario 6: Hidden production blocker requires eligible replacement

**Hypothetical inputs:** Triage selects #84 based on evidence showing two code-only PRs. PR1 merges using `Refs #84`, and its validation is recorded. During PR2 investigation a legacy cache format is discovered: complete acceptance requires a manual production migration using new credentials and human authorization. The credentials/write capability was not known at initial preflight. A previous shortlist candidate #65 remains eligible, independent of PR1/PR2, and has no active PR. PR2 contains recoverable task-owned commits and an open non-closing PR.

**Predicted decision:** Stop dependent progress on #84 without discarding its commits/PR. Leave #84 open, record PR1's actual delivery, PR2 state, exact migration/credential/approval blocker and remaining acceptance. Reassess current candidate and open-PR state, select #65 if still highest eligible ROI, and execute go with its own independent plan review/checkpoint. Do not weaken #84 acceptance, omit rollout, ask for manual production intervention when #65 exists, loop failed credential calls, or declare pending PR2 completed. Final report names both the replacement result and preserved blocked partial work.

**Evidence:** triage lines 93–99 explicitly preserve commits/PRs, leave incomplete issues open, reassess/reselect eligible tasks, avoid duplicated active work, prohibit weakened criteria/omitted rollout, and stop unchanged failing retries. Lines 48–52 disqualify the newly discovered requirements. Go line 46 permits only independent work whose prerequisites are merged; lines 69/75 keep exact blockers/partial issues. Triage lines 101–105 require actual state/remaining blockers and disclose queued work.

**Verdict:** PASS. “Normally one per invocation” in lines 56–57 is correctly overridden by the explicit hidden-blocker replacement rule, without expanding into unbounded backlog execution.

## Scenario 7: Independent review unavailable, archive unavailable

**Hypothetical inputs:** Host A can inspect issues/PRs and run tests but provides no separate subagent/reviewer capability. Host B supports independent plan review and all delivery capabilities but has no archive-session API.

**Predicted decision:** Host A cannot deliver any candidate through go; report independent review as the shared capability blocker without presenting self-review as equivalent or implementing first. Host B may complete delivery, issues, and recoverable supported cleanup, then report unavailable archival; never archive GitHub repository or another chat. Installing either skill is not authority to start any of these fictional workflows.

**Evidence:** triage lines 20–23 require independent review preflight and explicitly forbid self-review substitution. Go lines 12/38–40 block if review absent and require waiting for an actual subagent. Go line 82 preserves queued/blocked chats and limits archive to current completed chat; triage lines 104–105 state unsupported archive is a disclosed limitation. Skill introductions explicitly say creation/editing/installation does not invoke them.

**Verdict:** PASS.

## Findings

No required behavioral gap found in the reviewed scenarios. The drafts explicitly cover inventory completeness, evidence-based ROI, unavailable capability/human gates, unique duplicate requirements, deployment-gated closure, actual-state resume, and hidden-blocker replacement.

Two minor editorial clarifications could improve operator reliability but are not failures:

1. Triage's REST example says to paginate open-pulls separately without spelling its endpoint. Naming `repos/OWNER/REPO/pulls?state=open&per_page=100` would make a common fallback directly repeatable.
2. After a hidden blocker, explicitly say to recheck the replacement candidate's current acceptance, active PRs, and capability eligibility before executing go. Existing “reassess the shortlist” and go preflight already require this; a short sentence would remove room for interpreting a stale shortlist as automatically valid.

Important practical limit: these are read-only prompt simulations. They prove the written decision rules support the predicted behavior; they do not prove every host exposes the required subagent, GitHub permissions, deployment credential, or archival capability. The draft appropriately requires runtime capability checks and honest blockers.
