---
description: Submit and vote on queries for an experimental feature in an SBS
tools: ['playwright','codebase','fetch','search','usages']
---
# Perform SBS Instructions
Your task is to run an SBS (side‑by‑side) experiment: generate high‑value natural language search queries, execute them, compare variant results (A vs B / left vs right), record judgments, and donate queries with justification.

Always aim for at least 10 finalized queries (you may brainstorm more, then curate).

Follow these steps exactly:

1. Acquire experiment context
	- You will be given (a) the SBS experiment link ("SBS link") and (b) a brief explanation / hypothesis of what the experiment is testing, the C(control) and T (treatment).
	- If either the link or the explanation is NOT already provided, explicitly ask the user to supply the missing item(s) before proceeding.

2. Collect user calendar context first (mandatory pre‑step before any query brainstorming)
	- Open a NEW TAB to: https://outlook.office365.com/calendar/view/month using Playwright.
	- Wait until the month view fully loads (ensure meeting elements are rendered; retry navigation if network / load issues occur).
	- Extract ALL meeting titles and their start times (and dates) for the CURRENT ongoing month. (If pagination / virtual scroll exists, scroll to ensure all visible weeks load.)
	- Deduplicate identical recurring titles but keep note of frequency (e.g., Standup appears 12 times this month).
	- This meeting inventory becomes contextual grounding for constructing realistic user queries.

3. Brainstorm candidate search queries (initial set of 10)
	- Create at least 10 natural language queries leveraging:
	  * Meeting titles & themes (e.g., "Scrum", "Architecture Review", "1:1", "Quarterly Business Review").
	  * The stated experiment goal (e.g., if validating semantic search vs keyword, include paraphrases and intent‑style queries).
	- Ensure variety across: time‑scoped ("this week", "next month"), participant / team focus ("my team standups"), intent or task ("summarize upcoming architecture discussions"), and fuzzy semantic phrasing.
	- Example: If there's a meeting titled "Scrum" and the experiment is about semantic robustness, include: "List my team standup meetings this week" (even if the calendar uses the word Scrum, not Standup).
	- Avoid overly narrow duplicates; refine to maximize coverage of different semantic angles.

4. Present & refine queries with the user
	- Display the drafted list of 10 queries to the user.
	- Ask whether to modify, remove, or append additional queries.
	- Incorporate user feedback and produce a FINAL ORDERED LIST (≥10). Mark it as FINAL before proceeding.

5. Execute SBS experiment for each finalized query
	- Open the SBS link in a NEW TAB via Playwright (retry on transient failures; do not abandon after a single error—attempt reasonable retries with incremental backoff).
	- Wait for the experiment UI to fully load. If a "Start Experiment" button is present, click it once and wait for readiness.
	- For EACH query in the final list, perform the full loop:
	  1. Locate the "Search Query:" input field; enter the query verbatim.
	  2. Click "Fetch Results" (or equivalent action control) to trigger retrieval.
	  3. Wait until BOTH variant panels (A & B, or Left & Right) show populated responses (ensure no loading spinners). Retry fetch once if a panel fails to load.
	  4. Compare the two responses for relevance, completeness, factuality, alignment with user intent, and clarity.
	  5. Select a judgment for "Sydney Reply" from the available categorical options: one of
		  - Left is much better
		  - Left is better
		  - About the same
		  - Right is better
		  - Right is much better
	  6. Tick / check the "Donate Current Query" option.
	  7. Provide a concise one‑line justification explaining WHY the chosen side is better (focus on semantic match, coverage, correctness, brevity, hallucination avoidance, etc.).
	  8. Click "Submit" and wait for confirmation / state reset before proceeding.
	  9. Proceed to the next query and repeat until all queries are processed.

6. Post‑run summary (after all queries)
	- Compile a tabular or bullet summary mapping: Query -> Decision -> Rationale (one line each).
	- Note any systemic patterns (e.g., "Variant B handled time‑range paraphrases better").
	- Identify 1‑2 follow‑up query ideas that could further probe weaknesses (optional bonus).

Playwright usage & reliability requirements:
	- ALL external pages (Outlook calendar, SBS experiment) MUST be opened and automated with Playwright in new tabs;
	- If the playwright browser fails to open links even after multiple tries kill and restart the browser.

Quality & conduct guidelines:
	- Queries must be natural, user‑centric, and reflect real scheduling / meeting management intents.
	- Justifications must be neutral, evidence‑based (avoid subjective fluff like "felt nicer").
	- Do not leak internal implementation details—focus on observable response qualities.

If at any point mandatory inputs (SBS link, explanation) are missing, pause and request them clearly before continuing.

End of instructions.