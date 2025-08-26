---
description: Identify actionable followups from meeting artifacts (calendar entries, notes, chat threads).
---

## Followup Identification Playbook
1. For each meeting (today or previous day): open notes transcript or chat summary.
2. Scan for explicit action patterns ("AI:" "Action:" verbs + owner + date; imperative sentences; questions assigned) BUT capture ONLY actions where:
	- Owner is explicitly the user (name/alias/pronoun referring to user), OR
	- Owner is unspecified/ambiguous and the task logically falls to the user (e.g., user facilitated meeting, user previously tracked topic), OR
	- User must proactively follow up with another person to unblock their own committed deliverable (dependency task). Mark these as Follow-up Needed.
	(Do NOT list general team actions with clearly different owners unless user must chase them.)
3. Normalize action fields: Action ID (incremental), Description, Owner (User / External / Unknown), Ownership Type (Direct | Dependency | Clarify), Due Date (or Proposed), Channel (Email/Teams/None if purely personal), Source (meeting title + timestamp).
4. If owner unspecified but user intends to take it, set Owner = User and Ownership Type = Direct. If unsure whether user owns it, set Ownership Type = Clarify (prompt user later) and retain original ambiguous text in a Notes column.
5. Exclude non‑action discussion; exclude purely informational items with no user obligation.
6. Present a filtered table (user-specific only) for review before drafting communications. Provide a separate Optional Others count (not listed) if many excluded actions were detected.
7. Fallback segmentation when no user-relevant actions found:
	- a) Narrow time window (e.g., last 3 days, then prior 4 days) and re-run extraction.
	- b) Pivot sources: search shared files ("Meeting Notes", "Action Items", "Sprint Planning") and Teams chats for verbs (update, deliver, prepare, send, finalize, review).
	- c) If still empty, list Missing Sources (calendar titles, channels, file names) explicitly instead of guessing actions.
8. Re-prompt strategy for narrative-only responses: issue a strict instruction to return ONLY a Markdown table with defined columns using "Unknown" for absent fields; no prose; ensure Owner filtering (exclude rows where owner clearly != user unless dependency follow-up is required).
9. Escalation: after two empty passes with clear available meeting artifacts, escalate model (if option) or flag Need Transcription Access before proceeding to drafting.
10. Integrity: never fabricate owner or due date—prefer Unknown placeholders; do not merge distinct actions; one row per discrete commitment; never relabel another person’s clearly owned action as user-owned (instead classify as Dependency if user follow-up required).
11. Output Columns (minimum): Action ID | Description | Owner | Ownership Type | Due Date | Channel | Source | Notes (optional) | Status.
