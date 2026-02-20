# Writing Skills for Claude Code

A collection of Claude Code skills that enforce consistent, high-quality writing across different contexts. Each skill is a `SKILL.md` file that Claude Code loads automatically based on trigger conditions.

## Skills

| Skill | Purpose | Trigger |
|-------|---------|---------|
| **[personal-writing](skills/personal-writing/SKILL.md)** | Base layer for all writing. Voice, anti-AI patterns, banned words, rhythm. | Any prose of 2+ sentences |
| **[executive-communication](skills/executive-communication/SKILL.md)** | Board decks, investor updates, memos, decision documents. Pyramid Principle, SCQA, action titles, MECE. | Audience is director-level or above |
| **[internal-training-comms](skills/internal-training-comms/SKILL.md)** | SOPs, training materials, onboarding docs, change communications. Adult learning principles, action mapping. | Audience is employees or field staff |
| **[sales-copywriting](skills/sales-copywriting/SKILL.md)** | Direct mail, landing pages, email campaigns, proposals, ad copy. Direct response frameworks, VoC, awareness-level matching. | Customer-facing marketing content |
| **[sop-creator](skills/sop-creator/SKILL.md)** | Runbooks, playbooks, checklists, decision trees, onboarding guides. Definition of Done, specificity rules. | Documenting any repeatable process |
| **[spreadsheet-standards](skills/spreadsheet-standards/SKILL.md)** | IB/consulting-grade Google Sheets layout, formula discipline, formatting, MCP API constraints. | Building or writing to any Google Sheets deliverable |
| **[stakeholder-feedback-analysis](skills/stakeholder-feedback-analysis/SKILL.md)** | Predict stakeholder reactions to proposals and initiatives. Communication pattern analysis, objection anticipation. | Preparing for board meetings or exec reviews |

## How They Layer

`personal-writing` is the base layer. All other writing skills explicitly build on top of it:

```
personal-writing          (voice, banned words, rhythm, anti-AI patterns)
    |
    +-- executive-communication    (Pyramid Principle, SCQA, MECE)
    +-- internal-training-comms    (adult learning, action mapping, ADKAR)
    +-- sales-copywriting          (PAS/AIDA/BAB, VoC, awareness levels)
    +-- sop-creator                (Definition of Done, specificity rules)
    +-- spreadsheet-standards           (FAST standard, formula discipline, MCP constraints)
    +-- stakeholder-feedback-analysis  (stakeholder profiling, objection prep)
```

When Claude invokes `executive-communication`, it also applies `personal-writing` rules underneath. This means the banned word list, rhythm checks, and anti-AI patterns apply to board decks just as they do to emails.

## Installation

Copy the skills you want into your Claude Code skills directory:

```bash
# Copy all skills
cp -r skills/* ~/.claude/skills/

# Or copy individual skills
cp -r skills/personal-writing ~/.claude/skills/
cp -r skills/executive-communication ~/.claude/skills/
```

Claude Code will detect and load them automatically based on the trigger conditions in each skill's YAML frontmatter.

## Customization

These skills are designed to be forked and adapted. Common customizations:

- **Banned words**: Add industry-specific terms to the `personal-writing` banned list
- **Terminology**: Update the `internal-training-comms` terminology table for your systems
- **Trust signals**: Modify the `sales-copywriting` trust stack for your industry
- **SOP templates**: Add domain-specific templates to `sop-creator`
- **Spreadsheet conventions**: Adjust `spreadsheet-standards` formatting rules and API constraints for your platform
- **Stakeholder profiles**: Pre-populate known stakeholder patterns in `stakeholder-feedback-analysis`

## Credits

- `personal-writing` — Influenced by Ann Handley, Gary Halbert, CXL, blader/humanizer
- `executive-communication` — Barbara Minto (Pyramid Principle), McKinsey slide standards, Amazon memo format
- `internal-training-comms` — Malcolm Knowles (adult learning), Cathy Moore (action mapping), Prosci ADKAR
- `sales-copywriting` — Eugene Schwartz, Joanna Wiebe/CopyHackers, Robert Collier, Claude Hopkins
- `sop-creator` — Adapted from [coleam00/second-brain-skills](https://github.com/coleam00/second-brain-skills)
- `spreadsheet-standards` — FAST Standard, IB/consulting conventions, Google Sheets API constraints
- `stakeholder-feedback-analysis` — Original skill for stakeholder communication analysis
