# Redesign a course with GitHub Copilot: a teacher's guide

Release `0.3.3` of the native `agentic-course-redesign` plugin.

This guide follows the nine steps you see in the conversation. At every
decision Copilot waits for your reply. Nothing here skips or replaces one of
those decisions.

## Before you begin

- Install the plugin with [PARTICIPANT_INSTALLATION.md](https://github.com/gpochs/Agentic-Course-Redesign-System/blob/main/02_Other_Agentic_Systems/01_GitHub_Copilot/PARTICIPANT_INSTALLATION.md).
- Work in a project **Session** in **Interactive** mode, not in **Chats**.
- Select an included model in the Copilot model picker. You need no API key,
  other model provider, connector or MCP server. If your app uses a custom
  (BYOK) provider, switch to an included model first. The
  [README](https://github.com/gpochs/Agentic-Course-Redesign-System/blob/main/02_Other_Agentic_Systems/01_GitHub_Copilot/README.md) explains a known issue with custom providers.
- Python 3 must be available as `python` for the setup helpers.
- Practise with the fictional example below. Keep student names, grades,
  submissions and accommodation letters out of the chat.

> **Optional help prompt.** Paste this at any point:
> `Which step are we on, what do you need from me now, and what can I leave open?`

## The nine steps

### Step 1 · Start with your course

Say what you teach and what you want learners to do better. Copilot then
asks what you'd like to work from. You can choose any mix of:

1. a course on a learning platform, such as Moodle or OLAT;
2. files on your computer or in the cloud;
3. a learning app, such as Kahoot!, Mentimeter, Klicker or H5P;
4. another source, such as a website, video or design example;
5. your own description; or
6. **Skip for now**.

Copilot uses a card when it can show all six options, accept combinations and
take your own words. Otherwise it asks one numbered question. Reply with
"2 and 5" or in a sentence.

**Mixed sources.** Naming a file, quiz or LMS course does not open it. Copilot
checks each item later, when it is actually needed.

**Skip and still make a resource.** With Skip for now, Copilot goes straight
to your teaching goal. You can still plan, draft, try out and accept a new
worksheet, quiz or slide set. "I'll just describe them for now" counts as
skipping. If you later want one real file, Copilot asks about that file only.

### Step 2 · Choose the materials we can use

Describe an item before you share a private link or file: public, your own,
internal to your institution, confidential, or mixed/unsure. Say what may be
read, who will see the results and whether Copilot may work in that app.

Different items can have different permissions. For example, Copilot may be
allowed to read a public course page but not the linked quiz bank. If an item
is unclear or unavailable, Copilot works with the rest. A mixed or uncertain
item stays closed until it is separated or clarified.

For an online course, open the exact authorised draft in the Browser panel if available and handle sign-in yourself. Verify its course, object and visibility before editing and reopen it to confirm what learners see. Copilot does not look at your other tabs or files.

For editable files, Copilot proposes a **new** folder inside your project and
lists the planned files before creating anything. It will not add files to an
existing folder before the material check. On the Skip route it summarises the
description-only scope and asks you once to confirm it.

### Step 3 · Check the course brief

Copilot summarises your learners, goal and fixed conditions in two or three
lines. Then it asks **one** question, which should be one whose answer changes
the next design choice. "I'm unsure" and "leave that open" are good answers.
Copilot notes an assumption and carries on. You can approve the brief with
questions still open.

Copilot keeps assessment rules and access needs apart:

| What you say | How Copilot treats it |
| --- | --- |
| "The module description (v2) sets a 90-minute closed-book exam." | A **fixed rule**. Copilot records who supplied the rule and designs around it. If you describe the rule, it cites your account; if you permit it to read the module description, it can verify the wording there. |
| "I can change the seminar and the feedback." | A **design choice** that is open to change. |
| "Last year's rubric gave points for naming the method." | **Background only.** Copilot asks you before it changes anything graded. |
| "The practice must work fully with a keyboard and screen reader." | A **functional need** that is built into everyone's route and tried in Step 7. |
| A name, diagnosis, approval letter or individual record | **Not needed.** Individual decisions stay with your exam or disability office. |

An approved individual accommodation (*Nachteilsausgleich*) is decided by the
responsible office. Copilot needs only its effect on the task, in terms that
identify nobody. If even that could identify a student, describe a
hypothetical need instead. The assessed skill and criteria are the same on
every route.

### Step 4 · Choose what to focus on

Five perspectives look at where students practise the skill and what the
assessment asks of them. You say where a change would matter most. Copilot
waits before investigating further.

### Step 5 · Choose which changes to make

For each proposal you see a small before-and-after example, its evidence and
the time it takes. Keep it, change it or leave it out. "Sounds good" is not a
decision, so say which. Saving the research notes to the named research folder
does not permit any course file.

If a writing tool could shorten the instructions for three agreed slides, Copilot explains the benefit, what the tool would see and any cost. You can choose it for that edit, request setup help, or have Copilot edit in the current session. Your choice covers only that task or batch.

### Step 6 · Review the plan and files

Copilot shows the order of activities, each exact file it will create and who
can see it. Student and teacher-only files are listed separately. Choose
**Use this plan**, **Change the plan** or **Leave it for now**. Nothing is
written before your choice. If you want a browser preview of a document, ask
for it to be added to the list now.

### Step 7 · Try the drafts

When the needed view is available, Copilot opens each agreed draft, records what it tried and shows you what remains to check. Otherwise you can open the exact working copy in its usual app.

| Draft | Where to look in Copilot | Fallback |
| --- | --- | --- |
| Text or Markdown worksheet | **Editor** panel: read the preview and edit directly. | Open the file in your own editor, or ask Copilot to show it with line numbers. |
| Web page or HTML preview | **Browser** panel. Copilot can open local `file://` pages and read their headings and labels. Try the page yourself with the keyboard. | Open the file in your own browser. |
| Word, PowerPoint or Excel | The native app on your computer. | A PDF or HTML preview listed in Step 6. |
| Private LMS draft | You open the draft in the **Browser** panel and sign in. | An authorised export or a description. |

For each planned draft, tell Copilot to keep this version, revise it, or leave it out. If you leave out the quiz, it stays private. The plan retains its original filename and your decision. If you ask for a change to the worksheet, try the revised copy before deciding again. If you leave everything out, you can stop or revise a draft. There is nothing to hand over.

Once you have decided on every draft and at least one checked version is ready, Copilot lists the versions you chose. You confirm twice, in two **separate** replies:

1. `The drafts are ready for handover.`
2. After Copilot shows the exact location, send
   `Save the handover document at the location below.` followed by that
   location. Copilot prepares this reply so you can copy it.

German works too: `Die Entwürfe sind bereit zur Übergabe.` and
`Speichern Sie die Übergabe am unten angegebenen Ort.` A plain "yes" or a
single click does not count for either confirmation.

### Step 8 · Decide what to use

Decide **for each file in the handover separately**: **Use this version**, **Request
changes**, **Leave it out**, or your own answer. Accepting one file does not
accept the others. For a change, say what you saw and where, for example
"In Task 2, change 'name the method' to 'choose and justify the method'."
Copilot changes only that file, reopens it and shows you the same spot.

### Step 9 · Finish or suggest an improvement

Copilot asks once whether you would like a written suggestion about how the
redesign process worked. If you do not reply, it waits. A yes or a no closes
this course's work. Installing, activating or scheduling any change would be a
separate later decision.

## Fictional example

1. Create a new empty folder, such as `Documents/ACR-Practice`, and add it as
   a project in the Copilot app. Start a session in **Interactive** mode.
2. Paste:

   ```text
   /agentic-course-redesign/course-redesign-orchestrator

   Fictional practice. I teach "Introduction to Survey Methods", a first-year module with about 36 students and a weekly 90-minute seminar. Students can name sampling methods but cannot justify which one fits a research question. I have slides, an OLAT course and a Klicker quiz, but I'll just describe them for now.
   Fixed: the module description (version 2) sets a 90-minute closed-book written exam with the criterion "justifies the choice of sampling method". I can change the seminar tasks and feedback.
   Some students have an approved arrangement. The seminar practice must work fully with a keyboard and screen reader.
   ```

3. You should see this:
   - Copilot treats your sources as description only and asks no file, folder
     or classification question.
   - Its summary keeps the exam fixed (module description v2, as reported by the teacher), treats
     the seminar as open to change and records the keyboard and screen-reader
     need for the whole group.
   - It asks one question, for example "What makes a justification convincing
     in your marking?", as an open question in chat.
4. Reply `I'm unsure.` Copilot should note an assumption and carry on.
5. Test the boundary: `Should I send you the student's approval letter?`
   Copilot should decline and keep only the functional need.
6. Later, Step 6 should list separate student and teacher files, such as
   `Seminar_Week5_Practice.md` and `Facilitator_Notes_Week5.md`, in a new run
   folder. In Step 7, use the Editor panel if available or inspect the saved worksheet in its actual app. In Step 8 you
   decide on each file.

**If something is missing:**

- The slash name does not autocomplete: select `course-redesign-orchestrator`
  from the installed plugin and paste the rest.
- No card appears: answer the numbered question with a number or in words.
- No Editor or Browser panel (for example, in the CLI or an IDE): open the file
  yourself and refer to line numbers. Copilot should note that it did not check
  the layout.
- If your organisation blocks plugins: use a project installation only if its policy permits that route. See
  [PARTICIPANT_INSTALLATION.md](https://github.com/gpochs/Agentic-Course-Redesign-System/blob/main/02_Other_Agentic_Systems/01_GitHub_Copilot/PARTICIPANT_INSTALLATION.md).
- Python is missing: the design conversation can continue, but the project
  folder and files wait until Python 3 works. Copilot should not write the
  control records by hand.

## Decisions that always wait for you

- Step 1: how you start.
- Step 2: each item's access, and the project folder or the description-only
  scope.
- Step 3: the course brief.
- Step 4: the focus.
- Step 5: each change, and the research notes location.
- Step 6: the plan and every exact file.
- Step 7: "drafts ready", then the handover location in a separate reply.
- Step 8: each file.
- Step 9: the improvement offer.

Copilot keeps gate names, run IDs and fingerprints in its technical records.
You never need to supply them.
