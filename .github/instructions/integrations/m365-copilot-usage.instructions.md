---
description: Guidance for querying Microsoft 365 Copilot (work chat) to extract grounded status, summaries, and action items.
---

## Microsoft 365 Copilot Usage Playbook

Purpose: Efficiently interrogate enterprise work graph (meetings, emails, chats, files) to pull factual, attributable snippets for status consolidation and followup drafting—without hallucination.

### Access & Session
- If Copilot work chat loads with the correct corporate account already visible, proceed automatically (no pause) per global login rule.
- If MFA or account picker appears, pause and request user confirmation.

### Tab & Conversation Management
- Open a NEW browser tab for every logically distinct query batch (different dimension: highlights vs risks vs action items) instead of stacking unrelated prompts in one conversation.
- Use the SAME conversation only for direct refinements (clarify, reformat, add sources) to preserve grounding.
- Name/label (mentally) each tab purpose; avoid >3 concurrent tabs (see Parallel Query Strategy) to limit cognitive load.
- Close tabs once their data is captured in consolidation tables to prevent accidental prompt reuse.

### Grounded Query Patterns
Use precise, scoped prompts. Prefer direct time windows + output schema.

1. Recent Meetings Summary
  Prompt: Summarize my last 3 project-related meetings today into: Decisions, Risks, Action Items. Cite each item with meeting title.
2. Action Items Extraction (Ground a specific meeting):
  Type '/' and select the meeting (e.g., /Recap). Then:
  Extract actionable followups with explicit owners and due dates (if stated). Return Markdown table: Item | Owner | Due | Source Quote.
3. Executive Status Seed:
  Provide top 3 delivery highlights this sprint with source citations (meeting/email/file). If insufficient data, list missing source types instead of guessing.
4. Risk Scan:
  Identify any schedule risks mentioned in the past 7 days of my meetings and emails. Output: Risk | Impact | Source | Mitigation (or Unknown).
5. Blockers Escalation:
  List blockers requiring leadership help from last 5 days of chats or meeting notes. Output: Blocker | Affected Project | Source | Unblock Next Step.

### Slash (/) Grounding
- Press '/' to open entity picker (meetings, emails, chats, files). Select the most relevant artifact before typing the rest of the instruction to constrain scope.
- When multiple similar meeting titles, pick the one labeled Recently attended or closest in time.
- If required artifact not listed, revert to a time-bounded general prompt (e.g., In meetings this week...).

### Output Discipline
- Always request structured tables for machine-mergable fields (Status, Risks, Action Items).
- Ask Copilot to cite source names (meeting title / file name / channel) inline; reject outputs lacking source columns (repeat with explicit: Include a Source column listing exact artifact titles).
- If Copilot replies with generalized statements without sources, immediately issue a refinement prompt: Re-run with explicit source citations; omit any item without a verifiable source.

### GPT-5 Escalation Criteria
Escalate by clicking "Try GPT-5" only when:
- Prompt spans 3+ analytical dimensions (e.g., highlights + risks + blockers + mitigations), OR
- Initial model returns Insufficient data / vague summaries, OR
- Need reasoning over conflicting signals (e.g., two meetings give different ETAs).
After escalation, re-issue the refined structured prompt exactly (copy/paste) and compare depth; prefer earliest satisfactory output to save tokens.

### Parallel Query Strategy
- Run at most 2–3 parallel browser tabs for: (A) Highlights, (B) Risks/Blockers, (C) Action Items.
- Avoid duplicative scope; each tab should target distinct deliverable.
- After all responses complete, consolidate fields into working table BEFORE narrative synthesis.

### Response Completion & Waiting
- Always wait until the response fully finishes ("Generating response" indicators disappear) before issuing a new prompt in that tab.
- Light responses typically <15s; allow up to 45–60s for multi-source scans before considering a stall.
- Stall handling: if >60s with no new tokens and a Stop generating button is available, stop and re-issue a narrower prompt (reduced timeframe or fewer sections).
- Do NOT chain a refinement while the original is still streaming; this can truncate content and lose citations.

### Handling Partial / Missing Data
- If Copilot states it lacks context, issue a clarifying follow-up: List the exact meeting titles or channel names you would need to answer fully.
- Record those missing items verbatim under Improvements.

### Verification Pass
For each extracted item, spot-check at least one cited source via manual navigation (open link / entity) if available; if discrepancy found, annotate item with [VERIFY].

### Anti-Hallucination Safeguards
- In every multi-part prompt, append: If uncertain, respond with 'Unknown' instead of inferring.
- Reject any output containing future commitments not present in cited sources.

### Rate / Latency Management
- If a response stalls (no progress > 20s) and Stop generating is available, stop then rephrase more narrowly (reduce time window or number of sections).

### Consolidation Handoff Fields
Capture the following normalized columns from Copilot outputs when possible:
| Type (Highlight/Risk/Blocker/Action) | Project | Description | Owner | Due/ETA | Impact | Mitigation/Next Step | Source | Verification |

Use empty string or Unknown (not N/A) for absent data.

### Completion Criteria (Per Query Batch)
- All target dimensions queried or marked with explicit missing sources.
- Structured table assembled with Source column populated per row.
- Items requiring verification flagged.
