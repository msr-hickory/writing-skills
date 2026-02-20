---
name: internal-training-comms
description: Apply when writing any staff-facing content — SOPs, training materials, onboarding docs, process guides, internal announcements, change communications, scorecards/playbooks, or team-facing operational content. Enforces adult learning principles, action mapping, plain language, and change management communication patterns. Invoke explicitly with /internal-comms or auto-apply when the audience is Hickory employees, technicians, CSRs, or field staff.
---

# Internal Training & Communications Skill

**Version**: 1.0
**Last Updated**: 2026-02-14
**Owner**: Michael
**Status**: Active

---

## Skill Layering

**Always apply the personal-writing skill underneath this skill.** The personal-writing rules (voice, banned words, rhythm, anti-AI patterns) are the base layer. This skill adds internal-audience-specific structure (adult learning principles, action mapping, change management) on top.

---

## Trigger Conditions

Use this skill when:
- Writing SOPs, process guides, or step-by-step procedures
- Creating training materials, onboarding docs, or reference guides
- Drafting internal announcements, policy changes, or org updates
- Building playbooks, scorecards, or operational checklists
- Writing change management communications (new tool rollouts, process changes, reorgs)
- Creating content for technicians, CSRs, dispatchers, sales staff, or office teams
- Any content where the reader is a Hickory employee who needs to do something differently

---

## Core Philosophy

Internal content has one job: change what people do. Not what they know — what they **do**. If someone reads your SOP and can't immediately perform the task, the SOP failed. If someone reads your announcement and doesn't know what changes for them personally, the announcement failed.

Adults learn by doing, not by being lectured. They need to know **why** before they'll commit to **how**. They resist being talked down to. They have 30 competing priorities. Your content gets 90 seconds of attention before they decide it's relevant or not.

Write for the person in the truck between jobs, the CSR between calls, the new hire on day three. Not for the person reviewing the doc in a quiet office.

---

## Part 1: Adult Learning Principles (Knowles) — Applied

Every piece of internal content must honor how adults actually learn. These aren't abstract theories — they're design constraints.

### The Six Principles, Operationalized

| Knowles Principle | What It Means for Your Content | How to Apply |
|---|---|---|
| **Self-direction** | Adults resist being told what to do without context | Give the "why" before the "how." Let them see the logic. |
| **Experience** | Adults connect new info to what they already know | Reference their current workflow. "You already do X — this adds Y." |
| **Goal orientation** | Adults learn best when tied to a specific outcome | State the goal upfront: "After this, you'll be able to..." |
| **Relevance** | Adults ignore content that doesn't apply to their role | Tag content by role. Don't make a tech read CSR procedures. |
| **Practicality** | Adults want to apply immediately, not study theory | Lead with the action. Put background in an appendix or footnote. |
| **Respect** | Adults disengage when talked down to | Peer tone, not teacher tone. Acknowledge expertise. |

### The Acid Test

Before publishing any training material, answer these three questions:
1. **"Why should I care?"** — Is the relevance obvious within the first 2 sentences?
2. **"What do I do differently?"** — Is the specific behavior change stated clearly?
3. **"Can I do this right now?"** — Is there enough detail to act without asking someone?

If any answer is no, revise.

---

## Part 2: Action Mapping (Cathy Moore) — Applied

### The Principle

Don't start with "What do people need to know?" Start with "What do people need to **do** to hit this business goal?"

Traditional training dumps information. Action-mapped training designs practice around the decisions people actually make on the job.

### The Four-Step Process

```
1. Define the measurable business goal
        ↓
2. Identify the specific actions people need to take
        ↓
3. Design practice activities around those actions
        ↓
4. Add ONLY the information people need to complete those actions
```

### Applying Action Mapping to SOPs and Training

