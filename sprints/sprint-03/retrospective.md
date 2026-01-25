# Sprint 03 Retrospective

## What we planned
- Establish canonical JSONL sources for sprints, issues, and tasks.
- Build schema registry and validation pipeline.
- Implement workflow‑transition semantics for issues and tasks.
- Generate sprint analytics and prepare the Sprint 03 notebook.
- Produce mid‑sprint review and governance alignment artifact.

## What we achieved
- Canonical JSONL sources created, structured, and validated.
- Schema registry operational and integrated into the validator.
- Validator extended to enforce:
  - required fields
  - ID patterns
  - foreign keys
  - status values
  - workflow transitions
  - timestamp monotonicity
  - final‑status consistency
- Parquet generation pipeline restored and aligned with canonical sources.
- Sprint 03 analytics notebook scaffolded.
- Governance checkpoint reached successfully with validator enforcing v2 semantics.

## What didn’t go as planned
- One issue/task contains an illegal transition (`in_progress → done`) that surfaced only after workflow validation was enabled.
- JSONL formatting required correction after multi‑line edits introduced invalid JSONL structure.
- Timestamp parsing required compatibility adjustments due to environment differences.

## What we learned
- JSONL must remain strictly one‑line‑per‑object; multi‑line pretty‑printing breaks ingestion.
- Workflow semantics surface real data‑truth issues that must be corrected deliberately, not rushed.
- Validators must be robust to missing fields, NaN values, and environment‑specific timestamp formats.
- Governance checkpoints are effective at preventing silent drift in canonical truth.

## What we will improve in Sprint 04
- Add a task to correct workflow histories for affected Sprint 03 items.
- Add a task to extend or refine schema registry transition rules to reflect actual workflow.
- Add a task to generate the flow‑metrics table for Sprint 03.
- Add a task to finalize the Sprint 03 analytics notebook.
- Add a task to prepare the Sprint 04 planning artifact and initialize the new sprint cleanly.
