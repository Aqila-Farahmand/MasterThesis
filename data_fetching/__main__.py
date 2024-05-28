from cache import save_data_to_csv, PATH
from utils import (
    fetch_workflows,
    fetch_workflow_runs,
    fetch_commit_details,
    fetch_pull_request_details,
    fetch_pull_request_conversation,
    fetch_issue_details
)


def get_push_events(commit_id, wf_name, wf_run):
    commit_message, commit_author, commit_date, files_changed, lines_added, lines_deleted = fetch_commit_details(
        commit_id)

    commit_details = {
        "workflow_name": wf_name,
        "run_id": wf_run["id"],
        "run_status": wf_run["status"],
        "run_conclusion": wf_run["conclusion"],
        "event": wf_run["event"],
        "commit_id": commit_sha,
        "commit_message": commit_message,
        "commit_author": commit_author,
        "commit_date": commit_date,
        "lines_added": lines_added,
        "lines_deleted": lines_deleted,
        "files_changed": files_changed,
    }
    return commit_details


def get_pull_request_events(pull_request_id, wf_name, wf_run):
    pr_title, pr_author, pr_date, pr_body, pr_url, pr_labels = fetch_pull_request_details(pull_request_id)
    pull_request_conversation = fetch_pull_request_conversation(pr_url) if pr_url else []
    pull_request_details = {
        "workflow_name": wf_name,
        "run_id": wf_run["id"],
        "run_status": wf_run["status"],
        "run_conclusion": wf_run["conclusion"],
        "event": wf_run["event"],
        "pull_request_id": pull_request_id,
        "pull_request_title": pr_title,
        "pull_request_author": pr_author,
        "pull_request_created_at": pr_date,
        "Pull_request_label": pr_labels,
        "pull_request_body": pr_body,
        "pull_request_conversation": pull_request_conversation
    }
    return pull_request_details


def get_issue_events(issue_id, wf_name, wf_run):
    issue_id, issue_title, issue_author, issue_body, issue_url, issue_labels = fetch_issue_details(issue_id)
    issue_details = {
        "workflow_name": wf_name,
        "run_id": wf_run["id"],
        "run_status": wf_run["status"],
        "run_conclusion": wf_run["conclusion"],
        "event": wf_run["event"],
        "issue_id": issue_number,
        "issue_title": issue_title,
        "issue_author": issue_author,
        "issue_body": issue_body,
        "issue_url": issue_url,
        "issue_labels": issue_labels,
    }
    return issue_details


if __name__ == "__main__":
    workflows = fetch_workflows()
    for workflow in workflows:
        workflow_id = workflow["id"]
        workflow_name = workflow["name"]
        runs = fetch_workflow_runs(workflow_id)
        workflow_data_list = []

        for run in runs:
            event = run["event"]
            if event == "push":
                commit_sha = run["head_sha"]
                commit_data = get_push_events(commit_sha, workflow_name, run)
                workflow_data_list.append(commit_data)

            elif event == "pull_request":
                pull_requests = run.get("pull_requests", [])
                for pr_data in pull_requests:
                    pr_number = pr_data["number"]
                    pull_data_list = get_pull_request_events(pr_number, workflow_name, run)
                    workflow_data_list.append(pull_data_list)

            elif event == "issues":
                issue_number = run["payload"]["issue"]["number"]
                issue_data = get_issue_events(issue_number, workflow_name, run)
                workflow_data_list.append(issue_data)

            else:
                print(f"Unsupported event: {event}")
                continue
            # Generate a unique file name using event type and timestamp or UUID
            run_id = run["run_number"]
            file_name = f"{workflow_name}_{event}_{run_id}.csv"
            file_path = PATH / file_name

            # If the file already exists, skip processing
            if file_path.exists():
                print(f"Skipping {file_name} as it has already been processed.")
                continue
            save_data_to_csv(workflow_data_list, file_name)
            print(f"Data saved to {file_name}")
