from module import argparse as ap
from connector.github_connector import GithubConnector

import logging, os, sys
logging.basicConfig(level=logging.INFO)
ARGS = ap.parse_args()

def main():
    github = GithubConnector()
    init = ARGS.init

    if ARGS.repo:
        repo_name = ARGS.repo
        deploy_to_repository(github, repo_name, init)
    elif ARGS.group:
        group = ARGS.group
        deploy_to_group(github, group, init)
    else:
        sys.exit(1)

def deploy_to_repository(github, repo_name, init) -> None:
    '''
    Deploy workflows to single repository
    '''

    repo = github._get_repo(repo_name)

    if init:
        workflows = _get_workflows('common')
    else:
        group = _get_group(repo)
        workflows = _get_workflows(group)

    github._deploy(repo, workflows, init)

def deploy_to_group(github, group, init) -> None:
    '''
    Deploy workflows to group(multiple repositories)
    '''

    all_repositories = github._get_all_repositories()
    repo_names = _filter_match_repository_topics_to_group(group, all_repositories)

    for repo_name in  repo_names:
        repo = github._get_repo(repo_name)

        if init:
            workflows = _get_workflows('common')
        else:
            workflows = _get_workflows(group)

        github._deploy(repo, workflows, init)

def _get_workflows(group) -> list:
    try:
        workflow_path = f'./{group}/workflows'
        workflow_list = os.listdir(workflow_path)
    except FileNotFoundError as e:
        logging.error(e)
        sys.exit(1)
    except Exception as e:
        raise e

    workflows = []
    ignore_files = ['.gitkeep']
    for workflow_name in workflow_list:
        if workflow_name in ignore_files:
            continue
        workflow = _read_workflow(workflow_path, workflow_name)
        workflows.append(workflow)

    return workflows

def _read_workflow(workflow_path, workflow_name) -> dict:
    with open(f'{workflow_path}/{workflow_name}','r') as f:
        body = f.read()

    path = f'.github/workflows/{workflow_name}'

    workflow_meta = {}    
    workflow_meta[path] = body

    return workflow_meta

def _filter_match_repository_topics_to_group(group, repositories) -> list:
    '''
    Filter repositories which topics and groups match.
    '''

    result = []
    for repository in repositories:
        if group in repository['topics']:
            result.append(repository['full_name'])

    if not result:
        logging.error("No matching repositories.")
        sys.exit(1)

    return result

def _get_group(repo) -> str:
    '''
    Return group name which repository topic matches the directory.
    '''

    topics = repo.get_topics()
    groups = []

    # group list from current working dir
    group_list = os.listdir('./')
    for group in group_list:
        if os.path.isdir(group):
            groups.append(group)

    for topic in topics:
        if topic in groups:
            return topic

    logging.error('There are no matching topics in the workflow group!')
    sys.exit(1)

if __name__ == "__main__":
    main()
