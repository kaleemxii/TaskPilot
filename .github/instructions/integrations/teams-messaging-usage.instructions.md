---
description: Guidance for drafting and sending Teams chat or channel follow-up messages via browser (teams.microsoft.com/v2).
---

## Teams Messaging Usage Playbook

Purpose: Rapidly dispatch concise, contextual action or clarification messages derived from meeting followups with minimal formality while preserving source traceability.

### Access & Session
- Navigate to https://teams.microsoft.com/v2/ . If already signed in (teams UI + left rail visible), proceed automatically.
- For account picker/MFA, pause for user action.

### Message Type Selection
- 1:1 / Small Group Chat for direct owner nudge or clarification.
- Channel Post when wider team visibility or asynchronous decision logging needed.
- If uncertainty, default to private chat; escalate to channel only if action impacts >3 people or sprint scope.

### Locating / Opening Target Conversation
1. Use search bar (Ctrl+E) with recipient name or channel keyword.
2. Prefer existing thread; if none, open new chat (New Chat icon) and add participants.
3. For channel posts, choose correct channel then New conversation (avoid replying to old, unrelated thread).

### Draft Structure (Chat)
Line 1: @Owner – concise action statement.
Line 2: Context reference (Meeting Title Date) + optional link.
Line 3: Ask + due date OR confirmation request.
Optional: Bullet list (hyphen or *), max 3 items.
Final: Thanks / close (optional in short pings).

### Draft Structure (Channel Post)
Title (if supported) = Action: <Short Tag>
Body = Same 3-line pattern + bullets + Sources: list if >1.

### Grounding & Citations
- Always include meeting title or artifact name once.
- If quoting someone, limit to ≤15 words and wrap in quotes.
- Do not summarize unstated commitments.

### Multi-Message Sequencing
- If more than one action for same owner, merge into single message with bullet list unless separate urgency levels.
- Space sequential messages by ≥2s to allow UI updates.

### Formatting & Clarity
- Use simple markdown: *italic* for emphasis, **bold** sparingly (one keyword).
- Convert ambiguous dates ("next Friday") to explicit ("Fri 05 Sep") when visible in source; else keep original and mark [Confirm date].

### Approval Step
- For bulk actions: prepare all messages in a pending list (Message ID | Target | Preview (first 80 chars)).
- Send only those user approves (All or subset). No auto-sending without explicit approval list.

### Sending & Verification
1. Paste message into compose box; review for leftover brackets ([Unknown], [Confirm]).
2. Press Enter (or click Send). If Teams inserts a newline instead (Shift+Enter confusion), ensure actual send event (message appears in feed).
3. Verify message presence (text match) within conversation timeline; scroll if necessary.
4. Record timestamp + link (if accessible) in action tracking table.

### Error Handling
- If message fails (red retry icon), retry once after 3s; on second failure mark Failed and escalate.
- If wrong conversation opened (title mismatch), abort send and reopen correct target.

### Escalation: Switch to Email When
- Need attachments, external participants, formal approval, or lengthy (>6 lines) rationale.

### Anti-Hallucination & Safety
- Never generate private/sensitive info not on screen.
- Use [Clarify owner] if owner ambiguous.

### Completion Criteria Per Message
- Message visible in target chat/channel with correct @mentions.
- Action tracking table updated with status Sent.
