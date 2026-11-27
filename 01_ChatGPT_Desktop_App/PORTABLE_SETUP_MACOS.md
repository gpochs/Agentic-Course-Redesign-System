# Portable setup on macOS

Use this route when the attendee's supported Work or Codex surface does not
expose the custom marketplace or plugin installation, or when workspace policy
blocks that route. Prerequisites are Python 3 and an authorised
personal-computer project that can use the copied `AGENTS.md` and `.codex/`
configuration. This
guide has been structurally reviewed, but the route has not yet been
independently executed on a macOS machine.

1. Extract the shared bundle to a short writable path, for example
   `~/CourseRedesignSystem`. Do not run it from inside the ZIP.
2. Create one isolated folder for one course on local storage or an authorised
   personal OneDrive, for example `~/Courses/Biology/Year2`. Never put unrelated
   courses in the same project. OneDrive is cloud-synchronised rather than
   strictly local; use it for protected or assessment data only when authorised.
   Exclude student personal data, submissions, grades, credentials and secrets
   by default.
3. In Terminal, preview the scaffold:

   `python3 ~/CourseRedesignSystem/plugins/agentic-course-redesign/scripts/setup_course_project.py --target ~/Courses/Biology/Year2`

4. Review every destination. If the target is correct and there are no
   conflicts, apply it:

   `python3 ~/CourseRedesignSystem/plugins/agentic-course-redesign/scripts/setup_course_project.py --target ~/Courses/Biology/Year2 --apply`

   If that exact target already contains unrelated files, do not apply by
   default. `--allow-nonempty` is conditional: use it only after the lecturer
   reviews the preview, confirms every existing top-level entry, and approves
   adding the scaffold to that exact folder. It does not permit overwriting;
   any existing template path still causes a hard failure. Existing targets
   also require the approved Gate-0A record through `--eligibility-record`;
   without it the helper does not enumerate target contents and refuses apply.

5. Open `~/Courses/Biology/Year2` as a separate Codex project. In Work mode,
   use the same folder and gates only when the current surface can access that
   authorised project/folder. This portable route does not install the six
   plugin skills. The copied
   `AGENTS.md`, `.codex/config.toml`, custom agent files, state template and
   folder guidance provide the portable workflow even without plugin install.
6. Start with **Help me redesign one lesson**. Choose **Skip for now** to work from a teaching goal. Keep going through the normal lecturer decisions to produce materials. For durable work, use the source-free record and empty manifest. If a private document or LMS becomes relevant, review its handling at that point.
7. If you choose **Use existing materials**, clarify authority, sensitivity and environment before disclosing their locations. Add only approved inputs to the source and context folders.
8. Review the generated manifest, classifications, policy, tool/egress rules
   and Gate 0 record. Do not paste approval tokens supplied by someone else.

The setup does not upload files, activate a runtime or create a schedule.
