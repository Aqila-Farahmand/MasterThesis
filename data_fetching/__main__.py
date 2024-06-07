import os
from typing import Any

import pandas as pd
from hashlib import md5
from cache import save_data_to_csv, PATH
from cache import PATH as CACHE_PATH

from utils import (
    fetch_workflows,
    fetch_workflow_runs,
    fetch_commit_details,
    fetch_pull_request_details,
    fetch_pull_request_comments,
    fetch_issue_details,
    get_pull_number
)

file_name = PATH / "workflow_runs.csv"

if __name__ == "__main__":
    workflows = fetch_workflows()
    for workflow_index, workflow in enumerate(workflows):
        print("Starting workflow {} of {}".format(workflow_index + 1, len(workflows)))
        workflow_runs_list = []
        workflow_id = workflow["id"]
        workflow_name = workflow["name"]
        # get all the runs for this particular workflow_id
        print("Fetching workflow runs")
        runs = fetch_workflow_runs(workflow_id)
        print("Fetching completed")
        for run_index, run in enumerate(runs):
            print("Starting run {} of {}".format(run_index + 1, len(runs)))
            run_details = []
            event = run["event"]
            run_id = run["id"]
            commit_sha = run["head_sha"]
            run_filename = md5((str(workflow_id) + str(run_id)).encode()).hexdigest() + '.csv'
            # if the file is already present in the cache add its content to the list and skip
            if os.path.exists(CACHE_PATH / run_filename):
                file_content = pd.read_csv(CACHE_PATH / run_filename)
                run_events_details = file_content.to_dict('records')
                workflow_runs_list.append(run_events_details)
                run_details.append(run_events_details)
                continue
            # fetch commit details
            commit_message, commit_author, commit_date, files_changed, lines_added, lines_deleted = (
                fetch_commit_details(commit_sha))

            # Apply the logic to get all the pull requests for this commits by getting the pulls url or commit sha? sol: using sha
            # How different is run["pulls_url"] vs pr that I get for each commit?
            # I think the pr I fetch for each commit_sha of a run basically fetches pr for that commit which has to do nothing with runs! :) Since Fetching PR using commit_sha of a run fetches PR for that particular commit which is not related to the workflow run.
            # however the pulls_url that I get in the run field has to do something with the run but does that mean the run is trigered by that pr? is it the same thing?
            #The solution is to check it with an exampke small repo workflow run that event == pull_request? so I get my answer! :)

            # Note: in the run field I can only access the pulls url in the form of pulls/number
            # this "run.get("pull_requests", [])" is a different field in a run data field
            #issues_url = run.get("issues_url", [])
            #issue_url, issue_number, issue_title, issue_author, issue_date, issue_body, issue_labels = (fetch_issue_details(issues_url))
            # "pulls_url": "https://api.github.com/repos/octo-org/octo-repo/pulls{/number}" a list of dict

            # pull_request_url = run["pulls_url"]  # there are more than one key for a single run dictionary also, a generic template does't contain an actual number
            # print("pull_request_url")

            # pull_number = get_pull_number(pull_request_url)

            # pr_title, pr_author, pr_created_at, base_repository, is_closed, merge_state_status, files_changed, no_of_files_changes, pr_labels, pr_body, pr_comments_url, pr_comments = fetch_pull_request_details(pr_number)

            pull_requests = run.get("pull_requests", [])
            if pull_requests:
                for pr in pull_requests:
                    pr_number = pr["number"]  # example url: 'url': 'https://api.github.com/repos/moqimoqidea/tomcat/pulls/254' 254 is pull number! also pulls_url pattern
                    pr_title, pr_author, pr_created_at, pr_labels, pr_body, pr_comments_url = fetch_pull_request_details(pr_number)
                    pull_request_comments = fetch_pull_request_comments(pr_comments_url) if pr_comments_url else []
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
                        "pr_comments_url": pr_comments_url,
                        "pull_request_title": pr_title,
                        "pull_request_author": pr_author,
                        "pull_request_created_at": pr_created_at,
                        "Pull_request_label": pr_labels,
                        "pull_request_body": pr_body,
                        "pull_request_comments": pull_request_comments
                    }
                    workflow_runs_list.append(run_events_details)
                    run_details.append(run_events_details)
            # Save single run
            save_data_to_csv(run_details, run_filename)
        # Save single workflow
        save_data_to_csv(workflow_runs_list, file_name)
