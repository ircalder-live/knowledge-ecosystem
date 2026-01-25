import json
import re
import sys
import argparse
import pandas as pd
import datetime
from pathlib import Path

DATA_DIR = Path("data")
REGISTRY_PATH = Path("frameworks/schema_registry.json")

# ------------------------------------------------------------
# Load JSONL safely
# ------------------------------------------------------------
def load_jsonl(path):
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return pd.DataFrame(records)


# ------------------------------------------------------------
# Load schema registry
# ------------------------------------------------------------
def load_registry():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ------------------------------------------------------------
# Validation helpers
# ------------------------------------------------------------
def error(msg):
    print(f"VALIDATION ERROR: {msg}")
    sys.exit(1)


def validate_required_fields(df, required, label):
    missing = [f for f in required if f not in df.columns]
    if missing:
        error(f"{label} missing required fields: {missing}")


def validate_id_pattern(df, pattern, field_name, label):
    regex = re.compile(pattern)
    for _, row in df.iterrows():
        value = row[field_name]
        if not regex.match(value):
            error(f"{label} invalid {field_name} '{value}' does not match pattern {pattern}")


def validate_status_history(record, schema, registry):
    history = record.get("status_history", [])

    # Handle NaN, None, or missing
    if history is None or isinstance(history, float):
        return

    if not history:
        return


    transitions = registry.get("status_transitions", {})
    prev_time = None

    for entry in history:
        from_status = entry["from"]
        to_status = entry["to"]
        ts = entry["timestamp"]

        # Check legal transitions
        allowed = transitions.get(from_status, [])
        if to_status not in allowed:
            error(f"Illegal transition: {from_status} → {to_status}")

        # Check timestamp monotonicity
        # Accept timestamps with or without timezone
        ts_clean = ts.replace("Z", "+00:00")
        if "+" in ts_clean[10:] or "-" in ts_clean[10:]:
        # Timestamp includes timezone
            t = datetime.datetime.strptime(ts_clean, "%Y-%m-%dT%H:%M:%S%z")
        else:
            # Timestamp has no timezone
            t = datetime.datetime.strptime(ts_clean, "%Y-%m-%dT%H:%M:%S")
        if prev_time and t <= prev_time:
            error("Timestamps in status_history must be strictly increasing")
        prev_time = t

    # Final status must match last transition
    final_to = history[-1]["to"]
    if record.get("status") != final_to:
        error(
            f"Final status '{record.get('status')}' does not match last transition '{final_to}'"
        )


def validate_status_values(df, allowed, label):
    for _, row in df.iterrows():
        if row["status"] not in allowed:
            error(f"{label} invalid status '{row['status']}'")


def validate_foreign_keys(df, fk_map, lookup_tables, label):
    for fk_field, target in fk_map.items():
        target_table, target_field = target.split(".")
        valid_values = lookup_tables[target_table][target_field]

        for _, row in df.iterrows():
            if row[fk_field] not in valid_values:
                error(f"{label} invalid FK: {fk_field}='{row[fk_field]}' not found in {target}")


# ------------------------------------------------------------
# Schema-driven validation
# ------------------------------------------------------------
def validate_dataset(df, schema, lookup_tables, label, registry, strict=False):
    # Required fields
    validate_required_fields(df, schema["required_fields"], label)

    # Identifier pattern
    validate_id_pattern(df, schema["id_pattern"], schema["required_fields"][0], label)

    # Status values
    validate_status_values(df, schema["status_values"], label)

    # Foreign keys
    if "foreign_keys" in schema:
        validate_foreign_keys(df, schema["foreign_keys"], lookup_tables, label)

    # NEW: validate workflow transitions per record
    for _, row in df.iterrows():
        validate_status_history(row, schema, registry)

    # Strict mode: require schema_version field
    if strict and "schema_version" not in df.columns:
        error(f"Strict mode: {label} missing schema_version field")


# ------------------------------------------------------------
# Main pipeline
# ------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    # Load registry
    registry = load_registry()
    schemas = registry["schemas"]

    # Load canonical JSONL
    df_sprints = load_jsonl(DATA_DIR / "sprints.jsonl")
    df_issues = load_jsonl(DATA_DIR / "issues.jsonl")
    df_tasks = load_jsonl(DATA_DIR / "tasks.jsonl")

    # Lookup tables for FK validation
    lookup = {
        "sprints": {"sprint_id": set(df_sprints["sprint_id"])},
        "issues": {"issue_id": set(df_issues["issue_id"])},
        "tasks": {"task_id": set(df_tasks["task_id"])}
    }

    # Validate each dataset using registry rules
    validate_dataset(df_sprints, schemas["sprints"], lookup, "Sprints", registry, strict=args.strict)
    validate_dataset(df_issues, schemas["issues"], lookup, "Issues", registry, strict=args.strict)
    validate_dataset(df_tasks, schemas["tasks"], lookup, "Tasks", registry, strict=args.strict)

    if args.validate_only:
        print("Validation passed. No Parquet written.")
        return

    # Write Parquet only if validation passes
    df_sprints.to_parquet(DATA_DIR / "sprints.parquet", index=False)
    df_issues.to_parquet(DATA_DIR / "issues.parquet", index=False)
    df_tasks.to_parquet(DATA_DIR / "tasks.parquet", index=False)

    print("Validation passed. Parquet regenerated from canonical JSONL sources.")


if __name__ == "__main__":
    main()
