---
description: Overview of instruction file hierarchy and how each module is used by chat modes.
---

# Instructions Overview

This document maps every instruction module to its purpose and the chat modes that consume it. It enables automated selection of the right sub‑playbook for a given sub task (status vs. followups, integrations, global principles).

## Directory Structure
```
.github/
  copilot-instructions.md                # Global workspace-wide guardrails
  instructions/
    global-operational-principles.instructions.md
    status/
      status-collection.instructions.md
      status-consolidation.instructions.md
      status-publishing.instructions.md
    followups/
      followup-identification.instructions.md
      followup-context-gathering.instructions.md
      followup-drafting.instructions.md
      followup-review-and-send.instructions.md
    integrations/
      m365-copilot-usage.instructions.md
      outlook-email-usage.instructions.md
      teams-messaging-usage.instructions.md
  chatmodes/
    status-update.chatmode.md
    meeting-followups.chatmode.md
```

## Global Files
- `copilot-instructions.md`: High-level role, core principles, safety, data integrity, output style; applies to all chat interactions.
- `global-operational-principles.instructions.md`: Shared execution norms (stepwise, Unknown usage, working tables, verification).

## Status Workflow Modules
| File | Purpose | Consumed By |
|------|---------|-------------|
| status-collection.instructions.md | Enumerate project signals (issues, docs, chats) & capture raw fields | status-update |
| status-consolidation.instructions.md | Normalize & merge raw fields into structured status table | status-update |
| status-publishing.instructions.md | Safely insert/update status in target document | status-update |

## Followups Workflow Modules
| File | Purpose | Consumed By |
|------|---------|-------------|
| followup-identification.instructions.md | Extract user-specific action items & classify ownership | meeting-followups |
| followup-context-gathering.instructions.md | Pull minimal clarifying facts for each approved action | meeting-followups |
| followup-drafting.instructions.md | Draft email / Teams messages for actions | meeting-followups |
| followup-review-and-send.instructions.md | Approval + controlled sending & final reporting | meeting-followups |

## Integration Modules
| File | Scope | Key Capabilities | Used By |
|------|-------|------------------|---------|
| m365-copilot-usage.instructions.md | Microsoft 365 Copilot (work chat) | Tab strategy, grounded queries, waiting, escalation | both |
| outlook-email-usage.instructions.md | Outlook Web | Draft vs send safety, formatting, recipients handling | meeting-followups |
| teams-messaging-usage.instructions.md | Teams Web | Channel/chat drafting & safe send | meeting-followups |

## Selection Logic (for Automation)
When a user request text includes:
- "status" or "weekly update" → Load status collection + consolidation + publishing + global principles + m365.
- "followups", "action items", "meeting followups" → Load followup modules + global principles + m365 + (Outlook/Teams for drafting stage).
- Mixed request (mentions both status and followups) → Load all relevant status + followup modules and integrations; perform status first unless user specifies otherwise.

## Standard Output Tables
- Status: Project | Summary | Status (Green/Amber/Red) | % Complete | ETA | Key Risks | Blockers | Last Updated Source.
- Actions: Action ID | Description | Owner | Ownership Type | Due Date | Channel | Source | Notes | Status.

## Escalation & Fallback References
- For missing action items: see fallback section in followup-identification.
- For stalled Copilot responses: see Response Completion & Waiting in m365-copilot-usage.
- For zero-data remediation: meeting-followups chat mode defines remediation draft generation.

## Maintenance Guidelines
1. Add new workflow modules under a dedicated subfolder and list them here.
2. Keep file purpose statements concise (<= 1 line) for quick programmatic parsing.
3. Update chat modes to mention ONLY high-level grouping plus link to this overview (so additions auto-discoverable).

## Quick Reference Mapping
| Category | Primary Files | Chat Modes |
|----------|---------------|-----------|
| Status | status-* | status-update |
| Followups | followup-* | meeting-followups |
| Integrations | m365 / outlook / teams | both (where applicable) |
| Global | copilot-instructions + global-operational-principles | all |

## Change Log (Manual)
- v1: Initial overview created (adds explicit mapping & selection logic).
