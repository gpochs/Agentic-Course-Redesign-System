# Participant quick start

## Before opening Codex

1. Choose one course. Do not combine different courses in one project.
2. Create a short isolated folder for that course on the lecturer's personal
   computer. Use local storage or a lecturer-controlled personal OneDrive.
   OneDrive is cloud-synchronised, not strictly local; protected or assessment
   material may be stored there only when institutional and rights/data rules
   authorise it. Keep the lecturer's originals elsewhere; the workflow will
   create protected copies inside the project.
3. Gather the current materials: course plans, slides, workbooks, learning
   objectives, assessments and keys. Also gather relevant context: programme
   requirements, learner profile, accessibility guidance, grading policy,
   permitted tools, workload constraints and lecturer style examples.
4. Remove student personal data, submissions, grades, credentials and secrets,
   unless a separately authorised institutional workflow explicitly allows them.

The scaffold keeps that one course organised as follows:

- `00_Source_Materials/`: copied current course files;
- `00_Context/`: programme, learner, policy, assessment and style context;
- `01_Control/`: manifests, policies, approvals and state;
- `02_Working_Notes/`: run analysis and alignment records;
- `03_Research/`: approved dated research dossiers and handoffs;
- `04_Working_Copies/`: exact Gate-3-approved production targets;
- `05_Approved/`: lecturer-accepted releases;
- `06_QA_and_Review/`: independent checks; and
- `07_System_Improvement/`: separate reusable-system proposals.

Add only this course's materials. Do not bundle credentials, global activation,
standing schedules, personal memory or course data with the reusable system.

## In Work mode or Codex

1. Install the plugin from the configured custom marketplace in Work mode or
   Codex in the ChatGPT desktop app, then start a new chat. In Codex CLI, use
   `/plugins` and start a new session after installation. If the custom source
   is unavailable, use the portable setup guide instead.
2. Create or select a project for this one course and open/attach only its
   isolated local or authorised personal-OneDrive folder.
3. Start a new task and say: `Set up an agentic redesign project for this one course.`
4. Answer the setup questions conversationally. You do not need to prepare a
   long master prompt.
5. Review the proposed folder target before any scaffold is created.
6. Add current course files to `00_Source_Materials` and context files to
   `00_Context`.
7. Review the file list, hashes, source classifications, teacher-only boundary,
   tool/egress permissions and output audiences.
8. Approve Gate 0 only when those exact records are correct.

Current OpenAI documentation supports plugins in Work mode and Codex in the
ChatGPT desktop app. Workspace policy, account access, and app version can still
limit custom sources or installation. Plugins are not supported in the Codex
IDE extension. Expose only lecturer-authorised source classes; installation,
storage choice, or tool availability never grants source access or egress.

## What happens next

- Gate 1 agrees the course brief and run contract.
- Five specialists perform a preliminary scan.
- HITL 1 lets the lecturer choose the redesign focus areas.
- Specialists then research and reconcile concrete recommendations.
- HITL 2 is the detailed educational-consultant dialogue that decides changes;
  Gate 2B may save only its exact dated research dossier and handoff under
  `03_Research/`.
- Gate 3 approves the coherent blueprint and exact working/release material
  targets under `04_Working_Copies/` and `05_Approved/` before production.
- Independent QA checks pedagogy, assessment, facts, citations, accessibility,
  design, security and packaging.
- HITL 3 lets the lecturer accept the finished files or request bounded changes.
- Only after a successful run may the lecturer choose to validate improvements
  to the reusable system. Runtime activation and scheduling are later, separate
  decisions.

Installation alone never reads course files, uploads content, activates a
runtime or registers a schedule.
