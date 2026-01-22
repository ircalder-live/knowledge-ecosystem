import os
import csv
import json
import requests
from datetime import datetime, timezone, timedelta

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

SCHEMA_VERSION = "2026-01-21.v4-graphql-org"

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

# New organization + repo
REPO = "Relational-Colab/knowledge-ecosystem"
GITHUB_OWNER = "Relational-Colab"   # organization login
PROJECT_NUMBER = 1                  # ProjectV2 number in the org

STATUS_FIELD_NAME = "Status"        # field name in the project
IN_PROGRESS_VALUE = "In Progress"   # value meaning “in progress”

REST_HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

GRAPHQL_URL = "https://api.github.com/graphql"
GRAPHQL_HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Content-Type": "application/json"
}

# ------------------------------------------------------------
# Utility Functions
# ------------------------------------------------------------

def parse_timestamp(ts):
    if ts is None:
        return None
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))

def timedelta_hours(start, end):
    if start is None or end is None:
        return None
    return (end - start).total_seconds() / 3600.0

# ------------------------------------------------------------
# Metric Computation
# ------------------------------------------------------------

def compute_lead_time(created_at, closed_at):
    return timedelta_hours(created_at, closed_at)

def compute_cycle_time(in_progress_at, closed_at):
    return timedelta_hours(in_progress_at, closed_at)

def compute_slack_time(created_at, in_progress_at):
    return timedelta_hours(created_at, in_progress_at)

def compute_dependency_latency(dep_closed_at, in_progress_at):
    return timedelta_hours(dep_closed_at, in_progress_at)

def compute_throughput(issues, window_days=7):
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=window_days)
    return sum(
        1 for issue in issues
        if issue["closed_at"] and parse_timestamp(issue["closed_at"]) >= cutoff
    )

# ------------------------------------------------------------
# REST API Calls
# ------------------------------------------------------------

def fetch_issues():
    url = f"https://api.github.com/repos/{REPO}/issues?state=all&per_page=100"
    response = requests.get(url, headers=REST_HEADERS)
    response.raise_for_status()
    return response.json()

def fetch_issue(issue_number):
    url = f"https://api.github.com/repos/{REPO}/issues/{issue_number}"
    response = requests.get(url, headers=REST_HEADERS)
    response.raise_for_status()
    return response.json()

# ------------------------------------------------------------
# GraphQL Helpers
# ------------------------------------------------------------

def graphql(query, variables):
    payload = {"query": query, "variables": variables}
    response = requests.post(GRAPHQL_URL, headers=GRAPHQL_HEADERS, json=payload)
    response.raise_for_status()
    data = response.json()
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {data['errors']}")
    return data["data"]

def list_user_projects():
    query = """
    query($owner: String!) {
      user(login: $owner) {
        projectsV2(first: 20) {
          nodes {
            id
            title
            number
          }
        }
      }
    }
    """
    data = graphql(query, {"owner": "ircalder-live"})
    user = data.get("user")
    if not user:
        print("User not found")
        return

    print("Projects for user ircalder-live")
    for p in user["projectsV2"]["nodes"]:
        if not p or not p.get("id"):
            continue
        print(f"- {p['number']}: {p['title']} (id={p['id']})")


def list_repo_projects():
    query = """
    query($owner: String!, $repo: String!) {
      repository(owner: $owner, name: $repo) {
        projectsV2(first: 20) {
          nodes {
            id
            title
            number
          }
        }
      }
    }
    """
    owner, repo_name = REPO.split("/")
    data = graphql(query, {"owner": owner, "repo": repo_name})
    repo = data.get("repository")
    if not repo:
        print("Repository not found")
        return

    print("Projects for repository", REPO)
    for p in repo["projectsV2"]["nodes"]:
        if not p or not p.get("id"):
            continue
        print(f"- {p['number']}: {p['title']} (id={p['id']})")

def list_org_projects():
    query = """
    query($owner: String!) {
      organization(login: $owner) {
        projectsV2(first: 20) {
          nodes {
            id
            title
            number
          }
        }
      }
    }
    """
    data = graphql(query, {"owner": GITHUB_OWNER})
    org = data.get("organization")
    if not org:
        print("No organization found for", GITHUB_OWNER)
        return

    print("Projects for organization", GITHUB_OWNER)
    for p in org["projectsV2"]["nodes"]:
        if not p or not p.get("id"):
            continue
        num = p.get("number")
        title = p.get("title")
        print(f"- {num}: {title} (id={p['id']})")


def get_project_id():
    # Organization-only lookup to avoid user resolution errors
    query = """
    query($owner: String!, $number: Int!) {
      organization(login: $owner) {
        projectV2(number: $number) {
          id
        }
      }
    }
    """
    data = graphql(query, {"owner": GITHUB_OWNER, "number": PROJECT_NUMBER})
    org = data.get("organization")
    if org and org.get("projectV2"):
        return org["projectV2"]["id"]
    raise RuntimeError("ProjectV2 not found for organization/number")

