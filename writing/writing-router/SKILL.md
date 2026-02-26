---
name: writing-router
description: When the user needs written content, route to the right writing skill based on audience. The personal-writing skill (always loaded) provides the base layer — voice, anti-AI patterns, banned words. This router adds audience-specific structure on top.
---

# Writing Skill Router

The **personal-writing** skill is always active as the base layer (voice, banned words, rhythm, anti-AI patterns). When content needs audience-specific structure, invoke the right skill below.

## Audience Routing

| Audience | Skill | Invoke | Adds... |
|---|---|---|---|
| **Executives / board / investors** | Executive Communication | `/exec-comm` | Pyramid Principle, SCQA framing, action titles, MECE, slide/memo/email formats |
| **Hickory employees / field staff / CSRs** | Internal Training & Comms | `/internal-comms` | Adult learning principles, action mapping, SOP structure, ADKAR change comms |
| **Customers / prospects** | Sales Copywriting | `/sales-copy` | PAS/AIDA/BAB frameworks, awareness-level matching, VoC discipline, trust architecture |

## Process Documentation

| Content type | Skill | Invoke | Adds... |
|---|---|---|---|
| **SOPs / runbooks / playbooks / checklists** | SOP Creator | `/sop-creator` | Structured SOP templates, decision trees, onboarding guides, process formalization |

## How to Use

1. Identify the audience for the content
2. Tell the user which skill matches and why
3. Wait for them to invoke before proceeding
4. The invoked skill will layer on top of the always-active personal-writing rules
