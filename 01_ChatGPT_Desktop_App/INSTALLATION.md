# Install and start a course

## Use the plugin across courses

On the ChatGPT desktop app, open **Plugins**, search for **Agentic Course Redesign**, inspect the publisher and displayed version, and choose **Install** or **Update**. Start a fresh Chat, Work or Codex conversation, type `@` and select the plugin. Choose the **Agentic Course Redesign** entry if the picker lists the six skills. Keep each course's teaching materials and decisions in its own project.

On ChatGPT web, open **Plugins** and check the same listing. When it offers installation, select it and start a fresh Chat or Work conversation. A listing marked **Desktop only** directs you to the desktop app. Browser control, local editors, rendering and hosted agents vary by surface and workspace. The orchestrator can still work from a teaching brief and show an inline draft when the required surface is unavailable. [OpenAI plugin support](https://learn.chatgpt.com/docs/plugins)

In Codex CLI, open `/plugins` to install or enable the entry, then start a new session. For local development, if `codex plugin marketplace add --help` lists support for local directories, add your checkout as a marketplace using `codex plugin marketplace add "<absolute path to the repository>"`. Select the repository marketplace and install the plugin from that source. Inspect the version and source when curated and local listings share a display name. [OpenAI installation guide](https://learn.chatgpt.com/docs/plugins)

## Work locally in one course

To make the six skills available only inside an existing Codex project, run `python install_project_skills.py --project "<project folder>"` from this directory. Review the file list, then repeat with `--apply`. This creates project-local skills under `.agents/skills` and keeps their scripts and assets beside them. If you installed 0.3.0 this way, preview the update with the same command plus `--upgrade`, then add `--apply` after reviewing it. Only byte-identical copies from the previous release qualify for replacement. The installer reports conflicting files before writing. Start a new Codex session in that project and select `$course-redesign-orchestrator`. [OpenAI project skill discovery](https://learn.chatgpt.com/docs/build-skills)

For a project-scoped Codex workflow, use the scaffold bundled with this adapter. From this directory, preview a new course with `python plugins/agentic-course-redesign/scripts/setup_course_project.py --target "<new course directory>"`. Inspect the preview and append `--apply` to create the project in the agreed location. Open the new project in Codex. Its instruction file and ten role definitions live in that project. The full six skills are available through the installed plugin. The platform guides describe existing folders and eligibility records. [Windows](PORTABLE_SETUP_WINDOWS.md) · [macOS](PORTABLE_SETUP_MACOS.md)

## Try the first interaction

Ask “Help me redesign a lesson on interpreting graphs.” Choose **Skip for now**. The next question should concern the learners or your goal. If you already described both, the orchestrator checks the next detail that would change its advice, such as how the work will be assessed. Approve a project target when you want durable files. You still review the brief, focus, recommendations, file plan and finished materials.

For existing material, describe its category first. Once handling is clear, select the exact document, link or course. For Moodle, OLAT or another LMS, open the intended course in the in-app browser and grant access to that tab if you choose. Review a draft and its learner view before publishing anything. Installation requires no API key.
