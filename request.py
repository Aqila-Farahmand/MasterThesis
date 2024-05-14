import os
import time
import requests
from requests import Response


# export GITHUB_TOKEN=<your_github_token>
github_token = os.environ.get("GITHUB_TOKEN")

limit_remaining = "X-RateLimit-Remaining"
limit_reset = "X-RateLimit-Reset"


def get_header() -> dict[str: str]:
    return {"Authorization": f"token {github_token}"}


def make_request_with_retry(url: str, max_retries: int = 3, wait_seconds: int = 1) -> Response:
    """
    Make a request to the GitHub API with retry and backoff strategy.
    """
    for attempt in range(max_retries):
        headers = get_header()  # Get headers with the current GitHub token
        try:
            response = requests.get(url, headers=headers)
            code = response.status_code
            if code == 200:
                return response  # Success
            elif code == 403 and limit_remaining in response.headers and response.headers[limit_remaining] == "0":
                # Rate limit exceeded
                reset_time = int(response.headers[limit_reset])
                current_time = int(time.time())
                wait_for = max(reset_time - current_time, 1)  # Ensure at least a minimal wait time
                print(f"Rate limit exceeded. Waiting for {wait_for} seconds before retrying...")
                time.sleep(wait_for)
            else:
                # Other errors
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            if attempt < max_retries - 1:
                # Implement exponential backoff
                backoff_time = wait_seconds * 2 ** attempt
                print(f"Retrying in {backoff_time} seconds...")
                time.sleep(backoff_time)
            else:
                raise Exception("Max retries exceeded with GitHub API.")


def get_workflows():
    pass


def get_workflow_runs(url: str):
    all_runs = []
    next_page = url

    while next_page:
        response = make_request_with_retry(next_page)
        response.raise_for_status()
        data = response.json()
        all_runs.extend(data["workflow_runs"])

        next_page = None
        if "next" in response.links:
            next_page = response.links["next"]["url"]

    return all_runs


def get_commit():
    pass


def get_pull_request():
    pass
