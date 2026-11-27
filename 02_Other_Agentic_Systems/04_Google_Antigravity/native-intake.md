# Redesign a course in Google Antigravity

Use this guide with Agentic Course Redesign 0.3.4. Start with the teaching problem you want to solve. For example, “My learners read the chart correctly, but they jump from a difference to a claim about its cause.” The worked example below follows that problem through a revised activity.

## Model choice for this course

Offer **Match models to tasks**, **Keep the current model** or **Choose at each step**. With matching, get one approval for the named tasks, roles, models, account and fallbacks. A single-model choice applies to the specialists too. If a preferred choice is unavailable, keep the approved capable model and offer a manual switch. Pause the affected check only when its result would be invalid. Give each specialist its capability needs and approved model entry in its brief. See the [model plan and ten role criteria](model-plan.md).

For example, a materials or accessibility specialist may identify one format check missing from the installed tools. Search GitHub or Hugging Face only when it would address that gap. Inspect the publisher, revision, scripts, permissions, licence and destination. For separately approved project use, review a workspace skill under `.agents/skills/<name>/SKILL.md` and confirm it in Customizations. Hooks and MCP servers have their own access implications. The read-only specialist proposes the tool and the teacher decides. [Antigravity agent skills](https://antigravity.google/docs/skills) Follow the [task-specific skill check](tool-fit.md).

Use the model picker below the conversation or `/model` in the CLI for the main agent. A model change during an active turn applies after that turn finishes. In print mode, `--model` selects a named supported model and thinking level. Antigravity custom specialists declare a tier (`inherit`, `flash` or `pro`). All ten supplied profiles use `inherit`. For an exact approved model, first select it for the parent turn, then delegate the bounded role. Use a supported tier only when the plan permits that tier and the effective model can be identified as required. Offer a manual picker switch if a named per-role dispatch is unavailable. The separate Orchestrator planner/executor feature has its own account and model limits. [Antigravity model selection](https://antigravity.google/docs/models) · [Custom subagents](https://antigravity.google/docs/subagents)

## Your nine teaching steps

1. **Start with your course.** Antigravity can ask, “What would you like to work from?” or “Womit möchten Sie beginnen?” Choose any mix of a learning platform such as Moodle or OLAT, files on your computer or in the cloud, a learning app such as Kahoot!, Mentimeter, Klicker or H5P, and other sources. You can type your own combination, choose **Start with my description**, or **Skip for now**. The check helps keep course and student information in the right place. Skipping still lets you make and review new materials.
2. **Choose the materials we can use.** Name which items may be opened, who may see them and where private drafts may be edited. Your most recent instructions apply. If you name a slide deck, an LMS and a quiz, then say “I can describe them for now” or “Ich kann das zuerst nur beschreiben”, those items stay closed. If you later request a real file or site, settle its handling at that point and keep working on everything else.
3. **Check the course brief.** Correct a two- or three-line summary of your learners, outcomes and constraints. The assistant reuses information from a syllabus only when you have agreed it can be read. It asks one open question when the answer would change the design. “I’m unsure” and “leave that open” are valid. If accessibility matters, describe a requirement such as “the task must work using a keyboard”. Keep names, diagnoses and individual accommodation decisions private.
4. **Choose what to focus on.** See where learners practise the intended skill and what the assessment asks them to do. The assistant asks, “Where would a change make the biggest difference for your learners?” You can keep your current approach, adjust a suggested focus or propose a different one.
5. **Choose which changes to make.** Compare a concrete before-and-after example, the evidence for it, the effort and the trade-offs. Keep one idea, adapt another and leave out the rest. Correct the assistant’s recap before moving on.
6. **Review the plan and files.** Check the activity sequence, any design elements to preserve, who can see each draft and where it will be saved. Review copies of linked resources as well. A copied page can still point to a shared question bank, a master workbook or an answer key. To edit a linked resource, approve a separate copy and update the link in the draft. Keep teacher-only keys separate. Choose **Use this plan**, **Change the plan**, **Leave it for now**, or explain your own choice.
7. **Try the drafts.** Open each item in its intended view, try a learner action and ask which checks were actually performed. A file preview, keyboard test and live learner submission are different checks. If one is unavailable, review the editable copy and see the remaining check. Review the named drafts and teacher-only material separately. Choose, revise or leave out each item. Once all items have a decision and at least one checked version is ready, confirm the drafts to hand over and then approve the save location in a separate reply.
8. **Decide what to use.** See the finished items and any limitations. Choose **Use this version**, **Request changes**, **Leave it out**, or explain what you would change. Ask to inspect the revised item before making your decision.
9. **Finish or suggest an improvement.** Choose **Finish here**, **Write a suggestion**, or reply in your own words. A suggestion covers how the redesign process could improve, its benefits, risks and how a change could be undone. It only permits the review and suggestion. Installing, publishing or scheduling work needs a separate decision.

Antigravity can show a choice card when the current app supports all valid answers, their combinations where appropriate, and a custom reply. Otherwise you get the same choice in ordinary chat. Explain priorities and feedback in your own words. A suggestion counts only when you select it.

An optional tool is offered when it would improve a specific task. The assistant explains the benefit, minimum access, information sent, cost if known and built-in alternative. You can approve that task or batch, ask how to set up the tool, or decline and continue. Having a tool available does not approve access. Check that a model and service are covered by your signed-in subscription before using them.

## Review in the Antigravity App side panel

Suggest one view when it helps the teacher with the current step. For a description-only start, stay in the conversation.

- **Select source material.** In the side panel, **Open File** locates the named local file. Use **Documents** in the Overview panel to return to an agreed PDF, Office file or Google Workspace link already in the conversation. Confirm the item, audience and permitted action before attaching material or opening a linked object. [Side panel and Overview panel](https://antigravity.google/docs/side-panel)
- **Discuss a proposal.** Open an existing implementation plan or walkthrough from **Artifacts**. Ask the teacher to comment on the passage they want changed. Bring their decision about the proposed teaching change back to the conversation. [Antigravity artifacts](https://antigravity.google/docs/artifacts)
- **Try a learner activity.** Open the approved activity URL in **New Tab → Browser**, or use **Open File** for the exact approved worksheet PDF. For the slide below, open its approved learner-only HTML preview and press Tab, then Enter on the reveal. For a worksheet PDF, inspect page 2 at teaching size and point to the prompt whose wording needs work. Show the editable working copy alongside an approved companion preview when needed. Review the teacher’s scoring guide separately in its restricted location. [Browser use](https://antigravity.google/docs/browser) · [Built-in PDF viewer](https://antigravity.google/docs/cli-features)
- **Review a private LMS copy.** The built-in browser has its own sign-ins. Let the teacher handle sign-in. Verify the actual course, unpublished copy, audience and independently copied linked activity before any edit. The teacher can operate the manual browser tab. Where available, the built-in browser agent can try the agreed learner action. On supported CLI, IDE and business-account surfaces, the optional `/browser` route uses Chrome. Use only the route approved for that tab. If access is unavailable, use a permitted export or the teacher’s account of what they see. [Browser availability and sign-in](https://antigravity.google/docs/browser)
- **Check a change together.** Reopen the saved version at the same question, slide or page and try the action again. If only the teacher saw it, identify the result as teacher-reported. Ask whether to keep this version, change it or leave it out. When working in the CLI without a preview pane, link to the exact copy for the teacher to open in the intended app.

## Worked example for an environmental data course

This fictional ENVS-120 walkthrough shows what a teacher could ask and what a draft could contain. The HTML and student question are included below. The original OLAT course, a live quiz attempt, keyboard interaction, screen-reader output and separate teacher file were not verified in this example.

### Step 1 · Start with your course & Step 2 · Choose the materials we can use

- **Assistant (multi-select card, or compact numbered plain-chat alternative):**
  > This helps me keep course materials and student information in the right place. You can skip it and still make materials. If a tool would help with a particular task, I’ll explain it then. **What would you like to work from?** Choose any that apply, or tell me in your own words:
  > 1. A course in a learning platform, such as Moodle or OLAT
  > 2. Files on my computer or in the cloud, such as slides, handouts, rubrics or spreadsheets
  > 3. A learning app or activity, such as Kahoot!, Mentimeter (Menti), Klicker or H5P
  > 4. Another source, such as a website, video or design example
  > 5. Start with my description
  > 6. Skip for now
- **Teacher:** *"1, 2 and 3 — my Week 5 lesson uses a slide deck, an OLAT page and a linked quiz, but I can describe them for now. Students read a temperature-anomaly chart on the slides and jump straight to one cause without checking confounding factors. The written final exam is fixed, and everything must work by keyboard without colour-only chart cues."*
- **Assistant:** “I’ll work from your description. Your course site, slides and quiz can stay closed. When you want editable drafts, I’ll ask where you would like to keep them.”

### Step 3 · Check the course brief

- **Assistant:** “You want learners to consider another explanation when they interpret a temperature chart. The final written exam is fixed. Week 5 needs keyboard access and a table that works without colour. We can work from your description.” The assistant asks one question:
  > *"Where in Week 5 do students currently practise weighing a competing explanation before the final exam?"*
- **Teacher:** *"Only on the linked OLAT quiz, which pulls multiple-choice items from a shared department bank (`Dept_EnvStats_Bank`) that I must not overwrite."*
- **Assistant:** Checks the summary with the teacher and asks them to approve or correct it. The new exercise must remain independent of the shared bank.

### Steps 4–6 · Choose a focus, a change and a plan

- **Step 4 · Choose what to focus on:** Specialist perspectives note the gap between passive slide viewing and multiple-choice recall versus written exam justification; the teacher picks rehearsing short confounding-variable explanations before the exam.
- **Step 5 · Choose which changes to make:**
  - Assistant proposes: (A) add a 3-minute individual prediction and accessible data table on Slide 4 before Slide 4B's reveal; (B) author a separate two-question short-answer activity for possible use in OLAT (detached from `Dept_EnvStats_Bank`, with scoring notes isolated in a separate teacher file); (C) add a 10-minute post-class discussion-forum thread.
  - **Teacher:** *"Keep the Slide 4 prediction step, shorten the separate unlinked quiz copy to one 4-minute in-class check, and leave out the post-class forum."*
  - **Assistant editable recap:** Kept Slide 4 prediction + table; shortened local quiz draft to 4 minutes (1 item, no bank link); omitted post-class forum.
- **Optional tool offer with setup help (and decline):**
  - **Assistant:** *“A Google Slides integration could turn the fictional text for these two slides into an editable deck in your account. Would you like help checking whether it is available and covered by your plan, or shall I make a local HTML draft? I would wait for your decision before sharing the text.”*
  - **Teacher:** *"Keep everything local for now—no Google Slides connection."*
  - **Assistant (Step 6 · Review the plan and files):** Moves ahead immediately with local files and presents `Use this plan`, `Change the plan`, `Leave it for now`, plus custom input for two student drafts (`Week05_Slide04_Deck_Draft.html` and `Week05_LMS_Check_Copy.md`) and one teacher-only file (`Teacher_Scoring_Guide.md`) in a restricted area under `04_Working_Copies/2026-11-27_ENVS120/`. Teacher checks the three destinations and audiences, then chooses `Use this plan`. The teacher confirms the draft folder is private and chooses a separate teacher-only destination for the scoring guide. Only the learner files may be shared later.

### Step 7 · Try the drafts

**Draft 1 (`04_Working_Copies/2026-11-27_ENVS120/Week05_Slide04_Deck_Draft.html`):**

```html
<!DOCTYPE html><html lang="en"><body><main>
<h1>Slide 4 — Predict Before Explaining (3 Minutes, Individual)</h1>
<p>Compare Station B and Station C. Before opening the explanation, identify one variable other than tree cover that could explain Station B's lower night temperature.</p>
<table><caption>Night temperature and site variables (no colour-only cues)</caption>
<thead><tr><th scope="col">Station</th><th scope="col">Urban Tree Cover (%)</th><th scope="col">Mean Night Temp (°C)</th><th scope="col">Distance to Coast (km)</th></tr></thead>
<tbody>
<tr><td>Station A</td><td>18%</td><td>21.4 °C</td><td>14.0 km</td></tr>
<tr><td>Station B</td><td>20%</td><td>17.8 °C</td><td>0.6 km</td></tr>
<tr><td>Station C</td><td>46%</td><td>19.1 °C</td><td>15.2 km</td></tr>
</tbody></table>
<details><summary>Slide 4B — Check Your Reasoning (Press Enter or Space)</summary>
<p>Station B is 0.6 km from the coast and Station C is 15.2 km away. Distance to the coast is one possible competing explanation. Comparing these two stations cannot tell us whether coast or tree cover caused the temperature difference.</p>
</details></main></body></html>
```

**Draft 2 (`04_Working_Copies/2026-11-27_ENVS120/Week05_LMS_Check_Copy.md` — detached from `Dept_EnvStats_Bank`, AI-free, no teacher keys):**

```markdown
# Week 5 In-Class Check — Local Draft for an OLAT Activity (4 Minutes)

*Use the data table in the accompanying slide. You have four minutes. Work independently without AI tools.*

**Prompt:** Using the Slide 4 data table, explain in 2–3 sentences why comparing Station B and Station C alone cannot prove that higher tree cover cools night air—name one confounding variable and cite its values for both stations.
```

**Draft 3 (teacher only).** The example plan also names `Teacher_Scoring_Guide.md`. Its contents are not reproduced here. In a real project, deliver and independently review that file in the approved teacher-only location, or record the teacher’s decision to leave out that file and keep it private. Its original filename stays in the plan.

**What to check in a real course.** The sample HTML contains a table caption, labelled column headers and a native disclosure control. Those are visible in the source. To check the rendered draft, open the approved local file and use Tab and Enter or Space to reveal the explanation. For a screen reader, verify that the station, temperature and distance are announced together. No live OLAT import, student submission or feedback timing was tested here. If OLAT is available later, create or select an approved private draft, check that it is independent of the shared bank, and try one student attempt. Until then deliver the Markdown as an editable draft.
- **Two separate confirmations.** In this example the lecturer chooses **all three** checked files. In your course, you can leave a file out. It stays private and is omitted from the handover. A request for changes keeps the decision open until you have tried the revised copy and decided again. If you leave everything out, you can stop or revise a draft. There is nothing to hand over. Once each item has a decision and at least one is ready, answer the following questions one at a time. Each reply must refer to the current run and named items. Show the names for review and keep technical identifiers in the recorded context.
  1. Teacher sends Reply 1: `The drafts are ready for handover.` *(Deutsch: `Die Entwürfe sind bereit zur Übergabe.`)*
  2. Assistant shows all three accepted, checked drafts and the exact destination `04_Working_Copies/2026-11-27_ENVS120/Production_Handoff.md`; teacher sends separate Reply 2:
     `Save the handover document at the location below.`
     `04_Working_Copies/2026-11-27_ENVS120/Production_Handoff.md`
     *(Deutsch: `Speichern Sie die Übergabe am unten angegebenen Ort.` + exact path)*
  3. Assistant saves and independently reopens `Production_Handoff.md` to check that all accepted drafts and outstanding checks match the saved summary.

### Step 8 · Decide what to use & Step 9 · Finish or suggest an improvement

- **Step 8 · Decide what to use.** Review each included draft in its intended view. In the example that means two student drafts and a teacher-only guide. Choose `Use this version`, `Request changes`, `Leave it out`, or describe another change. In the example, the teacher asks for a shorter reveal label on the slide. The assistant would reopen the update and show it before asking for acceptance.
- **Step 9 (finish cleanly):** Assistant asks once: *"Would you like a written suggestion for improving how this redesign worked?"* (`Write a suggestion`, `Finish here`, or custom answer). The teacher picks `Finish here` for Step 9. They can skip the optional second opinion and finish.

### Step 10 · Would you like a second opinion?

After Step 9, **Skip** finishes immediately. If you choose **Prepare a review**, ask for the status of all nine teaching steps in the conversation, including skipped steps. If an approved **Walkthrough** already summarises the run, open it from **Artifacts** to check the evidence. Select the exact student drafts and versions in **Documents**. Review any teacher-only material in its restricted location. [Antigravity side panel](https://antigravity.google/docs/side-panel)

Look in the current Antigravity account’s model picker first. If it offers a suitable unused family, such as an included Claude model after a Gemini-only run, prefer a fresh Antigravity conversation with only the approved packet. If none fits here, offer a different signed-in app using separately approved computer control, or a manual handover. Check the families used across the whole run. If all eligible families contributed, identify the least-involved family, ideally different from the main author of this item. Disclose its earlier contribution and let the teacher choose a **limited second look** or finish. With one family, distinguish another model from an exact same-model self-check. Neither is an independent family review.

Choose a model from a different family than the one that actually prepared the drafts. For a worksheet made with Gemini, for example, ask which included Claude or GPT model can inspect the approved format. Check current model documentation and the signed-in account's picker. You may choose another model, use a different app or skip. Check the final packet in chat, including Steps 1–9 and skips, selected files, any original you individually opt in, receiving app, account, model, audience and cost. Only a separate final **Send this packet** decision authorises transfer. When the recipient runs in a supported, already approved browser tab, the browser agent can help deliver it to a fresh conversation with only that context. Alternatively, copy it yourself. Ask for findings tied to a step and page, slide or item, its version and evidence, including anything the reviewer could not verify. Choose which changes to try and reopen each affected learner draft for review. [Antigravity models](https://antigravity.google/docs/models) · [Browser use](https://antigravity.google/docs/browser)

<details>
<summary>Technical records and exact optional confirmation wording</summary>

## Details for the person maintaining the workflow

The ten specialist profiles inherit the selected model and are limited to reading the minimal authorised files for their assigned task. Their configured tools are `view_file` and `grep_search`. Shell execution and inherited MCP access are disabled. Browser actions and publishing are outside their permissions. If the host cannot independently check an item, record what is still unverified. Teacher approvals come from their actual replies in the current conversation.

Maintain the separate read-only planning and approved writing steps. Save only to the agreed local destination or specifically bound private external draft. Before every write check the real destination, container and audience, verify linked copies separately and reopen the saved result. A title alone cannot identify a copy. Screenshots and browser staging are additional destinations. Keep protected sources and teacher keys out of them. The shared materials guide explains approved private-draft evidence and per-file handling.

Check current records before asking for missing information. Show the teacher the action, named items and destination; fill in technical details for review where required. Record each planned target and the lecturer’s decision for that target. Every included copy needs current acceptance and independent checks. Keep an excluded target in the plan and out of the handover. An open revision or missing decision blocks the handover. The first handover reply confirms the drafts are ready. A separate second reply authorises saving the document and repeats the exact target. After saving it, independently reopen and verify it before final acceptance. Preserve the teacher’s exact words and bind the reply to the current run. The schedule example only applies to a separate scheduling request; fill in the actual ID, version, exact expiry and time zone before requesting a decision.

| Action | English | Deutsch |
| --- | --- | --- |
| Mark the drafts ready (Reply 1) | `The drafts are ready for handover.` | `Die Entwürfe sind bereit zur Übergabe.` |
| Save the handover document (Separate Reply 2 with exact path) | `Save the handover document at the location below.` | `Speichern Sie die Übergabe am unten angegebenen Ort.` |
| Prepare an inactive change to redesign files (Separate later step) | `Prepare the proposed changes to the files listed below.` | `Bereiten Sie die vorgeschlagenen Änderungen an den unten aufgeführten Dateien vor.` |
| Optional expiring schedule (3-line reply populated from stored contract) | `Set up this schedule.`<br>`Schedule: <ID> <version>`<br>`Expires: <exact expiry>` | `Richten Sie diesen Zeitplan ein.`<br>`Zeitplan: <ID> <version>`<br>`Gültig bis: <exact expiry>` |

[Antigravity browser and account support](https://antigravity.google/docs/browser) · [Custom subagents](https://antigravity.google/docs/subagents).

</details>
