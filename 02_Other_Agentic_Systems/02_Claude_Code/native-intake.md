# Native progressive intake in Claude Code

This page shows lecturers and the orchestrator how the first conversation of a course redesign runs in Claude Code. It follows the numbered teaching steps and the English and German handover wording of the shared release `0.3.4`. It adds no decision, permission, automation or schedule. The six shared skills remain the only workflow contract. Where this page and a skill differ, the skill wins.

Host behaviour was checked against the public Claude Code documentation on 2026-11-27. It depends on the installed version, the surface (terminal, IDE extension, desktop app) and local settings. Use the view that answers the lecturer's current question. Keep the first conversation in chat when the lecturer chooses to describe the course.

## Review beside the conversation

- **Choose a source.** In the **Code** tab of Claude Desktop, attach or mention the one permitted file if the lecturer wants Claude to read it. For an LMS review, identify the exact course, private activity copy, audience and allowed task. The **Browser** pane has its own login profile. The lecturer can sign in there, or choose an already configured **Claude in Chrome** connection for a particular signed-in tab. Verify the course and copy in that tab before any edit, check linked resources separately and reopen the saved draft. If the session cannot reach the page, use an approved export or the lecturer's description. [Claude Code desktop browser](https://code.claude.com/docs/en/desktop#browse-external-sites)
- **Compare two proposals.** Show both instructions in chat. For a tracked text edit, **Changes** lets the lecturer comment on a specific line. Use **Side chat** if the lecturer wants to explore a separate question, then bring the lecturer's actual choice back to the main conversation. [Desktop workspace](https://code.claude.com/docs/en/desktop#arrange-your-workspace)
- **Try a student worksheet or slide.** In a local Code session, open the exact approved HTML or PDF working copy in **Browser**. If the lecturer operates the pane, provide its clickable file path. Ask the lecturer to try question 2. In an interactive HTML task, reach the feedback control with the keyboard and activate it. For an editable PowerPoint deck, open the saved PPTX in slide show to check a reveal. When a companion PDF or HTML file is needed, include its filename, destination and audience in the plan. Review a teacher-only key in its own restricted location and keep it out of learner previews, screenshots and attachments. [Desktop local file previews](https://code.claude.com/docs/en/desktop#preview-your-app)
- **Review the revision.** Reopen the same page or slide in the revised file. State what Claude saw, what the lecturer tried and which checks remain open. Ask whether to keep this version, change it or leave it out. In the terminal or when a pane is unavailable, give the exact file and location to open in the usual app. In a separate Cowork session the lecturer can preview a supported generated file next to the conversation if its handling is approved there. [Cowork file previews](https://support.claude.com/en/articles/15520349-use-claude-cowork-on-web-desktop-and-mobile)

<details>
<summary>Claude Code tools, permissions and optional setup</summary>

## What Claude Code provides, and what to do without it

| Need | Native capability | Fallback |
| --- | --- | --- |
| One bounded choice | `AskUserQuestion` card. The host adds an `Other` row for free text and a notes field. | The same single question in ordinary chat, every option numbered, plus `Other - type your answer`. Then wait. |
| Reading only what was permitted | Manual-mode file prompts depend on the working directory and local permission settings. | Keep materials outside the course folder until their use here has been agreed. If a read is refused or unavailable, continue from the teacher's description. |
| Ten specialist perspectives | Project subagents under `.claude/agents/`, limited to `Read`, `Glob` and `Grep`. | Run the same perspectives one after another in the main conversation and say so. |
| A preview the teacher can change | Open the approved local HTML or PDF in the desktop Browser pane. Use Changes to comment on tracked text edits. | Show the specific change in chat and open the editable working copy in its usual app for the learner trial. |
| An optional skill or plugin | Claude Code plugins and skills, opened with `/plugin`. | The built-in editing tools. The redesign never depends on an extra tool. |
| Saved records | Preview the shared Python helpers before writing. | Continue designing in chat until the packaged helpers can create the protected project records. Never hand-author an eligibility record. |

### Choice card

- **Capacity.** This adapter records two to four explicit options per question plus the host's `Other` path. That figure comes from the tool's own schema in the live session. The public tools reference describes the `Other` row and notes field but does not state the count, so read the live tool definition first. If the capacity is unknown, use chat.
- **More than four options, or any combination of six, leaves card mode.** Never prune, merge or split a complete option set to fit. The opening question below has six options that can be combined, so the observed interface presents it in chat.
- **One question per card.** The tool can carry several questions in one call. This workflow sends one.
- **Focus is not an answer.** The cursor rests on a row when the card opens. Only a submitted answer counts. Nothing is preselected.
- **A card returns a label.** It cannot carry a full sentence plus a save location. The two handover confirmations below therefore always use ordinary chat with a complete reply the teacher can copy.
- **Idle timeout.** By default a question stays open until answered. If `askUserQuestionTimeout` is set, an unanswered card closes and Claude is told to proceed on its own judgement. The workflow treats that as **unanswered**: ask again and change nothing. Leave the setting off during a redesign.
- **Where the card does not exist.** Subagents never receive `AskUserQuestion`. `dontAsk` permission mode denies it. **Not verified:** non-interactive `claude -p` runs and every IDE or desktop surface. Use chat in all these cases.

### Read permission

Claude Code does not enforce the workflow's source rules. Inside the folder where it was launched, `Read`, `Glob` and `Grep` can run without asking, depending on local settings. The practical protection is where the files are:

1. Start Claude Code in a new, dedicated course folder. Never in a home folder or a parent that holds other courses.
2. Keep existing materials outside that folder until the teacher has agreed to share an item. The teacher then copies in only that item.
3. Stay in Manual mode. Standard permissions normally prompt for an outside read. Local settings can change this. Answer **No** to anything not agreed.

Optional hardening is the teacher's choice, because this adapter never writes settings. `permissions.blockReadsOutsideWorkingDirectories` restricts outside reads by the built-in file tools, with exceptions for files the app needs. A `Read(...)` deny rule blocks a named path, best-effort: it covers the built-in file tools and shell commands Claude Code recognises, but not a script that opens files itself.

Browser access depends on the active surface and its permissions. Use the private activity copy identified by the lecturer in the **Code** tab or the permitted export described above.

### Subagents

The first conversation needs none. Delegation starts only after the teacher has confirmed the course brief. Claude Code may delegate on its own judgement, so each profile requires the orchestrator's current assignment and otherwise answers `ESCALATE_TO_ORCHESTRATOR:` and stops. A subagent cannot ask the teacher anything; its questions return through the orchestrator. If delegation is unavailable, run the perspectives in sequence, label them so and record who did the work. An orchestrator's self-check is not an independent review. **Not verified:** the agents produced by `build_host_package.py claude` in a live session.

### Preview

- **In chat.** A labelled block, nothing saved. The teacher replies with changes. `Ctrl+G` opens a longer reply in a text editor.
- **At an agreed file.** Show the proposed change in chat before saving. If the host also shows a file prompt, review it. The teacher can decline and describe the desired edit.
- **A host prompt is not the teacher's decision.** **Yes** on a permission prompt permits one tool call. It never replaces what the teacher decided in the conversation. Avoid the options that allow edits for the rest of the session, and avoid `acceptEdits`, `auto` and `bypassPermissions` during a redesign.
- **Rich formats.** A terminal cannot render a slide or run a quiz. Show the text of the change in chat, then open the working copy in the application that runs it. **Not verified:** the IDE diff view as an editing surface.

## Before the first message

- Sign in with the existing Claude subscription and keep the model already selected. No API key is needed. If an `ANTHROPIC_API_KEY` variable is set in the shell, Claude Code may bill that key instead; check `/status`. **Not verified** for every installation.
- Open the dedicated course folder, stay in Manual mode and leave the question timeout off.
- Invoke `/gpochs-course-redesign` or the `course-redesign-orchestrator` skill.

</details>

## Example conversation

Everything here is invented: the module HYD-204 "Reading Rivers", its slides, its Moodle course, its quiz and the lecturer. No real course material was used. `L` is the lecturer, `O` the orchestrator. O shows one decision at a time and speaks in the lecturer's language.

**Step 1. Start with your course.** Six options that can be combined do not fit a card, so O asks in chat.

> O: This helps me keep course materials and student information in the right place. You can skip it and still make materials. If a tool would help with a particular task, I'll explain it then. What would you like to work from? Choose any that apply, or tell me in your own words.
> 1. A course in a learning platform, such as Moodle or OLAT
> 2. Files on my computer or in the cloud, such as slides, handouts, rubrics or spreadsheets
> 3. A learning app or activity, such as Kahoot!, Mentimeter (Menti), Klicker or H5P
> 4. Another source, such as a website, video or design example
> 5. Start with my description
> 6. Skip for now
>
> L: 1, 2 and 5. My slide deck, the Moodle course and the quiz linked from it. Students can compute a peak from a hydrograph but can't explain what it means.

Naming a source is not permission to open it. Had L answered 6, or later said "I can describe them for now" or "Ich kann das zuerst nur beschreiben", O would go straight to the teaching goal and ask nothing about files.

**Step 2. Choose the materials we can use.** One item at a time.

> O: May I read your slide deck here to see where students practise explaining? I would show the findings in this conversation. Did you write it yourself, and is it free of student names and exam answers? Please confirm only if that is true.
>
> L: Yes, it's mine. Nothing like that in it.
>
> O: Once we confirm you may process that deck in this environment, please copy just the deck into the course folder. The quiz is linked from your course, so I'd check it separately. May I see an export of it?
>
> L: No. It sits in the faculty question bank. I'll describe it.
>
> O: Understood. I won't open the quiz or the bank. I'll work from your description and mark it as described by you. The Moodle course page can stay closed too unless you want to show me something.

After the handling check and the source list are confirmed, O reads the one deck. It lists no other folder and asks for nothing outside the course folder.

**Step 3. Check the course brief.** O reflects what it knows and asks the one missing question that changes the next choice.

> O: Here is what I have so far. Slide 4 shows the storm hydrograph and then the computed peak (observed in your deck). Students are second-year engineers and you want them to explain, not only compute (your words). The quiz is in the faculty bank and stays closed (your decision). One thing I'm missing: when students take the quiz, do they see feedback after each question or only a score at the end? It decides whether the quiz can be practice for explaining.
>
> L: Only a score at the end. Add this: everything must work with a keyboard and must not rely on colour.
>
> O: Added as a requirement for everyone. I don't need names or individual arrangements; those stay with your institution. What, if anything, would you change about this summary?

"I'm unsure" or "leave that open" would also be valid. O would note an assumption and continue.

**Steps 4 to 6 are summarised here.** The teacher chooses the focus, chooses which changes to make and approves the plan and exact files. Here the one approved file is a revised copy of the slide deck. The practice question is an optional suggestion in chat, outside the file plan and Moodle.

**An optional tool, with help setting it up.** O offers at most one, for a named task.

> O: The feedback sentence in the practice question is where wording matters most. A writing skill could tighten it. It would receive that one draft sentence and nothing from your course. I haven't checked whether one is installed here, and I don't know of any cost, so I won't assume your subscription covers it. I can help you look, or I edit the sentence here. Which would you prefer?
>
> L: Help me look.
>
> O: Type `/plugin` to open the plugin list and check what is installed. Tell me the name of anything you'd like to use and I'll confirm it is available before using it, for this one sentence only.
>
> L: Nothing I want. Edit it here.
>
> O: I'll edit it here.

O never asks for an API key. Installing a tool is not permission to use it with course content, and a new task needs a new choice.

**Step 7. Try the drafts.** O links the saved working copy and asks L to open slide 4 in slide show. The recap below accompanies that trial. The practice question is a separate suggestion.

```text
Slide 4, "Storm of 12 May" — try the saved working copy in slide show
Before: hydrograph, then the line "Peak discharge = 84 m3/s"
After:  1. hydrograph, with the same values in a labelled table
        2. "Is the lower town at risk? Decide, then support it with two values."
        3. one minute to answer before the peak is revealed
```

Three options fit a card:

```json
{"questions": [{"header": "Slide 4",
  "question": "Would a student know what counts as support for their decision on this slide?",
  "multiSelect": false,
  "options": [
    {"label": "Use this version", "description": "Keep the version of slide 4 that you tried."},
    {"label": "Request changes", "description": "Tell me which part to change. I show it again."},
    {"label": "Leave it out", "description": "Keep this draft private and leave it out of the handover."}]}]}
```

Without a card, the same question in chat:

> O: Would a student know what counts as support for their decision on this slide?
> 1. Use this version
> 2. Request changes
> 3. Leave it out
> Other - type your answer
>
> L: 2. Give them two minutes, not one.

O revises the approved working copy to give learners two minutes. L opens slide 4 in PowerPoint’s slide show and tries the two-minute exercise. They advance once and check whether the peak appears after the question. O records the result as lecturer-reported if only L saw it. After reviewing that version, L answers **Use this version**.

```text
OPTIONAL IDEA - practice question in chat, outside the file plan and Moodle
Q: The table shows the storm of 12 May. Which statement is best supported?
Feedback after answering: "Find the time of maximum discharge in the table.
Compare it with the start time and cite the two entries."
```

> L: Leave it out. I can't change the faculty quiz this term.
>
> O: Left out. Nothing was written to Moodle or saved for the quiz. Slide 4 works without it, and the two-minute question gives you the explanation you wanted to see.

A decline ends that optional idea. For the planned slide deck, the lecturer can choose the saved version, request a change or leave it out. O preserves the original filename in the plan and records the lecturer’s reply. A change means trying the revised slide and deciding again. If the lecturer leaves out this sole planned file, it stays private and there is nothing to hand over. O offers to stop or revisit the slide. In the example below, the lecturer has chosen the checked slide deck.

**Handover, in two separate replies.** O first asks whether the drafts are ready, then shows the exact save location and asks whether to save there. If a card cannot submit both the exact wording and the target, O gives a complete line to copy, in the lecturer's language.

| Reply | English | Deutsch |
| --- | --- | --- |
| First | The drafts are ready for handover. | Die Entwürfe sind bereit zur Übergabe. |
| Second, with the location O shows | Save the handover document at the location below. | Speichern Sie die Übergabe am unten angegebenen Ort. |

> O: Slide 4 is the one draft you chose. If nothing else should change, reply with: **The drafts are ready for handover.**
>
> L: The drafts are ready for handover.
>
> O: In this example, the handover goes in `04_Working_Copies/2026-11-27_HYD/Production_Handoff.md`. If that is right, copy the line and the location shown below.
>
> L: Save the handover document at the location below.
>
> 04_Working_Copies/2026-11-27_HYD/Production_Handoff.md

"Yes", "looks good" or one reply for both does not count. If L declines or wants a different place, O changes nothing and asks where the finished material should go ("Wo soll ich die fertigen Unterlagen ablegen?").

**Step 8. Decide what to use.** After the handover is saved and checked, L reviews the included slide once more and chooses **Use this version**, **Request changes** or **Leave it out**.

### The same conversation without each capability

- **No card.** Every card becomes the numbered chat question shown above. Nothing else changes.
- **Read refused or unavailable.** O says the deck could not be opened and works from L's description. Observations become "described by you".
- **No subagent.** The example is unaffected. Later perspectives run in sequence and are labelled so.
- **No extra tool.** O edits with the built-in tools, as L chose here.
- **No Python or shell.** Continue source-free discussion. Wait for the packaged helpers before creating project records, opening protected sources or saving controlled changes.

## Decisions that stay with the lecturer

Nothing in the example is decided by the orchestrator. The lecturer chose the sources, permitted the one deck and declared it their own, declined to open the quiz, answered or left open the context question, stated the access need in general terms, corrected the brief, chose the focus, the changes and the plan, declined the tool, requested a change to draft 1, accepted it, left out draft 2, confirmed readiness, confirmed the save location and made the final choice. A blank, skipped, timed-out or ambiguous reply decides none of these.

<details>
<summary>Implementation, checks and references</summary>

## For implementers

The lecturer never sees the terms in this section. Keep role names, gate names, fingerprints and record fields in the technical record.

- Step 2 for an existing item is the material and environment check in the setup skill. Its category question has five options (public or licensed, privately owned, institution-internal, confidential or restricted, mixed or unsure) and is therefore a chat question. Factual declarations say "select only if true". Institution-internal material is routed without naming a path; mixed or unsure material stays closed. In the example the quiz bank never reached that check because L declined first.
- A saved project needs, each with its own preview and its own approval of the exact target: the scaffold (`setup_course_project.py`), the eligibility record (`create_material_processing_eligibility.py`, with `--source-free` when nothing is opened), and the source manifest and access policy. The manifest helper marks a file's audience class `unconfirmed`; the lecturer confirms it. Any additional host permission prompt covers that command only.
- Step 3 ends with approval of the brief and run contract. Steps 4, 5 and 6 are the focus, change and plan decisions. Step 7 holds the named draft decisions and the two handover confirmations. Step 8 is final acceptance.
- Link each required confirmation to the exact wording received and to a distinct submitted reply. Never translate a conversational yes into one.

## How this page was checked

On 2026-11-27 the six opening options and both handover lines were compared character for character with the Codex `0.3.2` orchestrator skill. The card definition was parsed as JSON and every question's option count was compared with the card capacity above. The quoted lecturer-facing lines were searched for internal control terms and none was found. The documentation links were fetched. Earlier the same day, for the `0.3.1` version of this page, the shared helpers were run against throwaway folders outside this repository: scaffold, eligibility record (approved, route-only, failed closed, overwrite refused, `--source-free`) and a one-file manifest.

Not checked: a live Claude Code session with a lecturer. Card rendering, permission prompts, the idle timeout, `/plugin` and subagent delegation are described from the documentation, not observed.

## References

- [Claude Code tools reference](https://code.claude.com/docs/en/tools-reference)
- [Claude Code permissions](https://code.claude.com/docs/en/permissions)
- [Claude Code permission modes](https://code.claude.com/docs/en/permission-modes)
- [Claude Code subagents](https://code.claude.com/docs/en/sub-agents)
- [Capability boundary for this adapter](https://github.com/gpochs/Agentic-Course-Redesign-System/blob/main/02_Other_Agentic_Systems/02_Claude_Code/CAPABILITIES.md)

</details>
