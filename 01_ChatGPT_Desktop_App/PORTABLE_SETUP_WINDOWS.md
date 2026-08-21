# Portable setup on Windows

Use this route when the attendee's supported Work or Codex surface does not
expose the custom marketplace or plugin installation, or when workspace policy
blocks that route. Prerequisites are Python 3 and an authorised
personal-computer project that can use the copied `AGENTS.md` and `.codex/`
configuration. This
route has been structurally and functionally tested on the Windows development
machine; attendee app capabilities can still vary.

1. Extract the shared bundle to a short writable path, for example
   `C:\CourseProjects\Tools\AgenticCourseRedesign`. Do not run it from inside the ZIP.
2. Create one short isolated folder for one course on local storage or an
   authorised personal OneDrive, for example
   `C:\CourseProjects\Biology\Year2`. Never put unrelated courses in the same project.
   OneDrive is cloud-synchronised rather than strictly local; use it for
   protected or assessment data only when authorised. Exclude student personal
   data, submissions, grades, credentials and secrets by default.
3. In PowerShell, preview the scaffold:

   `python C:\CourseProjects\Tools\AgenticCourseRedesign\plugins\agentic-course-redesign\scripts\setup_course_project.py --target C:\CourseProjects\Biology\Year2`

4. Review every reported destination. If the target is correct and there are
   no conflicts, apply it:

   `python C:\CourseProjects\Tools\AgenticCourseRedesign\plugins\agentic-course-redesign\scripts\setup_course_project.py --target C:\CourseProjects\Biology\Year2 --apply`

   If that exact target already contains unrelated files, do not apply by
   default. `--allow-nonempty` is conditional: use it only after the lecturer
   reviews the preview, confirms every existing top-level entry, and approves
   adding the scaffold to that exact folder. It does not permit overwriting;
   any existing template path still causes a hard failure. Existing targets
   also require the approved Gate-0A record through `--eligibility-record`;
   without it the helper does not enumerate target contents and refuses apply.

5. Open `C:\CourseProjects\Biology\Year2` as a separate Codex project. In Work
   mode, use the same folder and gates only when the current surface can access
   that authorised project/folder. This portable route does not install the six
   plugin skills. The copied
   `AGENTS.md`, `.codex/config.toml`, custom agent files, state template and
   folder guidance provide the portable workflow even without plugin install.
6. Start a task with: `Set up the gated agentic redesign workflow for this one course. Before asking for any source path or filename, complete Gate 0A from the material category, sensitivity and assessment-security classifications and authority, and exact processing environment only.` Public accessibility alone is insufficient; personal/unmanaged processing requires privately owned/rightsholder-authorised or appropriately licensed/public material with explicit AI-processing authority and no internal or student-personal data. Route internal, student-data and unauthorised protected-assessment material without path leakage and fail closed on mixed/uncertain classifications.
7. Only after Gate 0A permits processing, copy current course materials into
   `00_Source_Materials`; put programme, learner, accessibility, assessment and
   style context in `00_Context`.
8. Review the generated manifest, classifications, policy, tool/egress rules
   and Gate 0 record. Do not paste approval tokens supplied by someone else.

The setup does not upload files, activate a runtime or create a schedule.
