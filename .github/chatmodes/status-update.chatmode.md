---
description: Update the doc with latest updates on the experiments
tools: ['playwright','codebase','fetch','search','usages']
---
# Status Update Instructions
Your task is to identify the experiments from the given section of the doc and use m365 copilot to figure out the latest status on each of those and update that back into the doc.
.

Follow these steps exactly:

Core end-to-end workflow (do not skip any step, do not give up early):
1. Input acquisition:
	- You will be provided with a doc URL and a section reference (may arrive as text OR as an image describing the section header / nearby text).
	- If either the doc URL or a clear section reference is missing, explicitly ask the user once at the start; otherwise proceed without further clarification requests.
2. Open the doc:
	- Open the provided doc URL in a new browser tab.
	- Wait until the page fully loads (main content present).
	- Navigate to the target section using in‑page search by going to"View -> Navigation -> Find" to locate it, or do a Ctrl+F within the text content, or scroll and capture screenshots as you progress, until the section header or unique anchor text is detected.
	- Make sure the right section is identified by cross verifying with user given content, as there can be multiple instances of similar headers.
3. Section parsing:
	- Once the correct section header is located, capture all listed experiments beneath it until a logical boundary of the table content
	- Normalize each experiment into a list: ExperimentName | RawLine/Paragraph Source Snippet.
4. For each experiment (process sequentially):
	a. Open https://m365.cloud.microsoft/chat/ in a NEW tab (one tab per experiment so prior context does not leak).
	b. Handle any captcha / login prompts using available on‑screen controls (apply recovery tiers before declaring difficulty).
	c. Once chat input is ready, submit a concise query requesting: latest status, succinct ETA(s), blockers, ring / rollout phase specifics, and any notable changes since last known update for <ExperimentName>. Example query: "Provide a short 2 line summary of the latest concise status for the <ExperimentName> experiment: current state, any blockers, ETA(s), ring / rollout timeline details. Return factual, up-to-date info only." Adjust wording if needed for clarity.
	d. Wait until the response fully completes (e.g., streaming finished and any pause/stop button disappears) before extraction.
	e. Extract the full response text verbatim (retain source tab reference) and store it.
	f. Derive a one‑line distilled status: (<ExperimentName>): <Concise status with ETA(s) + blocker summary + ring phase>. Keep under 160 characters if possible; preserve key dates and risk terms.
	g. Close or leave the tab idle; proceed to next experiment with a fresh chat tab (avoid reusing prior chat threads to prevent context pollution).
5. Consolidation phase:
	- After all experiments are processed, present a table/list of ExperimentName -> One‑liner to the user for confirmation.
	- Do NOT ask the user for clarifications earlier unless a critical missing input prevented initial navigation (see step 1). Gather all one‑liners first.
6. User confirmation:
	- Await user modifications or approval. Incorporate any edits directly into the one‑liner set.
7. Doc update:
	- Return to the original doc tab, reopen in new tab if fails.
	- Insert the status as `[Latest on <Date>]: <Concise status with ETA(s) + blocker summary + ring phase>`, a bullet point against <ExperimentName>
	- Verify if the status was added correctly by re-reading the updated section, and fix as necessary.

Resilience & non-abandonment policy:
	- Never give up mid-flow; Complete it to the end.
	- You would have all the necessary edit permissions on the doc, so make the changes directly.
	- Capture screenshots when you hit failures to understand the context.
	- Only request additional user input after ALL experiments have one‑liners. Early prompting for help is prohibited.
	- If authentication barrier (e.g., MFA) cannot be bypassed programmatically, pause and report precisely.


Playwright usage & reliability requirements:
	- ALL external pages (m365 copilot and doc links) MUST be opened and automated with Playwright in new tabs;
	- Websites take time to load; ensure to wait for the page to fully render before interacting.
	- If the playwright browser fails to open links even after some 10 tries kill and restart the browser.

End of instructions.