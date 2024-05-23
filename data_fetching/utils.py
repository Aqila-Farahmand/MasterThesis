import re
from data_fetching.request import make_request_with_retry, get_workflow_runs


owner = "apache"
repo = "trafficcontrol"


def sanitize_filename(filename: str) -> str:
    """
    Sanitizes the filename by removing or replacing characters that are invalid in file names.
    """
    # List of invalid characters that cannot be in filenames
    invalid_chars = "/\\?%*:|\"<>."
    for char in invalid_chars:
        filename = filename.replace(char, "_")

    # Remove any non-ASCII characters, spaces are replaced with underscores
    filename = re.sub(r'[^\x00-\x7F]+', '_', filename)
    filename = filename.replace(" ", "_")

    # Additional logic to ensure filename length is within OS limits
    filename = filename[:255]

    return filename


def fetch_workflows() -> list:
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows"
    response = make_request_with_retry(url)
    if response and response.status_code == 200:
        workflows = response.json().get("workflows", [])
        return workflows
    else:
        print(f"Failed to fetch workflows. Status code: {response.status_code if response else 'Unknown'}")
        return []


def fetch_workflow_runs(workflow_id: list[str]) -> list:
    url = f"https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs"
    runs = get_workflow_runs(url)
    for run in runs:
        run["status"] = run.get("status")
        run["conclusion"] = run.get("conclusion")
    return runs


def fetch_commit_details(commit_sha) -> tuple[str, str, str, list[str], int, int]:

    files_changed = []
    lines_added = 0
    lines_deleted = 0

    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}"
    response = make_request_with_retry(url)
    if response and response.status_code == 200:
        commit_data = response.json()
        commit_message = commit_data.get("commit", {}).get("message", "No commit message")
        commit_author = commit_data.get("commit", {}).get("author", {}).get("name", "Unknown")
        commit_date = commit_data.get("commit", {}).get("author", {}).get("date", "Unknown")

        for file in commit_data.get("files", []):
            files_changed.append(file["filename"])
            lines_added += file["additions"]
            lines_deleted += file["deletions"]

        return commit_message, commit_author, commit_date, files_changed, lines_added, lines_deleted
    else:
        print(
            f"Failed to fetch details for commit {commit_sha}. Status code: {response.status_code if response else "Unknown"}")
        return None, "Unknown", "Unknown", [], 0, 0


def fetch_pull_request_details(commit_sha: str) -> tuple[str, str, str, str, str, str, list[str]]:
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}/pulls"
    response = make_request_with_retry(url)
    if response and response.status_code == 200:
        pulls = response.json()
        if pulls:
            pull_request = pulls[0]
            pull_request_id = pull_request["number"]
            pull_request_title = pull_request["title"]
            pull_request_author = pull_request["user"]["login"]
            pull_request_created_at = pull_request["created_at"]
            pull_request_conversation_url = pull_request["comments_url"]
            pull_request_labels = [label["name"] for label in pull_request["labels"]]
            # Additional API request to get pull request details including body and labels
            pull_request_details_url = pull_request["url"]
            response = make_request_with_retry(pull_request_details_url)
            if response and response.status_code == 200:
                pull_request_details = response.json()
                pull_request_body = pull_request_details["body"]
            else:
                print(
                    f"Failed to fetch pull request details for commit {commit_sha}. Status code: {response.status_code if response else 'Unknown'}")
                return 7 * [None]
            return pull_request_id, pull_request_title, pull_request_author, pull_request_created_at, pull_request_body, pull_request_conversation_url, pull_request_labels
        else:
            return 7 * [None]
    else:
        print(
            f"Failed to fetch pull request details for commit {commit_sha}. Status code: {response.status_code if response else 'Unknown'}")
        return 7 * [None]


def fetch_pull_request_conversation(conversation_url):
    response = make_request_with_retry(conversation_url)
    conversation_data = []
    if response and response.status_code == 200:
        conversation = response.json()
        for comment in conversation:
            # Check if the comment is made by a user (not a bot)
            if comment.get("user", {}).get("type") == "User":
                comment_data = {
                    "comment_body": comment.get("body", "")
                }
                conversation_data.append(comment_data)
        return conversation_data
    else:
        print(
            f"Failed to fetch pull request conversation from URL: {conversation_url}. Status code: {response.status_code if response else 'Unknown'}")
        return []
