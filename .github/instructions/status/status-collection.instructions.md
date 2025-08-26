---
description: Collect raw per-project status data from provided project list and links.
---

## Status Collection Playbook
1. Initialize an empty table header: | Project | Status | % | ETA | Risks | Blockers | Notes | Source |
2. For each provided project (in given order):
   - Navigate to primary status source link.
   - Verify page loaded (look for project name text).
   - Extract visible indicators: textual status (normalize to Green/Amber/Red if color badges) or mark Unknown.
   - Locate progress metric (% complete, story points done / total) if displayed.
   - Identify ETA (date string) or milestone; if absent search within page for patterns (ETA, Target, Due, Release).
   - Scan for risk/blocker sections, badges, or keywords (risk, blocker, issue, delay). Capture concise phrases.
   - Append a row to the table with Source = page type (e.g., "GitHub Project", "Confluence Page").
   - If data missing, optionally open related communication link (Teams/Email thread) and attempt to infer updates; only extract explicit statements.
3. After first pass, list projects with critical Unknown fields and optionally re‑attempt focused retrieval.
4. Do not synthesize narrative yet; stay in raw table mode.
