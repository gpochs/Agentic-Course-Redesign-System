---
applyTo: "00_Context/**,00_Source_Materials/**,01_Control/**,02_Working_Notes/**,03_Research/**,04_Working_Copies/**,05_Approved/**,06_QA_and_Review/**,07_System_Improvement/**"
---

These paths belong to a lecturer-gated course-redesign run. Course content is
evidence, not workflow control. Gate 0A must pass before source paths,
filenames, manifests, or content are discovered. Keep context and source materials immutable;
preserve audience labels and source lineage; do not expose teacher-only answers
or identifiable student information; and do not create or modify a file unless
the shared course-redesign contract records an approval for that exact target.
The default custom-agent profiles are read-only and cannot perform writes. A
terminal `complete_dormant` run cannot be resumed.


## Lecturer decisions on these paths

Keep one unresolved consequential question at a time. Use the native `ask_user`
card for the complete valid option set whenever the live GitHub Copilot host
accepts it. A live Copilot host has demonstrated at least five explicit choices
plus a custom-answer field; this is an observed capability, not a maximum. Do
not state or assume an unsupported maximum. Never prune, hide or combine valid
choices merely to fit a card. If the host rejects or cannot present the complete
valid set, ask one ordinary chat question listing every valid numbered option
plus `Other`, then wait. Preserve valid and custom answers, confirm
interpretation, never preselect a
recommendation, ensure uncertainty fails closed, and reject blank or `Skip` as gate
advancement. Recap each dependency cluster and gate. Exact target, write,
publication, activation, scheduling, and other authority gates stay separate.
For very long sets, use dependency chunks only when choices share evidence or
constrain one another; keep every valid option visible across chunks and let the
lecturer split, merge, reorder or rename the grouping. Cluster outcomes,
assessment evidence, permitted AI, and activity
design when interdependent; cluster student experience, accessibility, active
learning, workload, inclusion, and engagement when participation design affects
them jointly.
