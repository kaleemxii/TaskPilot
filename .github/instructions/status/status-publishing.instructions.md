---
description: Safely apply consolidated status sections into the target document section.
---

## Status Publishing Playbook
1. Navigate to the target document URL.
2. Locate the designated status section (user provides anchor/heading or HTML id).
3. Capture existing content between each defined marker pair; keep a backup copy text block.
4. Replace only the inner content of each marker pair with the newly generated section content.
5. Present a diff summary (lines removed/added counts per section) to user.
6. On approval, apply changes (e.g., edit + save / publish) but do NOT alter other document regions.
7. Confirm success by reloading page and verifying updated marker contents.
8. Log completion checklist.
