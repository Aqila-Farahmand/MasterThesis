import os
import sys
from typing import Any

import pandas as pd
from hashlib import md5
from cache import save_data_to_csv
from cache import PATH as CACHE_PATH

from utils import (
    fetch_workflows,
    fetch_workflow_runs,
    fetch_commit_details,
    fetch_pull_request_details,
    fetch_pull_request_comments,
    fetch_issue_details,
    sanitize_filename,
    flatten
)


if __name__ == "__main__":
    workflows = fetch_workflows()
    for workflow_index, workflow in enumerate(workflows):
        print("Starting workflow {} of {}".format(workflow_index + 1, len(workflows)))
        workflow_id = workflow["id"]
        workflow_name = workflow["name"]
        # get all the runs for this particular workflow_id
        workflow_runs_list = []
        run_details = []
        print(f"Fetching runs for workflow: {workflow_name}")
        runs = fetch_workflow_runs(workflow_id)
        for run_index, run in enumerate(runs):
            print("Starting run {} of {}".format(run_index + 1, len(runs)))
            event = run["event"]
            run_id = run["id"]
            commit_sha = run["head_sha"]

            run_filename = md5((str(workflow_id) + str(run_id)).encode()).hexdigest() + '.csv'
            file_path = CACHE_PATH / run_filename
            if file_path.exists():
                print(f"Skipping {run_filename} as it has already been processed.")
                continue

            commit_message, commit_author, commit_date, files_changed, lines_added, lines_deleted = (fetch_commit_details(commit_sha))
            pr_number, pr_url, pr_state, pr_title, pr_author, pr_created_at, pr_labels, pr_body, pr_comments_url = fetch_pull_request_details(commit_sha)
            pull_request_comments = fetch_pull_request_comments(pr_comments_url) if pr_comments_url else []

            # Fetch the issue details
            #issues_url = run.get("issues_url", [])
            #issue_url, issue_number, issue_title, issue_author, issue_date, issue_body, issue_labels = (fetch_issue_details(issues_url))
            # "pulls_url": "https://api.github.com/repos/octo-org/octo-repo/pulls{/number}" a list of dict

            run_events_details = {
                "workflow_name": workflow_name,
                "run_id": run["id"],
                "run_number": run["run_number"],
                "run_status": run["status"],
                "run_conclusion": run["conclusion"],
                "event": run["event"],
                "url": run["url"],
                "commit_id": commit_sha,
                "commit_message": commit_message,
                "commit_author": commit_author,
                "commit_date": commit_date,
                "lines_added": lines_added,
                "lines_deleted": lines_deleted,
                "files_changed": files_changed,
                "pull_request_number": pr_number,
                "pull_request_url": pr_url,
                "pull_request_state": pr_state,
                "pr_comments_url": pr_comments_url,
                "pull_request_title": pr_title,
                "pull_request_author": pr_author,
                "pull_request_created_at": pr_created_at,
                "Pull_request_label": pr_labels,
                "pull_request_body": pr_body,
                "pull_request_comments": pull_request_comments
            }
            run_details.append(run_events_details)
            print("Fetching completed")
            # Save single run
            save_data_to_csv(run_details, run_filename)
        # Save all runs for a single workflow
        workflow_runs_list.append(run_details)
        flattened_data = flatten(workflow_runs_list)
        workflow_name = sanitize_filename(f'{workflow_name}')
        workflow_file_name = workflow_name + '.csv'
        save_data_to_csv(flattened_data, workflow_file_name)
