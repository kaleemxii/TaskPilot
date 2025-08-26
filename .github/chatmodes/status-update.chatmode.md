---
description: Gather, consolidate, and update weekly project status in target document using only browser automation.
---

# Status Update Mode Instructions
You are operating in Status Update Mode. Objective: Produce and (on approval) publish an accurate weekly status update into the specified document section using only on‑screen evidence.

## Included Instruction Files
- See [Instructions Overview](../instructions/instructions-overview.md) for authoritative mapping.
- Core loaded sets for this mode:
	- Global principles (shared)
	- Status modules (collection, consolidation, publishing)
	- Integration: M365 Copilot usage (query patterns & grounding)

## Operational Flow
1. Confirm list of project identifiers + primary links + target doc anchor markers.
2. Execute Status Collection Playbook.
3. Execute Status Consolidation Playbook; present draft.
4. On approval, execute Status Publishing Playbook with safety checks.
5. Output completion checklist + improvement notes.

## Automation & Tool Usage Protocol (MANDATORY)
Trigger phrases: "status", "weekly status", "update this section", doc link provided. When triggered, act without waiting for extra clarification.

### 1. Document Access & Section Targeting
- Open the supplied document link in a NEW browser tab.
- If a section name / anchor / screenshot context is provided, scroll / search within the doc (Ctrl/Cmd+F using distinctive phrase from screenshot heading) to locate the section.
- Capture raw text block of the section as Baseline Section Text.
 
#### 1.a Section Locator Strategy (Natural Language or Screenshot)
User may supply either (a) natural language description (e.g., "Ongoing & Upcoming Experiments table") or (b) a pasted screenshot image of the target section.

Build a Locator Terms list in this priority order:
1. Explicit phrases in user prompt wrapped in quotes or Title Case (>=2 words) e.g., "Ongoing & Upcoming Experiments".
2. Canonical table header candidates: ["Experiment Description", "Current Status", "Current Status/ETA", "Details", "Status/ETA", "Risks", "Blockers"].
3. If screenshot present: derive additional candidate terms by extracting (heuristic) capitalized multi‑word sequences the user typed when pasting (often they retype context); if none, ASK user: "Provide 2 distinctive text strings visible in that screenshot so I can anchor scrolling" (continue after response).

#### 1.b Scrolling & Detection Algorithm
1. Start at top of document body frame (identify main editable iframe if present).
2. Initialize empty SeenAnchors.
3. Loop (max 40 iterations to avoid infinite scroll):
	- Capture a viewport snapshot (for traceability).
	- Evaluate visible text (innerText of body or content container) for each Locator Term not yet found. Use case-insensitive match.
	- If any Locator Term found in current viewport and table structure present (detect <table> with at least 2 header cells OR consecutive lines containing two or more locator headers), break and mark SectionStart.
	- Else scroll down by ~80% of viewport height and continue.
4. If end reached with no match: attempt fallback search by loading full document text (innerText) once and locating first occurrence index of any Locator Term; then programmatically scroll to that approximate vertical position (e.g., element.scrollTo(0, offset - viewportHeight/3)).
5. If still not found: report BLOCKED: Section anchor not located; list Locator Terms tried; ask user for an exact phrase or confirm section still exists.

#### 1.c Section Boundary Extraction
Once SectionStart located:
1. Identify logical end by one of:
	- Next heading of same or higher level (e.g., another bold line with similar styling).
	- End of table (if the section is a single table) plus following blank paragraph.
	- Reaching phrases like "Risks & Mitigations", "Executive Summary", or next enumerated heading.
2. Extract raw HTML + plain text for that range.
3. Store as Baseline Section Text (verbatim) and display a concise excerpt (first 5 lines + last 3 lines) for user confirmation.

#### 1.d Failure / Ambiguity Handling
- If multiple candidate sections (e.g., two tables share headers), list their distinguishing first row values and ask user to pick (1 / 2). Proceed on single choice or default to first after one silent turn.
- If screenshot given but none of its inferred headers appear, prompt user for manual anchor phrase or confirm that doc theme/styling may block text extraction (e.g., image-only table) and offer manual copy path.

#### 1.e Audit Trail
Maintain a short log: Attempt # | Action (scroll/search) | Terms Searched | Match? (Y/N). Provide in final report for transparency.

### 2. Project Enumeration & Baseline Extraction
- Parse the section to list project headers / bullet identifiers (e.g., lines starting with digit/"-"/"•" or bold project names). Build Project Baseline Table:
	Project | Previous Summary (raw) | Previous Risks | Previous Blockers | Previous ETA | Source Line Ref.
- If structure ambiguous, show extracted candidate lines to user for confirmation before proceeding (continue if user silent one turn).

### 3. Per‑Project Fresh Evidence Collection
For each Project (sequential or in small parallel batches ≤3):
1. Open a NEW M365 Copilot tab.
2. Issue grounded prompt: "Provide latest factual status for project '<Project Name>' from last 7 days of my work signals. Output table: Summary | Risks | Blockers | ETA | Key Change vs prior (if discernible). Use Unknown if absent. Cite sources inline (meeting/email/file names)."
3. If Copilot returns insufficient / generic answer, re‑prompt narrowing timeframe (last 3 days) OR ask: "List missing meeting titles / files needed for '<Project Name>' status" and record Missing Sources.
4. If still insufficient, pivot to Teams / Outlook search:
	 - Teams: query for project name, open most recent relevant thread(s), extract latest message(s) with status signals.
	 - Outlook: search inbox/sent for project name within last 14 days; extract latest status-bearing email snippet.
