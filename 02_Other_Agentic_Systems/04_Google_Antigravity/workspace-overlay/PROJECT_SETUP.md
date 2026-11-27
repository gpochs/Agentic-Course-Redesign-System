# Your course project in Antigravity

Open this folder as a project and start a course conversation with `/course-redesign-start`. Use one project per course. A folder in OneDrive also syncs to the cloud.

## Start with your course

> My learners can describe a technique but struggle to choose when to use it. Help me revise one activity and try it from the learner’s perspective.

1. **Start with your course.** Describe what you want learners to do. Choose **Skip for now** to go straight from your description to design, drafting and review. The material check helps keep course and student information in the right place.
2. **Choose the materials we can use.** You can combine a course site such as Moodle or OLAT, Word or PowerPoint files, cloud slides or spreadsheets, learning apps such as Kahoot! or Mentimeter, and other resources. Select several, name your own, or continue with just your teaching goal. You decide which items may be opened and who can see the drafts.
3. **Check the course brief.** Correct what the plugin understood. Leave a question open if the answer is unclear. Use your own words when explaining your priorities or giving feedback.

Later you choose the focus, compare suggested changes, approve the plan and files, try each draft, and decide what to use. The plugin briefly introduces optional tools and recommends one when it would help with a particular task. It explains the benefit, access and any cost. You can approve that task or batch, ask for setup help, or use the built-in option. Student materials and teacher-only keys have separate destinations.

[Follow all nine teaching steps](https://github.com/gpochs/Agentic-Course-Redesign-System/blob/main/03_Shared_Workflow_Core/PARTICIPANT_QUICK_START.md).

You can ask to see a private course draft in the browser, share an authorised copy or start from a description. Keep original files separate. If an activity uses a shared quiz bank or workbook, check that the link belongs to the copy you approved. The learner draft and the teacher’s answer notes each need their own audience.

<details>
<summary>For maintainers handling course files and project settings</summary>

## Working with authorised existing materials

1. Invoke `/course-redesign-start` before disclosing any course source path,
   filename, or list. Declare only the material category and exact processing
   environment for Gate 0A.
2. Review and fingerprint Gate 0A. Personal/unmanaged processing is permitted
   only for privately owned/rightsholder-authorised or appropriately licensed/
   public material with explicit AI-processing authority; public availability
   alone is insufficient. Institution-internal/restricted material is route-
   only there, and mixed/uncertain material fails closed until segregated or
   clarified.
3. For an approved institutional environment, record the exact policy
   reference, approved scope, and non-expired expiry.
4. Only after Gate 0A permits processing, add current course files to
   `00_Source_Materials/` and relevant programme, learner, policy,
   accessibility, assessment, AI-tool, rights, and style context to
   `00_Context/`.
5. Keep student personal data, submissions, grades, credentials, and secrets
   out of the project in this workflow.
6. Ask the orchestrator to inventory the files and prepare Gate 0.
7. Review source classifications, teacher-only assessment boundaries,
   tool/egress permissions, output audiences, eligibility/manifest/policy
   fingerprints, and expiry where applicable.
8. Approve or revise Gate 0 before any specialist analysis.

## Important distinctions

- The source manifest proves file integrity; it does not grant access or egress.
- A course-material decision is not a system activation decision.
- After accepted HITL 3, silence on the system-review offer waits. An explicit
  request or decline closes the course run as terminal `complete_dormant`; it
  never resumes.
- One informational trigger-guidance offer registers nothing. A manual or
  separately authorised scheduled trigger creates a fresh run and lineage.
- A system activation decision is not schedule approval.
- Schedule approval registers an expiring contract but does not trigger an immediate run.
- Every scheduled recurrence creates a fresh run and waits at the configured human gate.

See the [project instructions](AGENTS.md) and [decision records](01_Control/GATES.md) for the implementation contract.

</details>
