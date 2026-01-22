import os
import subprocess
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# Ensure data directory exists
# ---------------------------------------------------------
os.makedirs("data", exist_ok=True)

# ---------------------------------------------------------
# Extract commit-level metadata
# ---------------------------------------------------------
def extract_commit_metadata(repo_path="."):
    git_log_cmd = [
        "git",
        "-C",
        repo_path,
        "log",
        "--pretty=format:%H|%an|%ad|%s"
    ]

    result = subprocess.run(git_log_cmd, capture_output=True, text=True)
    lines = result.stdout.split("\n")

    records = []

    for line in lines:
        if "|" in line:
            commit_hash, author, date_str, message = line.split("|", 3)
            records.append({
                "commit_hash": commit_hash,
                "author": author,
                "timestamp": datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y %z"),
                "message": message
            })

    return pd.DataFrame(records)


# ---------------------------------------------------------
# Extract file-level changes
# ---------------------------------------------------------
def extract_file_changes(repo_path="."):
    git_log_cmd = [
        "git",
        "-C",
        repo_path,
        "log",
        "--pretty=format:%H",
        "--numstat"
    ]

    result = subprocess.run(git_log_cmd, capture_output=True, text=True)
    lines = result.stdout.split("\n")

    records = []
    current_commit = None

    for line in lines:
        if line.strip() == "":
            continue

        # Detect commit hash (40 hex chars)
        if len(line) == 40 and all(c in "0123456789abcdef" for c in line.lower()):
            current_commit = line.strip()
            continue

        # numstat line: added removed file
        parts = line.split("\t")
        if len(parts) == 3:
            added, removed, file_path = parts
            records.append({
                "commit_hash": current_commit,
                "file_path": file_path,
                "lines_added": int(added) if added.isdigit() else 0,
                "lines_removed": int(removed) if removed.isdigit() else 0
            })

    return pd.DataFrame(records)


# ---------------------------------------------------------
# Merge commit-level and file-level dataframes
# ---------------------------------------------------------
def build_forensic_dataset(repo_path="."):
    df_commits = extract_commit_metadata(repo_path)
    df_files = extract_file_changes(repo_path)

    df_merged = df_commits.merge(df_files, on="commit_hash", how="left")
    return df_merged


# ---------------------------------------------------------
# Derive sprint metrics
# ---------------------------------------------------------
def compute_sprint_metrics(df):
    metrics = {}

    # Velocity: number of commits
    metrics["commit_count"] = df["commit_hash"].nunique()

    # Velocity: number of files touched
    metrics["files_touched"] = df["file_path"].nunique()

    # Velocity: total lines added/removed
    metrics["total_lines_added"] = df["lines_added"].fillna(0).sum()
    metrics["total_lines_removed"] = df["lines_removed"].fillna(0).sum()

    # Cadence: average time between commits
    df_sorted = df.drop_duplicates("commit_hash").sort_values("timestamp")
    df_sorted["delta"] = df_sorted["timestamp"].diff()
    metrics["average_cadence"] = df_sorted["delta"].mean()

    # Flow efficiency: proportion of active time vs idle time
    deltas = df_sorted["delta"].dropna()
    if len(deltas) > 0:
        active_time = deltas.min()
        idle_time = deltas.sum() - active_time
        metrics["flow_efficiency"] = active_time / (active_time + idle_time)
    else:
        metrics["flow_efficiency"] = None

    return metrics


# ---------------------------------------------------------
# Run full extraction + save + metrics
# ---------------------------------------------------------
df = build_forensic_dataset(".")

# Save sovereign forensic dataset
df.to_csv("data/forensics.csv", index=False)
df.to_parquet("data/forensics.parquet")

# Compute sprint metrics
metrics = compute_sprint_metrics(df)

# Display results
print("\n=== FORENSIC DATASET ===")
print(df)

print("\n=== SPRINT METRICS ===")
for key, value in metrics.items():
    print(f"{key}: {value}")

# df and metrics now exist in memory for further analysis