| Step | Question | Example (CSR call handling) |
|---|---|---|
| **Business goal** | What measurable outcome are we driving? | "Increase diagnostic booking rate from 38% to 55%" |
| **Actions** | What do people need to do on the job? | "Ask 3 qualifying questions before offering a price. Book the diagnostic, not the repair." |
| **Practice** | How do they rehearse this? | "Listen to 3 call recordings. Identify where the CSR gave a price vs. booked a visit. Role-play 5 inbound calls." |
| **Info needed** | What's the minimum knowledge required? | "The 3 qualifying questions. The booking script. The escalation path if the customer insists on a price." |

### What to Cut

If content doesn't directly support an action the learner needs to take, cut it:

- Company history → Cut (unless it's day-1 onboarding context)
- "Understanding the importance of..." → Cut. State the importance in one sentence and move on.
- Technical theory behind a process → Move to appendix. Link for the curious.
- Policy rationale that spans 3 paragraphs → Compress to 1 sentence of "why" + the rule itself

---

## Part 3: SOP & Process Guide Standards

### Structure Template

Every SOP follows this structure. No exceptions.

```
┌─────────────────────────────────────────────┐
│ HEADER BLOCK                                 │
│ Title: [Action-oriented — "How to..." or     │
│         verb phrase]                          │
│ Applies to: [Role(s)]                        │
│ Last updated: [Date]                         │
│ Owner: [Name]                                │
│ Version: [#]                                 │
├─────────────────────────────────────────────┤
│ PURPOSE (1-2 sentences)                      │
│ Why this process exists. What goes wrong     │
│ without it.                                  │
├─────────────────────────────────────────────┤
│ WHEN TO USE                                  │
│ Trigger conditions. Be specific.             │
├─────────────────────────────────────────────┤
│ BEFORE YOU START                             │
│ Prerequisites, tools, access needed          │
├─────────────────────────────────────────────┤
│ STEPS                                        │
│ 1. [Verb] + [Object] + [Condition/Detail]    │
│    └─ Substep if needed                      │
│ 2. [Verb] + [Object] + [Condition/Detail]    │
│ 3. ...                                       │
├─────────────────────────────────────────────┤
│ IF SOMETHING GOES WRONG                      │
│ Common errors + what to do                   │
├─────────────────────────────────────────────┤
│ EXAMPLES (optional but encouraged)           │
│ Screenshot, sample, or worked example        │
└─────────────────────────────────────────────┘
```

### Writing Rules for Steps

| Rule | Right | Wrong |
|---|---|---|
| Start every step with a verb | "Open the job in ServiceTitan" | "The job should be opened" |
| One action per step | "Click Save." | "Click Save and then verify the status updated and send the confirmation." |
| Use active voice only | "Enter the customer's zip code" | "The zip code should be entered" |
| Name the exact UI element | "Click the blue 'Create Estimate' button" | "Create the estimate" |
| Include the why when it's not obvious | "Set status to 'Pending Dispatch' (this triggers the auto-assignment)" | "Set status to 'Pending Dispatch'" |
| Specify what "done" looks like | "You'll see a green confirmation banner." | (No confirmation that it worked) |

### Terminology Consistency

Pick one term for each concept and use it everywhere. Maintain a glossary if needed.

| Concept | Standard Term | Don't Use |
|---|---|---|
| The customer's request for service | "Job" (in ServiceTitan context) | Work order, ticket, service call, request |
| A potential sale from a lead | "Opportunity" (in Pipedrive context) | Deal, prospect, lead (when it's past qualification) |
| The visit where a tech evaluates the home | "Diagnostic" or "Survey" | Assessment, inspection, evaluation, site visit |
| The plan for equipment + price | "Estimate" or "Proposal" | Quote, bid, offer |

---

## Part 4: Change Communications

When announcing changes — new tools, process updates, org changes, policy shifts — use the ADKAR-informed framework below. The #1 reason change fails is that people don't understand why it's happening or what it means for them.

### The Change Communication Template

```
SUBJECT: [What's changing] — [Effective date]

WHAT'S CHANGING:
[1-2 sentences. Plain language. What specifically is different.]

WHY:
[1-2 sentences. The business reason. Tie to a goal or problem
the audience already knows about.]

WHAT IT MEANS FOR YOU:
[Role-specific impact. Be explicit:
 - "If you're a technician, here's what changes..."
 - "If you're a CSR, here's what changes..."
 - "If you're a manager, here's what changes..."]

WHAT YOU NEED TO DO:
[Specific actions. By when. With links to training/resources.]

TIMELINE:
[Key dates — announcement, training, go-live, full enforcement]

QUESTIONS?
[Who to contact. Specific person, not "your manager."]
```

### Sender Rules (from Prosci research)

The messenger matters as much as the message:

| Message Type | Best Sender | Why |
|---|---|---|
| "Why we're changing" (business reason) | **Senior leader / executive** | Employees need to hear the strategic rationale from the top |
| "How it affects your role" (personal impact) | **Direct manager / supervisor** | Employees trust their manager for personal-impact info |
| "How to do the new thing" (training) | **Subject matter expert or trainer** | Credibility on the mechanics |
| "You're doing great / here's what to adjust" (reinforcement) | **Direct manager** | Ongoing coaching |

### ADKAR Progression for Internal Comms

Map your communications to where people are in the change curve:

| ADKAR Stage | Employee Mindset | Communication Goal | Tactics |
|---|---|---|---|
| **Awareness** | "I don't know this is happening" | Create understanding that change is coming and why | Announcement email (from exec), all-hands mention, Slack post |
| **Desire** | "I see it's happening but I don't want to" | Build motivation — WIIFM (What's In It For Me?) | Role-specific impact docs, peer testimonials ("I tried it, here's what happened"), address fears directly |
| **Knowledge** | "I want to but I don't know how" | Teach the new way | SOP, training session, video walkthrough, reference card |
| **Ability** | "I know how but I'm still fumbling" | Enable practice and build confidence | Ride-alongs, shadowing, sandbox environments, "first 5 times" coaching |
| **Reinforcement** | "I can do it but might slip back" | Sustain the change | Manager check-ins, scorecards showing improvement, recognition, process audits |

### Common Change Communication Mistakes

| Mistake | Why It Fails | Fix |
|---|---|---|
| Announcing everything at once | Information overload — people retain nothing | Sequence communications: awareness → training → go-live |
| Skipping the "why" | People resist what they don't understand | Lead with the business reason, not the mechanics |
| Generic messaging to all roles | "This doesn't apply to me" → ignored | Segment by role and make the impact explicit |
| Email-only | Low-trust channel for high-impact changes | Use face-to-face (or video) for big changes, email for follow-up/reference |
| No feedback channel | Resistance goes underground | Include a named person for questions + a way to give anonymous feedback |
| Declaring victory too early | People revert when attention moves on | Plan 90 days of reinforcement, not 1 week |

---

## Part 5: Tone & Voice for Internal Content

### The Internal Voice Standards

| Attribute | What It Sounds Like | What It Doesn't Sound Like |
|---|---|---|
| **Peer-to-peer** | "Here's how this works and why it matters." | "As per company policy, all employees are required to..." |
| **Respectful of expertise** | "You already handle 40+ calls a day — this changes one step in your flow." | "This training will teach you how to answer the phone." |
| **Direct** | "This is mandatory starting March 1." | "We would encourage all team members to consider adopting..." |
| **Honest about difficulty** | "This will feel clunky for the first week. That's normal." | "This seamless transition will be easy for everyone." |
| **Specific** | "Open ServiceTitan → Jobs → click 'Reschedule'" | "Use the system to make the necessary updates." |

### Tone Matching by Content Type

| Content Type | Tone | Example Opening |
|---|---|---|
| SOP / process guide | Clear, neutral, precise | "This process handles rescheduling a same-day cancel." |
| Training material | Encouraging, practical | "By the end of this, you'll run a full diagnostic intake in under 4 minutes." |
| Policy change | Direct, empathetic, specific | "Starting March 1, all field quotes require manager approval over $15K. Here's why and how." |
| Team announcement | Warm, forward-looking | "Alex Moreno is joining as CT Regional Manager on the 15th. Quick intro below." |
| Performance feedback / coaching | Honest, constructive, evidence-based | "Your booking rate this week was 34%. Target is 55%. Let's look at the calls." |
| Urgent operational update | Brief, action-first | "All LI installs tomorrow are pushed to Thursday. Reason: permit delay. Your updated schedule is below." |

### Words That Work vs. Words That Don't

| Internal Comms Context | Use | Don't Use |
|---|---|---|
| Describing a new requirement | "Required starting [date]" | "We'd love it if you could..." |
| Explaining a process change | "This replaces the old process" | "This exciting new process enhances..." |
| Addressing a performance gap | "Current rate is 38%. Target is 55%." | "There's room for improvement in this area." |
| Introducing a new tool | "You'll use [Tool] for [task] starting [date]" | "We're thrilled to announce our partnership with..." |
| Acknowledging difficulty | "This is a big change. Here's support." | "This seamless transition..." |
| Referencing a deadline | "Due by Friday 5pm ET" | "Please complete at your earliest convenience" |

---

## Part 6: Training Material Formats

### Quick Reference Card (for field/phone staff)

One page. Laminate it. Stick it to a clipboard or tape it near a screen.

```
┌──────────────────────────────────────────┐
│ [TITLE: What This Covers]                │
│ [Role: Who uses this]                    │
├──────────────────────────────────────────┤
│ WHEN TO USE:                             │
│ [1 sentence trigger condition]           │
├──────────────────────────────────────────┤
│ STEPS:                                   │
│ 1. _______________                       │
│ 2. _______________                       │
│ 3. _______________                       │
│ (Max 7 steps)                            │
├──────────────────────────────────────────┤
│ IF STUCK: [Name] at [number/Slack]       │
└──────────────────────────────────────────┘
```

### Scenario-Based Training (for decision-heavy roles)

For CSRs, sales reps, and anyone making judgment calls:

```
SCENARIO: [Real situation, described in 2-3 sentences]

"A customer calls and says their AC stopped working last night.
 It's 94 degrees today. They want someone out within the hour
 and ask how much it will cost."

WHAT TO DO:
1. [The correct action]
2. [Why — one sentence]

WHAT NOT TO DO:
- [Common mistake + consequence]

WHAT TO SAY:
"[Exact script or talk track]"
```

### Process Walkthrough (for system training)

For ServiceTitan, Pipedrive, or any tool-based process:

```
GOAL: [What you'll be able to do after this]

SETUP: [What you need open/logged into before starting]

STEP-BY-STEP:
1. [Screenshot or description of where to click]
   → You should see: [what the screen looks like after]
2. [Next action]
   → You should see: [confirmation]
3. ...

COMMON MISTAKES:
- [Thing people get wrong] → [How to fix it]

PRACTICE:
- Try it now with [test scenario]. Your result should be [X].
```

---

## Part 7: Pre-Publish Checklist

Before finalizing any internal content:

- [ ] **Action test**: Can the reader do the thing after reading this? (If it's training/SOP)
- [ ] **"Why" check**: Is the reason for this process/change/policy stated in the first 3 sentences?
- [ ] **Role tagging**: Is it clear who this applies to? Is irrelevant info excluded for each role?
- [ ] **Verb-first steps**: Does every procedural step start with an action verb?
- [ ] **One action per step**: Are compound steps broken into separate numbered items?
- [ ] **Active voice audit**: Are all instructions in active voice? (Search for "should be" as a passive voice flag)
- [ ] **Terminology check**: Are you using the standard terms consistently? (Job, Opportunity, Diagnostic, Estimate)
- [ ] **Tone check**: Read the first paragraph aloud. Does it sound like a peer talking to a peer?
- [ ] **Specificity test**: Are tool names, button labels, field names, and deadlines exact?
- [ ] **"Done" state**: Does the reader know what success looks like after completing the steps?
- [ ] **Error handling**: Are the 2-3 most common mistakes addressed with fixes?
- [ ] **Feedback channel**: Is there a named person to contact with questions?
- [ ] **Banned word check**: Run against the personal-writing-SKILL.md banned list

---

## Calibration Examples

### SOP — Before (Wall of Text, Passive Voice, No Structure)

> When a customer calls to reschedule their appointment, the appointment should be looked up in the system and the relevant information should be verified. It is important to ensure that the customer's preferences are taken into account when selecting a new time. The system should then be updated accordingly and a confirmation should be sent to the customer. If there are any issues with availability, the matter should be escalated to the appropriate team member.

### SOP — After (Action-Oriented, Structured, Specific)

> **How to Reschedule a Same-Day Appointment**
> Applies to: CSRs | Updated: 2026-02-14 | Owner: Derek
>
> **When to use**: Customer calls to move an already-confirmed appointment.
>
> **Steps:**
> 1. Open the job in ServiceTitan → search by customer name or phone number.
> 2. Confirm the current appointment date and time with the customer: "I'm showing [date] at [time] — is that the one?"
> 3. Click "Reschedule" on the job card.
> 4. Offer the next 2-3 available slots: "I have [time] on [date] or [time] on [date]. Which works better?"
> 5. Select the new time → click "Confirm."
> 6. Verify the confirmation screen shows the updated time and the green checkmark.
> 7. Say: "You're all set for [new date/time]. You'll get a text confirmation in a few minutes."
>
> **If something goes wrong:**
> - No available slots this week → Offer to add them to the priority waitlist and explain they'll get a call if something opens up.
> - Job is locked / can't reschedule → Slack the dispatcher with the job number. Don't tell the customer "the system won't let me."

### Change Announcement — Before (Generic, No "Why", No Role Impact)

> Subject: New Process Update
>
> Hi Team,
>
> We're excited to announce that we'll be implementing a new process for handling estimates. This change is part of our ongoing commitment to operational excellence and continuous improvement. More details will be shared soon. We appreciate your flexibility and support as we roll this out.

### Change Announcement — After (ADKAR-Informed, Role-Specific)

> Subject: Estimates over $15K now need manager approval — starts March 1
>
> **What's changing:**
> Starting March 1, any residential estimate over $15,000 requires your regional manager's approval before it goes to the customer. Estimates under $15K — no change.
>
> **Why:**
> We had 4 pricing errors over $5K last quarter on large installs. This adds a 15-minute check that catches errors before they become margin problems.
>
> **What it means for you:**
> - **Sales / comfort advisors**: After building the estimate in ServiceTitan, Slack your RM with the estimate number. They'll approve or flag within 2 hours. Don't send to the customer until you get the thumbs-up.
> - **Regional managers**: You'll get 3-5 approval requests per week. Target: respond within 2 hours during business hours.
> - **CSRs**: No change for you. Estimates are still sent from the sales team.
>
> **Timeline:**
> - Feb 15: This announcement
> - Feb 22: 15-minute walkthrough (recorded, link to follow)
> - March 1: Live — all estimates over $15K require approval
>
> **Questions?** Ask Derek directly on Slack or email derek@hickory.com.

---

## Sources & Influences

Principles compiled from:
- **Malcolm Knowles** (*The Adult Learner*) — six principles of andragogy, self-direction, experience-based learning
- **Cathy Moore** (*Map It*) — action mapping, performance objectives over learning objectives, cutting unnecessary content
- **Prosci ADKAR Model** — Awareness, Desire, Knowledge, Ability, Reinforcement for change communications
- **David Kolb** (Experiential Learning Theory) — learning by doing, concrete experience → reflection → abstract conceptualization → active experimentation
- **Penn State Extension / FDA Group** — SOP writing standards, 3Cs (Clarity, Consistency, Conciseness)
- **Scribe / SwipeGuide** — SOP best practices, hierarchical format, plain language
- **Gallup research** — leader communication effectiveness and employee engagement during change
- **Albert Bandura** (Social Learning Theory) — observation, modeling, peer-based learning in teams
