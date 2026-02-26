# Shared Skills for Claude Code

A collection of Claude Code skills organized by category. Each skill is a `SKILL.md` file that Claude Code loads automatically based on trigger conditions.

## Why Skills?

Claude Code is powerful out of the box, but it defaults to generic behavior. Skills give it **process knowledge** — the same frameworks, quality standards, and thinking patterns your team already uses. Instead of getting "helpful AI assistant" output, you get output that follows your playbook.

Skills solve three problems:
1. **Consistency** — Every team member gets the same writing voice, the same brainstorming rigor, the same feedback framework
2. **Quality floor** — Skills encode best practices so the baseline is high even when the user's prompt is vague
3. **Institutional knowledge** — Patterns that live in people's heads get codified and shared

## Skill Categories

| Category | Skills | Purpose |
|----------|--------|---------|
| **[Writing](#writing)** | 8 skills | Voice, executive comms, sales copy, SOPs, spreadsheets, audience routing |
| **[Thinking](#thinking)** | 2 skills | Structured brainstorming and idea evaluation |
| **[Session](#session)** | 1 skill | Context window management across long sessions |
| **[Meta](#meta)** | 1 skill | Building new skills for your team |
| **[Starter Template](#starter-template)** | 1 file | CLAUDE.md template for Trusted Advisor posture |

---

## Writing

Skills that enforce consistent, high-quality writing across different contexts.

| Skill | Purpose | Trigger |
|-------|---------|---------|
| **[personal-writing](writing/personal-writing/SKILL.md)** | Base layer for all writing. Voice, anti-AI patterns, banned words, rhythm. | Any prose of 2+ sentences |
| **[executive-communication](writing/executive-communication/SKILL.md)** | Board decks, investor updates, memos, decision documents. Pyramid Principle, SCQA, action titles, MECE. | Audience is director-level or above |
| **[internal-training-comms](writing/internal-training-comms/SKILL.md)** | SOPs, training materials, onboarding docs, change communications. Adult learning principles, action mapping. | Audience is employees or field staff |
| **[sales-copywriting](writing/sales-copywriting/SKILL.md)** | Direct mail, landing pages, email campaigns, proposals, ad copy. Direct response frameworks, VoC, awareness-level matching. | Customer-facing marketing content |
| **[sop-creator](writing/sop-creator/SKILL.md)** | Runbooks, playbooks, checklists, decision trees, onboarding guides. Definition of Done, specificity rules. | Documenting any repeatable process |
| **[spreadsheet-standards](writing/spreadsheet-standards/SKILL.md)** | IB/consulting-grade Google Sheets layout, formula discipline, formatting, MCP API constraints. | Building or writing to any Google Sheets deliverable |
| **[stakeholder-feedback-analysis](writing/stakeholder-feedback-analysis/SKILL.md)** | Predict stakeholder reactions to proposals and initiatives. Communication pattern analysis, objection anticipation. | Preparing for board meetings or exec reviews |
| **[writing-router](writing/writing-router/SKILL.md)** | Routes writing requests to the right skill based on audience. Coordinates all writing skills above. | Any writing task where audience determines format |

### How Writing Skills Layer

`personal-writing` is the base layer — always active. The `writing-router` directs to the right audience-specific skill on top:

```
personal-writing          (voice, banned words, rhythm, anti-AI patterns)
    |
    +-- executive-communication    (Pyramid Principle, SCQA, MECE)
    +-- internal-training-comms    (adult learning, action mapping, ADKAR)
    +-- sales-copywriting          (PAS/AIDA/BAB, VoC, awareness levels)
    +-- sop-creator                (Definition of Done, specificity rules)
    +-- spreadsheet-standards      (FAST standard, formula discipline, MCP constraints)
    +-- stakeholder-feedback-analysis  (stakeholder profiling, objection prep)
```

When Claude invokes `executive-communication`, it also applies `personal-writing` rules underneath. The banned word list, rhythm checks, and anti-AI patterns apply to board decks just as they do to emails. The `writing-router` automates this selection — tell it the audience and it picks the right skill.

---

## Thinking

Skills for structured exploration and evaluation of ideas — before you start building.

| Skill | Purpose | Trigger |
|-------|---------|---------|
| **[brainstorming](thinking/brainstorming/SKILL.md)** | Clarifies WHAT to build through collaborative dialogue. Phases: assess clarity, understand the idea, explore approaches, capture the design. | "let's brainstorm", "help me think through", ambiguous feature requests |
| **[idea-feedback](thinking/idea-feedback/SKILL.md)** | Structured evaluation of a specific idea using Trusted Advisor principles. Phases: listen & understand, steel man, structured critique, synthesis & recommendation. | "what do you think of", "poke holes in", "evaluate this idea" |

### Brainstorming vs. Idea Feedback

These skills complement each other but serve different purposes:

- **Brainstorming** is for when you *don't yet know* what to build. Requirements are vague, multiple approaches exist, trade-offs need exploring. It's collaborative exploration.
- **Idea Feedback** is for when you *already have* a specific idea and want honest assessment. It earns the right to critique by listening first, steel-manning second, then giving a clear recommendation.

If someone says "help me think through X" → brainstorming. If someone says "what do you think of X" → idea-feedback.

---

## Session

Skills for managing Claude Code sessions effectively.

| Skill | Purpose | Trigger |
|-------|---------|---------|
| **[context-handoff](session/context-handoff/SKILL.md)** | Saves structured handoff when context window is getting full. Commits WIP, captures todo state, writes a resume file so the next session starts productive in 1-2 turns. | Long sessions, context compression, degraded recall |

### Why Context Handoff Matters

Claude Code's context window is large but finite. Without a clean handoff protocol, ending a long session means the next session starts from scratch — re-reading files, re-asking questions, re-discovering decisions. The context-handoff skill automates the save point: it commits uncommitted work, snapshots your progress, and writes a structured file the next session can pick up instantly.

---

## Meta

Skills for building and improving your team's skill library.

| Skill | Purpose | Trigger |
|-------|---------|---------|
| **[create-agent-skills](meta/create-agent-skills/SKILL.md)** | Guide for authoring Claude Code skills and slash commands. Covers YAML frontmatter, progressive disclosure, invocation control, subagent patterns, and testing. Includes 13 reference files. | Working with SKILL.md files, creating or auditing skills |

Use this skill when you want to create new skills for your team. It covers the official skill specification, best practices, and common patterns — so you don't have to reverse-engineer the format.

---

## Starter Template

A ready-to-customize `CLAUDE.md` that establishes two high-value defaults for any project:

| File | Purpose |
|------|---------|
| **[CLAUDE.md](starter/CLAUDE.md)** | Trusted Advisor posture + Confirmation Required Before Acting |

### What's in the Template

**Trusted Advisor Standards** — Configures Claude to behave as a peer advisor rather than a compliant assistant. It will lead with disagreements, identify weak assumptions before offering support, hold its position under social pressure, and flag material flaws proactively. This is the single highest-leverage configuration change you can make.

**Confirmation Required Before Acting** — Guardrails for shared systems. Claude will show drafts and wait for approval before creating issues, editing shared documents, or sending messages. Prevents the "helpful assistant that creates 12 Jira tickets you didn't ask for" failure mode.

### How to Use It

```bash
# Copy to your project root (project-specific config)
cp starter/CLAUDE.md ./CLAUDE.md

# Or copy to your home directory (global config)
cp starter/CLAUDE.md ~/.claude/CLAUDE.md
```

Then customize: add your team's tools, conventions, MCP servers, key file paths, and any domain-specific instructions.

---

## Installation

### Option 1: Copy individual skills

Pick the skills you want and copy them into your Claude Code skills directory:

```bash
# Copy a single skill
cp -r writing/personal-writing ~/.claude/skills/
cp -r thinking/brainstorming ~/.claude/skills/

# Copy an entire category
cp -r writing/* ~/.claude/skills/
cp -r thinking/* ~/.claude/skills/
```

### Option 2: Git submodule (recommended for teams)

Add this repo as a submodule to keep skills in sync across the team:

```bash
# Add the submodule
git submodule add https://github.com/stanleyruth/writing-skills.git upstream/writing-skills

# Symlink the skills you want into your .claude/skills/ directory
ln -s ../../upstream/writing-skills/writing/personal-writing .claude/skills/personal-writing
ln -s ../../upstream/writing-skills/thinking/brainstorming .claude/skills/brainstorming
# ... repeat for each skill you want
```

This way, `git submodule update --remote` pulls the latest skills for everyone.

### Recommended setup order

1. Start with the **starter template** — copy `starter/CLAUDE.md` and customize it
2. Add **personal-writing** — the base layer that makes all output sound human
3. Add **writing-router** — auto-routes to the right writing skill by audience
4. Add **brainstorming** and **idea-feedback** — structured thinking before building
5. Add **context-handoff** — session management for long conversations
6. Add remaining writing skills as needed for your role (exec comms, sales copy, SOPs, etc.)
7. Add **create-agent-skills** when you're ready to build your own

Claude Code will detect and load skills automatically based on the trigger conditions in each skill's YAML frontmatter.

## Customization

These skills are designed to be forked and adapted. Common customizations:

- **Banned words**: Add industry-specific terms to the `personal-writing` banned list
- **Terminology**: Update the `internal-training-comms` terminology table for your systems
- **Trust signals**: Modify the `sales-copywriting` trust stack for your industry
- **SOP templates**: Add domain-specific templates to `sop-creator`
- **Spreadsheet conventions**: Adjust `spreadsheet-standards` formatting rules and API constraints for your platform
- **Stakeholder profiles**: Pre-populate known stakeholder patterns in `stakeholder-feedback-analysis`
- **Brainstorm output location**: Change the output path in `brainstorming` to match your project's docs structure
- **Advisor posture**: Tune the Trusted Advisor standards in `starter/CLAUDE.md` for your team's culture

## Credits

- `personal-writing` — Influenced by Ann Handley, Gary Halbert, CXL, blader/humanizer
- `executive-communication` — Barbara Minto (Pyramid Principle), McKinsey slide standards, Amazon memo format
- `internal-training-comms` — Malcolm Knowles (adult learning), Cathy Moore (action mapping), Prosci ADKAR
- `sales-copywriting` — Eugene Schwartz, Joanna Wiebe/CopyHackers, Robert Collier, Claude Hopkins
- `sop-creator` — Adapted from [coleam00/second-brain-skills](https://github.com/coleam00/second-brain-skills)
- `spreadsheet-standards` — FAST Standard, IB/consulting conventions, Google Sheets API constraints
- `stakeholder-feedback-analysis` — Original skill for stakeholder communication analysis
- `brainstorming` — YAGNI principles, collaborative design methodology
- `idea-feedback` — David Maister's Trusted Advisor framework
- `context-handoff` — Session continuity protocol for Claude Code
- `create-agent-skills` — Based on [official Claude Code skills documentation](https://code.claude.com/docs/en/skills)
