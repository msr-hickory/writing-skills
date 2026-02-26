---
name: context-handoff
description: Context window management protocol. Auto-activates when approaching context capacity. Saves structured handoff to memory and instructs user to resume in a fresh session. Use when conversation is long, context compression has occurred, or you notice degraded recall of earlier details.
user-invokable: true
---

# Context Handoff Protocol

This protocol makes a 200k context window feel infinite by ensuring clean handoffs between sessions before context degrades.

## When to Trigger

Two tiers: a **proactive warning** before compaction hits, and a **hard stop** after.

### Proactive Warning (before compaction)

After **~30 tool calls** or **~15 user turns** in a single session, warn the user:

> "Heads up — this session is getting long. I can keep going, but if we're not close to done, this is a good breakpoint for a handoff."

If the user says to continue, keep working but stay alert for hard-stop signals. Reset the warning — don't nag every turn.

### Hard Stop (non-negotiable)

Activate the full handoff protocol when ANY of these appear:

1. **Context compression occurred** — a `<context-compression>` or similar system message appeared, indicating prior messages were compressed
2. **Degraded recall** — you notice you're losing track of earlier decisions, file contents, or conversation details
3. **User requests handoff** — user says anything about context being full, conversation being long, or needing to wrap up

**Do NOT wait until context is completely exhausted.** Stop with room to spare — writing the handoff itself consumes context.

## Protocol Steps

### Step 1: Stop Current Work

Immediately stop what you're doing. Do not attempt to squeeze in "one more thing." Half-finished work with a clean handoff is better than finished work the next session can't understand.

### Step 2: Git Checkpoint

If there are any uncommitted changes from this session:

1. Stage the changed files
2. Commit with message: `wip: context handoff — [brief task description]`
3. Push if the branch has a remote

Do NOT skip this. Uncommitted changes are invisible to the next session. If the user switches tasks before resuming, un-committed work is effectively lost.

### Step 3: Capture Todo State

If TodoWrite was used during this session, snapshot the current todo list into the handoff. Copy the items and their statuses exactly — the next session should restore them.

### Step 4: Write Handoff File

**Determine the handoff path:**
- If the current working directory has a `.claude/memory/` directory, write there (project-local)
- Otherwise, fall back to the shared config: `~/.claude/memory/` or the ai-config-repo equivalent

**Filename:** `YYYY-MM-DD-HHMM-context-handoff.md` using current date and 24-hour time.

**Handoff template** (write this as the file content — do NOT wrap in a code fence):

---

YAML frontmatter:
- type: context-handoff
- created: YYYY-MM-DD HH:MM
- task: [short task name]
- status: incomplete
- cwd: [current working directory]
- branch: [git branch name, if any]

Sections to include:

**# Context Handoff: [Task Name]**

**## Objective** — What we set out to accomplish this session.

**## Completed** — Bulleted list of specific items done, with file paths.

**## Pending** — Checkbox list of remaining tasks, ordered by priority.

**## Todo State** — If TodoWrite was active, reproduce the full todo list with statuses (completed / in_progress / pending) so the next session can restore it.

**## Resume Instructions** — Include this exact block:

> To resume, start a fresh Claude Code session and send:
> `resume [task description] from [full handoff file path]`

If the next session does NOT have the context-handoff skill loaded (e.g., different project without this config), include these inline instructions in the handoff file:

> **For the resuming session:** Read this file, acknowledge completed work, start on the first pending item, and reference blockers/decisions below — do not re-ask resolved questions.

**## Blockers & Decisions** — Any blockers encountered. Key decisions made this session and why. Architectural choices, rejected approaches, and rationale.

**## Key Context** — File paths that matter. Branch name. Error messages, API responses, or state not captured in code.

---

### Step 5: Send User Message

Send this exact message (filling in the path):

> I need to stop here. This session is approaching context capacity, and continuing risks missed details.
>
> I committed WIP changes and saved a full handoff at `[handoff file path]`.
>
> Please start a fresh chat and send:
> `resume [task] from [handoff file path]`

### Step 6: Do Not Continue

After sending the message, **stop**. Do not:
- Try to finish "just one more thing"
- Offer to keep going
- Minimize the context issue
- Suggest workarounds to avoid restarting

The whole point is clean breaks with zero information loss.

## Resume Protocol (For the Next Session)

When a user sends `resume [task] from [path]`:

1. Read the handoff file at the specified path
2. Restore the todo list from the Todo State section (if present)
3. Acknowledge what was completed
4. Start on the first pending item
5. Reference blockers/decisions — do not re-litigate resolved decisions
6. Delete the handoff file when the task is fully complete

## Quality Bar

A good handoff lets the next session start productive work within 1-2 turns. If the next session needs to re-read files or re-ask questions to understand what happened, the handoff was too thin.

**Include file paths.** Include branch names. Include the exact error message. Include the decision and the reason. Future-you has zero context — write for them.
