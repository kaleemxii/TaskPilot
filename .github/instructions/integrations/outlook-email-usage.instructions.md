---
description: Guidance for drafting, staging, and sending follow-up emails in Outlook Web (outlook.office365.com) via browser automation.
---

## Outlook Email Usage Playbook

Purpose: Create accurate, source‑grounded follow-up emails (from meeting actions or status needs) with minimal user friction while enforcing approval and safety.

### Access & Session
- Navigate to https://outlook.office365.com/mail/ . If the correct corporate account mailbox loads (inbox visible), proceed automatically.
- If account picker or MFA is presented, pause and request user action.

### Compose Workflow (Draft Phase)
1. Click New mail (or equivalent compose button) to open a fresh draft pane.
2. Populate fields in this order to reduce accidental send:
   - To: Insert primary recipient(s). If multiple owners, include all; defer broad CC until draft approved.
   - (Optional) CC: Only after user approval or if provided explicitly in action item context.
   - Subject: Prefix with concise category keyword (Follow-up:, Action Required:, Info:) + short synopsis.
   - Body: Follow the standard structure (see Template) with placeholders for missing data.
3. NEVER click Send before explicit approval list includes this draft.
4. Save draft implicitly (most autosave). If manual Save required, trigger it.

### Standard Body Template
Line 1: Context (meeting name / source + date) – one sentence.
Line 2–3: Specific ask or commitment needed (what + by when + success definition).
Optional: Bullet list for sub-tasks (max 5 bullets).
Closing: Appreciation + invitation for clarification.
Signature: Use existing auto signature; do not modify.

### Data Grounding & Citations
- Cite original source inline on first mention (e.g., (Design Sync 27 Aug)).
- For multi‑source summary emails list Sources: at end if >2.
- Do not include any metric or date not present in upstream artifacts; mark [Unknown] instead of guessing.

### Refinement Prompts (Using M365 Copilot before Draft)
- Ask Copilot for a concise summary or risk articulation BEFORE composing if context unclear.
- Example pre‑prompt: Summarize key decisions from <meeting title> focusing on owner commitments and dates.

### Approval & Sending
1. Maintain a table of pending drafts: Draft ID | Subject | To | Ready? | Missing Fields.
2. After user selects drafts to send, re-open each draft tab/pane and re‑verify:
   - To field non-empty and matches table.
   - Subject unchanged (unless user-provided edits).
   - Body contains no [Unknown] unless user accepted.
3. Click Send; wait for confirmation (e.g., toast or draft pane closes). If confirmation absent after 8s, check Sent Items for subject.
4. Update status to Sent with timestamp.

### Error Handling
- If send fails (toast error), retry once after 3s; on second failure, mark Failed and surface reason.
- If recipient not found / address suggestion list appears, choose first exact match; otherwise pause for clarification.

### Anti-Hallucination Safeguards
- Do not elaborate beyond extracted context; no speculative promises.
- Replace ambiguous verbs ("fix soon") with precise ask or mark [Clarify].

### Escalation Rules (When to Email vs Teams)
- Use Email when: multiple stakeholders, external recipients, formal record, or attachments required.
- If a draft is <3 sentences and only internal single recipient, consider redirecting to Teams (ask user).

### Completion Criteria Per Email
- Stored draft OR sent confirmation.
- Table updated with final status.
- Any unresolved placeholders listed for user.
