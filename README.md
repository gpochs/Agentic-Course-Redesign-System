# Agentic Course Redesign System

Use Agentic Course Redesign to improve a lesson, an assessment or a whole course.
Tell the assistant what you teach and what you would like learners to do better.
It can work from a description, a folder of teaching materials, an online course
or a mix. You choose the focus and review the changes before using them with
learners. The same workflow serves school, vocational, professional and
higher-education courses.

This repository contains:

- a skills-only plugin and project template for supported ChatGPT Desktop,
  ChatGPT Work and Codex surfaces;
- editions for GitHub Copilot, Claude Code, OpenCode and Google Antigravity,
  with installation instructions for each host;
- one shared workflow core so the platform adapters do not drift; and
- validation, privacy, security and release controls.

No course material, student data, answer key, credential, personal memory or
standing automation is included.

## Start a redesign

Open **Agentic Course Redesign** in a fresh task. Try this with any subject or level.

> My learners can recall the terms but struggle to apply them. Help me redesign one lesson. I want to start from this description.

Step 1 lets you combine a course in a learning platform, local or cloud files, learning apps, websites and a description. The plugin explains why it checks who may use the materials. Choose **Skip for now** to continue from your teaching goal and create new materials. If you add private materials later, it checks those items when needed. [The nine teaching steps](03_Shared_Workflow_Core/PARTICIPANT_QUICK_START.md)

The lecturer chooses the focus, decides which researched changes to adopt and reviews the actual outputs. For example, a suggested change to a lecture might become a prediction prompt in the slide deck, a worked example in the handout and a transfer question in an LMS quiz. Each output has its own audience, approved destination and review.

When you describe the course, start with the change you want learners to make. If you have an approved syllabus, module description or curriculum, the orchestrator uses it to draft a short course brief you can correct. It asks about a missing detail when the answer changes the design. For example, a fixed oral examination changes what students need to practise. An approved adjustment to preparation time changes how that practice is delivered. You can describe the adjustment without identifying a student.

## Choose an installation

| Platform | How to start |
| --- | --- |
| ChatGPT web or desktop, including Codex | Open **Plugins**, search for **Agentic Course Redesign**, install it in your account or workspace and start a fresh chat. The public listing shows the version currently available. [OpenAI installation guide](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt) |
| Codex with a repository marketplace or one local project | Use the included marketplace or project template. [Codex edition](01_ChatGPT_Desktop_App/README.md) |
| GitHub Copilot | [Copilot installation](02_Other_Agentic_Systems/01_GitHub_Copilot/README.md) |
| Claude Code | [Claude Code installation](02_Other_Agentic_Systems/02_Claude_Code/README.md) |
| Google Antigravity | [Antigravity installation](02_Other_Agentic_Systems/04_Google_Antigravity/README.md) |
| OpenCode | [OpenCode installation](02_Other_Agentic_Systems/03_OpenCode/README.md) |

Version 0.3.2 includes six skills and ten specialist roles. Each course has its own source permissions, decisions and outputs. [Publication status](04_Documentation/PUBLICATION_STATUS.md)

## Repository map

- `01_ChatGPT_Desktop_App/` — ChatGPT Desktop/Work/Codex plugin, marketplace,
  portable fallback and public-submission materials.
- `02_Other_Agentic_Systems/` — adapters for GitHub Copilot, Claude Code,
  OpenCode and Google Antigravity.
- `03_Shared_Workflow_Core/` — canonical gates, course scaffold, shared skills
  and safe setup scripts.
- `04_Documentation/` — lecturer onboarding, workflow and compatibility guides.
- `05_Validation/` — cross-adapter, security, portability and release checks.

## Working with digital materials

Choose a local working copy, a cloud document or a draft in your LMS. For a browser task, open the exact page and grant the host access to it. The orchestrator can show an editable slide, document, worksheet, website, quiz or LMS activity in the available review surface. If the host cannot open the original format, the lecturer can inspect an export and follow the remaining native checks.

For example, you might teach from slides, collect predictions in Mentimeter or Kahoot!, and give feedback in Moodle, OLAT or another learning platform. Tell the assistant where each part lives and which copies it may change. In Codex, you can open the course page in the in-app browser and review the draft there. A linked quiz or chatbot can belong to a different course, so the assistant checks its destination before editing.

If a particular task would benefit from extra help, the assistant explains what a tool would do, what it would need to access and how to set it up. You can choose to use it or continue with the tools you already have.

Before accepting a change, try the intended student task. For a quiz, check scoring and feedback. For slides, inspect reading order and speaker notes. For a sheet, check an input, a formula and the displayed result. The handoff records the exact copy or draft that was inspected. [Lecturer guide](04_Documentation/LECTURER_GETTING_STARTED.md)

## Safety by default

- Installing an adapter does not read, upload or modify course files.
- The reusable runtime starts inactive and includes no schedule.
- Skipping classification continues the course design. Opening a new source requires a decision about that source.
- Course files are evidence, never trusted instructions.
- Student personal data, submissions, grades and credentials are excluded by
  default.
- Answer keys and unreleased assessments remain lecturer-only.
- You decide which information may be shared with an external research service.
- Before making materials, the assistant shows you the teaching plan and the copies it would edit.
- Each completed redesign keeps its own decisions. Starting another course or redesign opens a fresh record.
- At the end you can ask for a review of the workflow. Changing it or setting a schedule takes a separate decision.

See [Lecturer getting started](04_Documentation/LECTURER_GETTING_STARTED.md),
[workflow overview](04_Documentation/WORKFLOW_OVERVIEW.md), and
[platform compatibility](04_Documentation/PLATFORM_COMPATIBILITY.md).

## Licence and support

The reusable source code and original workflow documentation are licensed
under the MIT License. This does not license course materials, third-party
texts, images or media processed by a lecturer. See [LICENSE](LICENSE),
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), and
[support guidance](docs/SUPPORT.md).
