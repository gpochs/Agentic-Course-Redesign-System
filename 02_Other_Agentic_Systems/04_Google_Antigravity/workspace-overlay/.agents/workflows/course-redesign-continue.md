---
description: Continue only the next lecturer-approved course-redesign stage while preserving gates, lineage, course isolation, and assessment security.
---

# Continue the active run

1. Read root `AGENTS.md` and `01_Control/state.json`; resolve `active_run_id`.
2. Use the `course-redesign-orchestrator` skill and only the recorded next
   permitted action.
3. Verify the current run contract, gate, conversation reference, context and
   plan versions, manifest fingerprint, source-policy version/fingerprint,
   permitted tools/actions/egress/audiences, and retry history.
4. Reject stale or mismatched specialist returns and approvals without merging
   findings. Never borrow authority from another run or stage.
5. Load the relevant specialist role contract. Use permitted bounded subagents
   only if available; otherwise preserve every role perspective serially.
6. Request review before terminal commands or writes. Create only exact targets
   authorised by the current gate and preserve protected-source hashes.
7. Stop at the next named gate with a truthful status, evidence, open risks, and
   exactly one next permitted action. Do not infer approval or continue
   automatically.
