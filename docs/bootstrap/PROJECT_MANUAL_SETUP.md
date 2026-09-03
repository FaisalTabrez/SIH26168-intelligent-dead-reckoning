# GitHub Project Manual Setup

Project-v2 automation is currently unavailable because the authenticated token lacks `project` and `read:project`. Do not claim the project exists until an owner completes and verifies this procedure.

## Project

Create an owner-level private project named **SIH26168 Development Roadmap** and add all 128 repository issues.

## Fields

| Field | Suggested type |
|---|---|
| WP ID | Text |
| Parent WP | Text |
| Phase | Single select |
| Submission critical | Single select: Yes/No |
| Priority | Single select |
| Area | Single select |
| Owner role | Single select |
| Assignee | Built-in assignees |
| Start date | Date |
| Due date | Date |
| Estimated effort | Number or text |
| Evidence required | Single select: Yes/No |
| Scientific gate | Single select |
| Dependency status | Single select |
| Risk | Single select |
| Status | Built-in project status |

## Views

Create and verify these 14 views: Submission Critical, Roadmap, Backlog, Ready, In Progress, In Review, Blocked, At Risk, By Owner, By Milestone, Scientific Gates, Operations Queue, Post-Submission, and Done.

Recommended filters must use repository labels as the source of truth—for example `label:submission-critical`, `label:status:blocked`, `label:role:operations`, and `label:post-submission`. Roadmap uses milestone/due date; owner and milestone views group by their matching fields.

After setup, record the project URL, field identifiers, view names, issue count, visibility, and verification timestamp in `REPOSITORY_BOOTSTRAP_REPORT.md`.
