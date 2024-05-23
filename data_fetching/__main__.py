from cache import save_data_to_csv, PATH
from utils import (
    fetch_workflows,
    fetch_workflow_runs,
    fetch_commit_details,
    fetch_pull_request_details,
    fetch_pull_request_conversation
)

if __name__ == "__main__":
    workflows = fetch_workflows()
    for workflow in workflows:
        workflow_id = workflow["id"]
        runs = fetch_workflow_runs(workflow_id)
        for run in runs:
            commit_sha = run["head_sha"]
            file_name = f"{commit_sha}.csv"
            file_path = PATH / file_name

            # If the file is already in the cache, skip processing
            if file_path.exists():
                print(f"Skipping {file_name} as it has already been processed.")
                continue

            commit_message, commit_author, commit_date, files_changed, lines_added, lines_deleted = fetch_commit_details(commit_sha)
            pr_id, pr_title, pr_author, pr_date, pr_body, pr_url, pr_labels = fetch_pull_request_details(commit_sha)
            pull_request_conversation = fetch_pull_request_conversation(pr_url) if pr_url else []
            workflow_data = {
                "workflow_name": workflow["name"],
                "run_id": run["id"],
                "run_status": run["status"],
                "run_conclusion": run["conclusion"],
                "commit_id": commit_sha,
                "commit_message": commit_message,
                "commit_author": commit_author,
                "commit_date": commit_date,
                "lines_added": lines_added,
                "lines_deleted": lines_deleted,
                "files_changed": files_changed,
                "pull_request_id": pr_id,
                "pull_request_title": pr_title,
                "pull_request_author": pr_author,
                "pull_request_created_at": pr_date,
                "Pull_request_label": pr_labels,
                "pull_request_body": pr_body,
                "pull_request_conversation": pull_request_conversation
            }
            # Save each workflow run data immediately after processing
            # save_data_to_file(workflow_data, 'workflow_data.json')
            save_data_to_csv(workflow_data, file_name)
