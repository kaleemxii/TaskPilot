---
description: Transform collected raw project table into structured narrative status sections.
---

## Status Consolidation Playbook
1. Validate raw table completeness; highlight any remaining Unknown fields inline (e.g., "ETA: Unknown – awaiting confirmation").
2. Derive Executive Summary (max 3 bullets): overall progress sentiment, notable risk, upcoming key milestone.
3. For each project row, produce a bullet: Project Name – current status (Status, % complete, ETA) + one risk or blocker if present.
4. Aggregate risks: list distinct risks with affected projects and proposed mitigation (if visible; else mark Pending).
5. Upcoming Milestones: list any ETAs within next 2 weeks chronologically.
6. Add Improvements section (process gaps / access issues) at end.
7. Prepare final Markdown sections with stable anchors:
   <!--STATUS:EXEC_SUMMARY--> ... <!--/STATUS:EXEC_SUMMARY-->
   <!--STATUS:PROJECTS--> ... <!--/STATUS:PROJECTS-->
   <!--STATUS:RISKS--> ... <!--/STATUS:RISKS-->
   <!--STATUS:MILESTONES--> ... <!--/STATUS:MILESTONES-->
   <!--STATUS:IMPROVEMENTS--> ... <!--/STATUS:IMPROVEMENTS-->
8. Await explicit user approval before publishing to target doc.
