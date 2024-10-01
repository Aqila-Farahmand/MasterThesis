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


def flatten(data):
    if not isinstance(data, list):
        return [data]
    if all(isinstance(item, dict) for item in data):
        return data
    flat_list = []
    for item in data:
        flat_list.extend(flatten(item))
    return flat_list


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


def fetch_issue_details(issue_url: str) -> tuple[str, int, str, str, str, str, list[str]]:
    response = make_request_with_retry(issue_url)
    if response and response.status_code == 200:
        issue_data = response.json()
        issue_url = issue_data.get("url")
        issue_number = issue_data.get("number")
        issue_title = issue_data.get("title")
        issue_author = issue_data.get("author")
        issue_date = issue_data.get("date")
        issue_body = issue_data.get("body")
        issue_labels = issue_data.get("labels")

        return issue_url, issue_number, issue_title, issue_author, issue_date, issue_body, issue_labels
    else:
        print(
            f"Failed to fetch details for the following issue {issue_url}. Status Code: {response.status_code if response else "Unknown"}")
        return None, "Unknown", "Unknown", "Unknown", "Unknown", []


def fetch_pull_request_details(commit_sha: str) -> tuple[int, str, str, str, str, str, list['str'], str, str]:
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{commit_sha}/pulls"
    response = make_request_with_retry(url)
    if response and response.status_code == 200:
        pulls = response.json()
        if pulls:
            for pull in pulls:
                pr_number = pull["number"]
                pr_url = pull["url"]
                pr_state = pull["state"]
                pr_title = pull["title"]
                pr_author = pull["user"]["login"]
                pr_created_at = pull["created_at"]
                pr_labels = [label["name"] for label in pull["labels"]]  # list
                pr_body = pull.get("body", str)
                pr_comments_url = pull["comments_url"]
                return pr_number, pr_url, pr_state, pr_title, pr_author, pr_created_at, pr_labels, pr_body, pr_comments_url
            else:
                return 9 * [None]
        else:
            print(f"No pulls found for commit {commit_sha}")
            return 9 * [None]
    else:
        print(
            f"Failed to fetch pull request details for commit {commit_sha}. Status code: {response.status_code if response else 'Unknown'}")
        return 9 * [None]


def get_pull_number(pulls_url: str) -> int:
    for url in pulls_url:
        parts = url.split('/')
        # The pull request number is the last part of the URL
        pull_number = parts[-1]
        if pull_number.isdigit():
            return int(pull_number)
        else:
            raise ValueError(f"No pull request number is found in the URL: {url}")


def fetch_pull_request_comments(comments_url: str) -> list[dict]:
    response = make_request_with_retry(comments_url)
    if response and response.status_code == 200:
        pr_comments = []
        comments_data = response.json()  # returns a list of dictionary
        for comment in comments_data:  # for a dict in a list
            if comment.get("user", {}).get("type") == "User":
                comment_body = comment.get("body")
                pr_comments.append(comment_body)
        return pr_comments if pr_comments else None
