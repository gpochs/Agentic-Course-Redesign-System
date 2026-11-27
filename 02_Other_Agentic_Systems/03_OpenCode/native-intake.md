# Redesign one lesson in OpenCode

Try this fictional lesson in a fresh OpenCode chat: “Use the course-redesign skill. We meet in class and practise in Moodle. I want students to judge which bus route is more reliable.” Expect one question at a time.

### Model choice for this course

Offer **Match models to tasks**, **Keep the current model** or **Choose at each step**. With matching, get one approval for the named tasks, roles, models, account and fallbacks. A single-model choice applies to the specialists too. If a preferred choice is unavailable, keep the approved capable model and offer a manual switch. Pause the affected check only when its result would be invalid. Give each specialist its capability needs and approved model entry in its brief. See the [model plan and ten role criteria](model-plan.md).

If a specialist identifies a concrete gap, inspect already installed skills before considering GitHub or Hugging Face. Review a candidate’s publisher, exact revision, scripts, licence, data and destinations. For separately approved project use, review `.opencode/skills/<name>/SKILL.md` and verify discovery in a fresh session. OpenCode’s executable plugins have a different access model. Give a read-only specialist only the tools and material allowed for that role. [OpenCode skills](https://opencode.ai/docs/skills/) · [OpenCode plugins](https://opencode.ai/docs/build/plugins/) Follow the [task-specific skill check](tool-fit.md).

Select the parent conversation model with `/models` or, for an authorised CLI session, `--model provider/model#variant`. Selecting a primary agent by ID leaves the session model as selected. Native custom-agent profiles accept `provider/model#variant`. The ten supplied profiles omit that field and inherit the parent. The documented `subagent` call takes the agent ID, description and prompt. Use an existing appropriately configured, approved specialist only if its permissions and role match. Otherwise, offer to switch the parent at a stage boundary and invoke the normal read-only specialist there. If the host cannot report the effective model or variant, label it unverified. Check the included sign-in route for the chosen provider. [OpenCode agents](https://opencode.ai/docs/agents#model) · [Subagent tool](https://opencode.ai/docs/tools/#subagent) · [Providers](https://opencode.ai/docs/providers)

**1. What would you like to work from?** Choose any that apply:

1. A learning platform (LMS), such as Moodle or OLAT
2. Local or cloud files
3. A learning app (H5P or Mentimeter)
4. Another source (a video, website or design example)
5. My description, alone or alongside materials
6. Skip for now
7. Other – type your answer

Use the card if it shows every choice, lets you select several and accepts a write-in answer. Otherwise reply to the same numbered list in chat: `1 + 2 + 3: Moodle, my slides and a Mentimeter poll.`

**Skip for now** or “I’ll describe them” takes you straight to question 3. No files or tabs are opened. You can still make and review both drafts below; return to question 2 only for an item you later want to open.

**2. Which materials may OpenCode read here?** Set the limits before sharing: “Read my slides in this project for my review. Leave the class responses in Moodle.” Editing or sharing needs separate permission.

In OpenCode Desktop, the **Files** panel helps locate the agreed project file. Keep any learner responses and the teacher-only answer key in their own restricted locations. Opening a file for yourself and attaching it as context give the agent different access. Offer a view when the current task calls for it. [OpenCode Desktop](https://opencode.ai/desktop)

**3. Does this capture your goal?** “Students choose a route and justify it using late trips out of total trips.” Correct the summary. If you haven’t given a goal, start with what learners should do better.

**4. Where do students need practice?** Pick a focus before OpenCode investigates: calculating a rate or explaining why it’s fairer when routes have different numbers of trips.

**5. Is the change worth two minutes?** Compare “Count the late trips” with “Vote in pairs and defend your choice.” Ask what supports the change and keep, adapt or decline it. If the wording is already in a tracked draft, the **Review** panel shows the changed lines and lets you comment on one. Open the rendered copy when the decision depends on what students see. [OpenCode Desktop](https://opencode.ai/desktop)

**Optional help:** A writing skill such as Humanizer could shorten the voting prompt. Ask where the text goes and whether the cost is included, extra or unknown. Choose **Use for this prompt**, **Help with setup** or **Edit here without it**. For [project-only setup](https://github.com/gpochs/Agentic-Course-Redesign-System/blob/main/02_Other_Agentic_Systems/03_OpenCode/README.md#install-the-native-skills-and-agents), review the skill folder before adding it under `.opencode/skills/`; check it appears in a fresh project chat.

**6. Shall we make these two files?** Approve the plan, the filenames below and the exact private draft folder first. Both copies are for your review before learners see them. Keep any answer key or marking notes in a separately approved teacher-only file.

**7. What happens when you try each draft?** For an approved learner-facing web worksheet, open its exact private preview in the desktop **built-in browser** beside the session. Try question 2 with the keyboard and check when feedback appears. If the desktop exposes browser controls to the agent, bind the trial to that tab and keep its tab ID for each action. If only you can see it, tell OpenCode what happened. Any extra HTML or PDF review copy needs an agreed filename, destination and audience in the plan. [OpenCode Desktop](https://opencode.ai/desktop) · [Browser tools](https://opencode.ai/docs/tools/#browser)

For the two saved Office drafts in this example, open each editable copy in its usual app.

- `Route-choice-v1.pptx`, slide 3: In PowerPoint’s slide show, can pairs vote before seeing the rates? “Keep the trip counts visible; reveal the percentages on the next click.”
- `Trip-rates-v1.xlsx`, sheet `Routes`: In Excel, enter 3 late trips in `B4` and 20 total in `C4`. Expect 15% in `D4`. Try two zeros: “Show ‘No trips’ in `D4` instead of an error.”

**For a course open in your signed-in Chrome or Edge**, the optional, paired **OpenCode Browse** extension can lend the existing tab. Agree on the course, unpublished activity, audience, allowed site and task, then use the extension’s toolbar button on that tab. Handle sign-in yourself. The desktop browser has its own profile. For an LMS tab already open there, verify that tab directly. Opening a local worksheet does not grant access to a Chrome or Edge tab. Immediately before editing, check the actual course, private copy and audience in the lent tab. Check that any linked quiz also opens its approved independent copy. Reopen the saved draft in learner preview and try one fictional response when the approved trial permits it. If submission is disabled, leave feedback timing untested. The teacher-only key stays out of learner tabs and captures. [OpenCode Browse](https://opencode.ai/product/browse)

In a terminal session or when the browser panel or extension is unavailable, link the exact working copy for the teacher to open, work from an approved export, or keep discussing the description. Identify which version was inspected, by whom, and which learner action remains untested.

For each planned file, choose the version, ask for a change or leave it out. For example, you can keep the slide and leave out the spreadsheet. The spreadsheet stays private, and the plan keeps its filename and your decision. A change to the slide calls for another trial of the updated version and a fresh decision. If you leave out both drafts, you can stop or revise one. There is nothing to hand over. Otherwise, once every file has a decision, confirm that the checked versions you chose are ready. In a separate reply, decide whether to save the handover document at the exact location shown. Check that it lists only those versions.

**8. Which version will you use?** Choose **Use**, **Request changes** or **Leave out** for each file in the handover. Reopen revisions at the same slide or cell and retry them.

**9. Finish here?** Stop or ask for a written suggestion for next time. Publishing is a separate decision.

**Step 10 · Would you like a second opinion?** After Step 9, **Skip** ends the review immediately. Choose **Prepare a review** for a copy-ready packet you can use yourself, or **Explore a different model** to compare suitable receiving models. The packet includes a progress list covering all nine teaching steps and the ones skipped. Select the saved versions you want reviewed in **Files**. A **Review** diff can help check a changed instruction. For a question about feedback timing, include only an approved learner draft the reviewer can actually try.

Ask which different model family fits this review. For example, if an OpenAI model created the worksheet, switching to the same model in another app would provide the same family. Check candidates against current format support and the account's model picker. OpenCode distinguishes a ChatGPT subscription from a provider API key. Use an already included account route and let the teacher choose or replace the model. [OpenCode providers](https://opencode.ai/docs/providers)

Look at the already included providers and models in this OpenCode account first. If a suitable unused family is available, prefer a fresh OpenCode conversation on that model with only the approved packet. If none fits here, offer a different signed-in app using separately approved computer control, or a manual handover. Check the families used across the whole run. If all eligible families contributed, identify the least-involved family, ideally different from the main author of this item. Disclose its earlier contribution and let the teacher choose a **limited second look** or finish. With one family, distinguish another model from an exact same-model self-check. Neither is an independent family review.

Before transfer, show the exact packet with Steps 1–9 and skips, selected filenames and versions, any original individually chosen, receiving app, account, model, audience and cost. Ask for separate final approval to **Send this packet**. Deliver to a fresh conversation with only the selected context. A separately authorised **OpenCode Browse** tab can reach a signed-in web app. For another desktop app, or if Browse is unavailable, give the teacher the copy-ready packet. The reviewer should cite each step and page, slide or item, version and evidence, and state what could not be verified. The teacher chooses whether to revise, keep or dismiss each finding. Reopen any revised draft and repeat the learner trial before accepting it. [OpenCode Browse](https://opencode.ai/product/browse)

Based on the [Codex teacher quick start](https://github.com/gpochs/Agentic-Course-Redesign-System/blob/main/03_Shared_Workflow_Core/PARTICIPANT_QUICK_START.md).

**Public browser check · 27 November 2026.** I opened the [public repository](https://github.com/gpochs/Agentic-Course-Redesign-System) with paired OpenCode Browse in a fresh read-only Edge tab restricted to `github.com`. The tab title was “gpochs/Agentic-Course-Redesign-System: A lecturer-in-the-loop, evidence-grounded workflow for course redesign across ChatGPT Desktop, Codex, Copilot, Claude Code, OpenCode, and Antigravity.” The page snapshot listed `01_ChatGPT_Desktop_App` as a directory under **Folders and files**. I then closed the tab.