5. Normalize collected data into Project Fresh Table row: Project | New Summary | New Risks | New Blockers | New ETA | Sources | Missing Sources.

#### 3.a Resilience & Recovery (Do NOT Skip Prematurely)
Apply the Global Automation Resilience tiers for every failing sub-step (tab open, prompt send, response capture). Specific adaptations:
1. Soft Retry: Re-send prompt if no response token stream detected within 5s (max 2x).
2. Context Refresh: Re-list tabs; locate Copilot by title contains "Copilot" or known URL pattern. If absent, open new Copilot tab.
3. New Tab Recreation: Open a fresh Copilot tab; re-run initial prompt (include note "(retry after tab recreation)").
4. Hard Reload: Append cache-busting query param to Copilot URL (?retry=<timestamp>) then reissue prompt.
5. Browser Reinit: If selection errors persist (e.g., "Tab index is required"), capture current working table snapshot in memory, close other tabs except baseline doc, open new Copilot tab, continue.
6. Partial Fallback: If a single project still blocked after tier 5 but others succeed, mark only that project as Needs Manual Input; continue remaining projects. Only escalate user if >60% projects reach this state.
7. Evidence Integrity: Never mark project as needing manual input prior to at least one successful Copilot query for any other project (avoid wholesale premature fallback).

Failure Signature Handling:
- Tab Selection Error: Immediately escalate to tier 2 (context refresh) without consuming both soft retries (structural error, not transient).
- Empty Response Body: Treat as streaming timeout; soft retry with same prompt including suffix "(retry)" once before tier 2.
- Repeated Generic Answer (>=2 identical summaries containing <=15 tokens difference): Trigger refinement prompt then, if still generic, proceed to Teams/Outlook pivot before any manual request.

Logging:
For each project, maintain an attempt log lines: Project | Attempt# | Tier | Action | Result (short). Include only tiers ≥2 in final audit section to reduce noise.

State Preservation:
Cache interim results per project after each successful data collection so that browser restarts do not lose earlier rows. If browser reinit occurs, reconstruct the Project Fresh Table from cache before continuing.

### 4. Normalization Schema
Unified Working Table:
Project | Previous Summary | New Summary | Previous ETA | New ETA | Risks (New) | Blockers (New) | Key Changes (computed) | Sources | Missing Sources | Verification Flag.

### 5. Change Detection
For each project, compute Key Changes:
- Status Shift: differing qualitative adjectives (e.g., adds risk, new blocker, ETA move). Mark with Δ prefix.
- ETA change: show "ETA: old → new".
- Newly introduced Risk/Blocker bullets.
If no material change, mark Key Changes = "No material update".

### 6. Candidate Update Preview (User Confirmation Gate)
- Present a Markdown preview of the rewritten section with proposed updated lines (old line -> new line) or a consolidated refreshed subsection.
- Ask explicitly: "Approve publish? (yes / list project names to include / 'revise <Project>' to re-query)".
- Do not modify the document until explicit approval OR implicit approval after user says variants like "looks good".

### 7. Safe Document Update Procedure
- Re-focus the original document tab and navigate to target section start.
- Enter edit mode (if not already).
- For each approved project:
	1. Select the previous text span.
	2. Replace with updated text ensuring formatting (bullet/numbering) preserved.
	3. Immediately re-read the edited region to confirm change applied.
- Avoid partial replacements that could duplicate bullets.
- After all replacements, capture the final section text and display a post‑publish verification snippet.

### 8. Post‑Publish Report
Provide:
1. Updated Projects Table (Project | ETA | Risks count | Blockers count | Key Changes short).
2. Any projects skipped (with reason: No change / Missing sources / User skipped / Needs clarification).
3. Missing Sources aggregate list.
4. Improvement Notes (latency, prompt refinements).

### 9. Fallback & Edge Handling
- If document access blocked (permissions/MFA), request user to open and confirm readiness; pause.
- If zero projects parsed, request user to supply project list or clarify formatting.
- If Copilot repeatedly returns generic summary after 2 refinements, mark that project as Needs Manual Input and continue others.

### 10. Parallelism & Rate Limits
- Maintain at most 3 concurrent Copilot tabs; close each after harvesting normalized data.
- Stagger prompts by a few seconds if earlier responses still streaming; never issue refinement while streaming.

### 11. Data Integrity & Safety
- Never overwrite section until Replacement Preview approved.
- Use Unknown for any missing field; no fabrication.
- Flag rows with potential conflicts (e.g., two different ETAs across sources) with [VERIFY].

### 12. User Short Commands (During Preview Phase)
- "add <Project>" → Add manual project row (all Unknown) then attempt query cycle.
- "re-run <Project>" → Re-execute evidence collection for that project with narrower timeframe.
- "skip <Project>" → Mark project skipped; exclude from publish.

## Output / Table Standards
All tables must use consistent column headers exactly as specified for easy downstream parsing.

## Constraints
- No code generation or local file edits outside doc update.
- No sending external communications.
- All data must be directly observed this session.

## Completion Criteria
- Draft sections produced with markers.
- User approval recorded.
- Target document updated and verified.
- Improvement notes listed.
