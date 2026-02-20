---
name: stakeholder-feedback-analysis
description: Predict likely feedback from key stakeholders on proposals, initiatives, or strategic documents by analyzing their communication patterns, priorities, and decision-making styles. Invoke explicitly with /stakeholder-feedback or auto-apply when preparing for board meetings, executive reviews, or initiative presentations.
---

# Stakeholder Feedback Analysis Skill

## Purpose
Predict likely feedback from key stakeholders on proposals, initiatives, or strategic documents by analyzing their communication patterns, priorities, and decision-making styles.

## When to Use This Skill
- Before presenting strategic plans, rocks, or initiatives to leadership
- When preparing for board meetings or executive reviews
- To anticipate objections and prepare responses
- To tailor messaging for different stakeholder groups

---

## Methodology

### Step 1: Identify Stakeholders
Create a list of all stakeholders who will review or approve the proposal, including:
- Name and title
- Role in decision (Accountable, Responsible, Consulted, Informed)
- Expected level of engagement (high/medium/low)

### Step 2: Research Communication Patterns (Parallel)
For each stakeholder, launch parallel research agents to analyze:

**A. Email Communications**
- Search Gmail for emails from/to/cc the stakeholder
- Analyze: tone, length, questioning patterns, priorities mentioned
- Look for: recurring themes, pet peeves, approval language

**B. Google Drive Documents**
- Search for documents authored by or mentioning the stakeholder
- Analyze: writing style, focus areas, decision frameworks
- Look for: strategic priorities, measurement preferences, risk tolerance

**C. Meeting Patterns**
- Review calendar invitations and meeting titles
- Analyze: which meetings they prioritize, recurring cadences
- Look for: operational vs. strategic focus, cross-functional involvement

**D. Decision History** (if available)
- Previous approvals/rejections on similar initiatives
- Feedback patterns on past proposals
- Changes they've requested historically

### Step 3: Build Stakeholder Profiles
For each person, document:

**Communication Style:**
- Tone (direct/collaborative/formal/casual)
- Length preference (concise/detailed)
- Format preference (bullet points/narratives/data-driven)
- Response time patterns

**Core Priorities:**
- Top 3-5 areas they care about most
- What keeps them up at night
- Success metrics they track
- Recent initiatives they're driving

**Decision-Making Approach:**
- Questions they typically ask
- Framework they use (ROI/risk/strategic fit)
- Red flags that trigger rejection
- Green flags that earn support

**Personality Traits:**
- Analytical vs. intuitive
- Risk tolerance (conservative/aggressive)
- Detail-oriented vs. big-picture
- Collaborative vs. directive

### Step 4: Predict Feedback by Initiative
For each major element of your proposal:

**✅ Will Support If:**
- [Conditions that align with their priorities]
- [Elements that match their decision framework]