def get_issue_node_id(issue_number):
    query = """
    query($owner: String!, $repo: String!, $number: Int!) {
      repository(owner: $owner, name: $repo) {
        issue(number: $number) {
          id
        }
      }
    }
    """
    owner, repo_name = REPO.split("/")
    data = graphql(query, {"owner": owner, "repo": repo_name, "number": issue_number})
    issue = data["repository"]["issue"]
    if not issue:
        return None
    return issue["id"]

def get_in_progress_time_from_project(issue_node_id, project_id):
    query = """
    query($itemId: ID!) {
      node(id: $itemId) {
        ... on Issue {
          projectItems(first: 20) {
            nodes {
              project {
                id
              }
              fieldValues(first: 20) {
                nodes {
                  ... on ProjectV2ItemFieldSingleSelectValue {
                    field {
                      ... on ProjectV2SingleSelectField {
                        name
                      }
                    }
                    name
                    updatedAt
                  }
                }
              }
            }
          }
        }
      }
    }
    """
    data = graphql(query, {"itemId": issue_node_id})
    node = data.get("node")
    if not node:
        return None

    items = node["projectItems"]["nodes"]
    for item in items:
        if item["project"]["id"] != project_id:
            continue
        for fv in item["fieldValues"]["nodes"]:
            field = fv.get("field")
            if not field:
                continue
            if field.get("name") == STATUS_FIELD_NAME and fv.get("name") == IN_PROGRESS_VALUE:
                return parse_timestamp(fv["updatedAt"])
    return None

# ------------------------------------------------------------
# Dependency Parsing
# ------------------------------------------------------------

def extract_linked_issues(issue):
    body = issue.get("body") or ""
    linked = []
    tokens = body.replace("\n", " ").split(" ")
    for token in tokens:
        if token.startswith("#") and token[1:].isdigit():
            linked.append(int(token[1:]))
    return linked

def compute_dependency_metrics(issue_number, in_progress_at):
    if in_progress_at is None:
        return None, None

    issue = fetch_issue(issue_number)
    linked_numbers = extract_linked_issues(issue)
    if not linked_numbers:
        return None, None

    dep_closed_times = []
    for dep_num in linked_numbers:
        try:
            dep_issue = fetch_issue(dep_num)
            dep_closed_at = parse_timestamp(dep_issue.get("closed_at"))
            if dep_closed_at:
                dep_closed_times.append(dep_closed_at)
        except Exception:
            continue

    if not dep_closed_times:
        return None, None

    latest_dep_closed = max(dep_closed_times)
    latency_hours = compute_dependency_latency(latest_dep_closed, in_progress_at)
    return latest_dep_closed, latency_hours

# ------------------------------------------------------------
# Main Extraction Logic
# ------------------------------------------------------------

def extract_metrics():
    project_id = get_project_id()
    raw_issues = fetch_issues()
    issue_rows = []

    for issue in raw_issues:
        # Skip pull requests
        if "pull_request" in issue:
            continue

        number = issue["number"]
        title = issue["title"]
        created_at = parse_timestamp(issue["created_at"])
        closed_at = parse_timestamp(issue.get("closed_at"))

        issue_node_id = get_issue_node_id(number)
        in_progress_at = None
        if issue_node_id:
            in_progress_at = get_in_progress_time_from_project(issue_node_id, project_id)

        lead_time = compute_lead_time(created_at, closed_at)
        cycle_time = compute_cycle_time(in_progress_at, closed_at)
        slack_time = compute_slack_time(created_at, in_progress_at)

        dep_closed_at, dep_latency = compute_dependency_metrics(number, in_progress_at)

        issue_rows.append({
            "issue_number": number,
            "title": title,
            "created_at": issue["created_at"],
            "closed_at": issue.get("closed_at"),
            "in_progress_at": in_progress_at.isoformat() if in_progress_at else None,
            "dependency_latest_closed_at": dep_closed_at.isoformat() if dep_closed_at else None,
            "lead_time_hours": lead_time,
            "cycle_time_hours": cycle_time,
            "slack_time_hours": slack_time,
            "dependency_latency_hours": dep_latency
        })

    throughput_7d = compute_throughput(issue_rows, window_days=7)

    metadata = {
        "schema_version": SCHEMA_VERSION,
        "repo": REPO,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "throughput_last_7_days": throughput_7d,
        "issue_count": len(issue_rows)
    }

    return {
        "metadata": metadata,
        "issues": issue_rows
    }

# ------------------------------------------------------------
# Output Writers
# ------------------------------------------------------------

def write_csv(payload, filename="governance-metrics.csv"):
    issues = payload["issues"]
    if not issues:
        return
    fieldnames = issues[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(issues)

def write_json(payload, filename="governance-metrics.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

# ------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------

def main(): list_user_projects()

if __name__ == "__main__":
    main()
