# Agentic Course Redesign in your teaching apps

Choose the edition for the app you already use. Install it **for your account** to use it across projects, or **for one course** to make it available only in that project. Each course has its own materials, decisions and drafts. Both installation choices can use your existing subscription and an included model.

| App | Across your projects | For one course |
| --- | --- | --- |
| GitHub Copilot | [Install the repository marketplace plugin](01_GitHub_Copilot/PARTICIPANT_INSTALLATION.md#install-for-your-account) | [Add the project skill and specialist agents](01_GitHub_Copilot/PARTICIPANT_INSTALLATION.md#install-for-one-project) |
| Claude Code | Install the plugin in your personal skills directory, then open your course project. | Install it inside the project’s Claude skills directory. [Claude Code instructions](02_Claude_Code/README.md) |
| Google Antigravity | Install the native plugin in your user plugins directory. | Add it to the chosen project’s plugins directory. [Antigravity instructions](04_Google_Antigravity/README.md) |
| OpenCode | Add the course-redesign skill and specialist agents to your OpenCode configuration. | Add them to the chosen project’s OpenCode directory. [OpenCode instructions](03_OpenCode/README.md) |

For Codex, use the [ChatGPT Desktop edition](../01_ChatGPT_Desktop_App/README.md).

## Start with one teaching goal

> My learners can follow a worked example, but they struggle to decide which method to use on their own. Help me revise one lesson.

1. **Start with your course.** Choose any combination of a course site such as Moodle or OLAT, files on your computer or in the cloud, a learning app such as Kahoot! or Mentimeter, and other resources. You can name your own tools, work from your description alone, or choose **Skip for now**. The short material check helps keep course and student information in the right place. Skipping still lets you produce and review new drafts.
2. **Choose the materials we can use.** You decide which item may be opened, what the assistant may do with it and who can see the result. For example, if slides are cleared for use but permission for a linked quiz bank is unclear, leave the bank closed and work with the slides or your description. If materials with different permissions cannot be separated, defer that collection and continue the rest. When using an online course, approve the intended copy and check the destination of any linked resource before editing.
3. **Check the course brief.** Correct the assistant’s summary of the learners, goals and constraints. Then choose what to focus on, consider the proposed changes, review the plan, try the drafts and decide what to use. Student handouts and teacher-only answer notes have separate destinations. [Walk through all nine teaching steps](../03_Shared_Workflow_Core/PARTICIPANT_QUICK_START.md).

When several options can apply, you can pick a combination or explain it in your own words. The assistant uses a choice card if it fits and chat for teaching priorities or feedback. It may recommend an optional tool for a particular task, such as revising instructions across three worksheets. You see what the tool would add, what material it would receive, any known cost and how to set it up. Approve that named task or batch, ask for help, or continue with the built-in option. Live editing and previews depend on the app, your sign-in and the course permissions. A local draft or an authorised export gives you another way to review the work.

<details>
<summary>Implementation and validation for maintainers</summary>

The four editions share six workflow skills and ten specialist roles. The [native package builder](build_host_package.py) creates a new directory for the selected host. The [portable project overlay](00_Portable_Core_Adapter/README.md) remains available for projects that use the older layout. The platform guides above describe supported install paths, host-specific discovery and manual overlays.

From this directory, check the portable, Claude Code and OpenCode adapter records.

```text
python 00_Portable_Core_Adapter/validation/validate_adapters.py
```

The [Copilot validation guide](01_GitHub_Copilot/README.md#validation) and [Antigravity validation guide](04_Google_Antigravity/README.md#local-validation) cover their native packages. These checks verify package structure, recorded hashes and declared permissions. A live learner-view test requires an appropriate app and an authorised draft.

</details>