**⚠️ Will Question:**
- [Specific questions they'll likely ask]
- [Areas where they'll want more detail]

**🔴 Red Flags:**
- [Dealbreakers or major concerns]
- [Missing elements they expect to see]

### Step 5: Prepare Response Strategy

**How to Frame the Proposal:**
- Lead with what they care about most
- Use their language and frameworks
- Address red flags proactively
- Provide evidence they find credible

**Meeting Strategy:**
- Who to brief first (1:1 pre-meetings)
- What order to present (sequence matters)
- Who to pair together (alliances)
- When to schedule (timing considerations)

---

## Implementation Template

### Research Phase (Use Parallel Agents)

```markdown
For each stakeholder, use Task tool with Explore agent:

"Research [STAKEHOLDER NAME]'s communication patterns, priorities, and personality:
- Search GDrive for documents authored by or mentioning [NAME]
- Search emails from/to/cc [EMAIL]
- Analyze meeting patterns and calendar invitations
- Look for patterns in: what they care about, how they communicate, their role, their concerns
- Focus on understanding: decision-making approach, typical questions/concerns, red flags
Goal: Create a profile to predict what feedback they'll give on [INITIATIVE NAME]"
```

### Analysis Template

For each stakeholder, create a profile using this structure:

```markdown
## [STAKEHOLDER NAME] - [ROLE/TITLE]

### Role & Scope
- [Primary responsibilities]
- [Organizational influence]
- [Key relationships]

### Communication Style
- **Tone:** [direct/collaborative/formal]
- **Length:** [concise/detailed]
- **Format:** [bullets/narrative/data]
- **Response Pattern:** [same-day/weekly/thoughtful]

### Core Priorities (Top 3-5)
1. [Priority 1 with evidence]
2. [Priority 2 with evidence]
3. [Priority 3 with evidence]

### Decision-Making Approach
- **Framework:** [How they evaluate proposals]
- **Key Questions:** [What they always ask]
- **Red Flags:** [What triggers rejection]
- **Green Flags:** [What earns support]

### Expected Feedback on [INITIATIVE]

**✅ Will Support:**
- [Aligned elements]

**⚠️ Will Question:**
- [Specific concerns or clarification needs]

**🔴 Red Flags:**
- [Dealbreakers]

### How to Prepare
- [Framing strategy]
- [Evidence to provide]
- [Pre-meeting approach]
```

### Output Document Structure

```markdown
# [INITIATIVE NAME] - Expected Stakeholder Feedback

**Initiative Overview:**
[Brief summary of what you're proposing]

---

## 1. [STAKEHOLDER 1 NAME]
[Profile and predictions]

## 2. [STAKEHOLDER 2 NAME]
[Profile and predictions]

[etc.]

---

## SUMMARY: KEY THEMES

### Universal Concerns
- [Concerns shared by multiple stakeholders]

### Initiative-Specific Patterns
- [Patterns by workstream or component]

### Meeting Strategy
1. [Step-by-step approach to presenting]
```

---

## Example Use Cases

### Use Case 1: Strategic Initiative Approval
**Context:** Presenting Q1 Rocks to executive team
**Stakeholders:** CEO, COO, CTO, VP Marketing, VP Operations
**Output:** Feedback prediction document with speaking points for each person

### Use Case 2: Board Presentation Prep
**Context:** Quarterly board meeting on M&A strategy
**Stakeholders:** Board members, investors, CEO, CFO
**Output:** Objection-handling guide and board deck messaging

### Use Case 3: Cross-Functional Project Kickoff
**Context:** Launching new data platform initiative
**Stakeholders:** IT leads, business unit leaders, finance
**Output:** Stakeholder engagement plan with tailored messaging

---

## Best Practices

### Research Phase
1. **Use parallel agents** for efficiency (research all stakeholders simultaneously)
2. **Look for patterns** not individual emails (volume > single instance)
3. **Search recent activity** (last 3-6 months most relevant)
4. **Cross-reference sources** (email + docs + meetings = complete picture)

### Analysis Phase
1. **Be specific** with predictions (not "they'll want data" but "they'll ask for 3-year ROI model")
2. **Provide evidence** for each claim about personality/priorities
3. **Distinguish** between dealbreakers and preferences
4. **Consider relationships** between stakeholders (who influences whom)

### Presentation Phase
1. **Pre-brief key influencers** (get buy-in before group setting)
2. **Tailor the deck** (different versions for different audiences if needed)
3. **Address red flags proactively** (don't wait for them to raise)
4. **Bring supporting data** they'll ask for (have backup slides ready)

---

## Tools & Techniques

### For Research
- **Google Docs MCP:** `mcp__google-docs__searchGoogleDocs` (search docs by name/content), `mcp__google-docs__listGoogleDocs` (list recent docs), `mcp__google-docs__readGoogleDoc` (read doc content)
- **Slack MCPs:** `mcp__slack-elm__conversations_history` / `mcp__slack-bell__conversations_history` / `mcp__slack-stanleyruth__conversations_history` (search Slack for communication patterns per workspace)
- **Linear MCP:** `mcp__claude_ai_Linear__list_issues` / `mcp__claude_ai_Linear__get_issue` (review project involvement and priorities)
- **Task Tool:** Launch Explore agents for deep research in parallel
- **Note:** Gmail and GDrive MCPs (`mcp__gmail__*`, `mcp__gdrive__*`) may be available depending on workspace config — use `ToolSearch` to check before calling

### For Analysis
- **Pattern Recognition:** Look for recurring phrases, meeting cadences, decision frameworks
- **Historical Context:** Review past decisions on similar initiatives
- **Peer Comparison:** How do they interact with others? Who do they trust?

### For Output
- **Markdown Documents:** Easy to share, version, and reference
- **Structured Format:** Use ✅ ⚠️ 🔴 indicators for clarity
- **Actionable Insights:** Every prediction should inform a preparation step

---

## Skill Invocation

To use this skill in the future:

**Manual Approach:**
1. List stakeholders and roles
2. Launch parallel research agents (one per stakeholder)
3. Synthesize findings into profile document
4. Generate feedback predictions
5. Create meeting strategy

**Automated Approach:**
Use this prompt:

```
Analyze stakeholder feedback for [INITIATIVE NAME]:

Stakeholders:
1. [Name, role, email]
2. [Name, role, email]
[...]

Document: [Link or path to the proposal/initiative]

Please:
1. Research each stakeholder's communication patterns in parallel
2. Build profiles for each person
3. Predict their likely feedback on this initiative
4. Create a meeting strategy document

Output format: Stakeholder Feedback Analysis document
```

---

## Maintenance & Updates

**Update stakeholder profiles when:**
- New strategic priorities emerge (quarterly VTO updates)
- Leadership changes or role changes occur
- Major organizational shifts happen
- After significant decision events (learn from actual feedback vs. predicted)

**Review accuracy:**
- After each major presentation, compare predicted vs. actual feedback
- Adjust profiles based on discrepancies
- Document new patterns or priority shifts
- Archive outdated communication patterns

---

## Success Metrics

This skill is working well when:
- ✅ You anticipate 80%+ of questions asked
- ✅ No major objections come as a surprise
- ✅ Stakeholders feel "heard" (you addressed their concerns proactively)
- ✅ Approval rates increase on strategic initiatives
- ✅ Meeting time decreases (less back-and-forth needed)

---

## Version History
- **v1.0** (Feb 2026): Initial skill created based on Q1 2026 Rocks stakeholder analysis
