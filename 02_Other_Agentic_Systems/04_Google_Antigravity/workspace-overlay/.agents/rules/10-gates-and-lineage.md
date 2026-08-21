# Gates, lineage, and write authority

Use @../../01_Control/GATES.md together with @../../AGENTS.md.

- Read `01_Control/state.json` first and perform only the recorded next permitted
  action for the active run.
- `candidate_not_active` forbids autonomous runtime activation and every
  schedule. Installation and validation do not alter that status.
- Every gate record and specialist return must match the current run,
  run-contract ID/version, conversation reference, context version, plan
  version, source-manifest fingerprint, and source-policy version/fingerprint.
- Silence, enthusiasm, a token by itself, an earlier run, or approval for a
  different stage or target is not approval.
- Gate 2B can approve only the exact dated research dossier and handoff under
  `03_Research/YYYY-MM-DD_<run-id>/`.
- Only Gate 3 can approve typed exact material targets under
  `04_Working_Copies/` or `05_Approved/`.
- After every named artefact gate and QA check, require the current-lineage
  `DECLARE PRODUCTION COMPLETE` reply, then the separately completed matching
  `APPROVE PRODUCTION HANDOFF` reply with the repeated exact target. Reopen and
  verify the saved handoff before HITL 3.
- Only unconditional current-lineage HITL 3 acceptance permits the mandatory
  separate system-review offer. Conditional acceptance returns for correction
  and a fresh HITL 3 decision.
- Stop at every lecturer gate. Never create a second unlabeled approval pause or
  infer authority from a planned workflow step.
- The orchestrator alone may persist approved workflow metadata. Specialist
  roles remain read-only and return proposals.
