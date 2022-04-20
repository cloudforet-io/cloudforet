from module import argparse as ap
from connector.github_connector import GithubConnector

import logging, os, sys
logging.basicConfig(level=logging.INFO)
ARGS = ap.parse_args()
ORG_NAME = "cloudforet-io"


def main():
    github = GithubConnector(ORG_NAME)
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
    group = _get_group(repo)

    if init:
        workflows = _get_workflows('common')
    else:
        repo_name_formatted = _format_repo_name(ORG_NAME, repo_name)
        workflows = _get_workflows(group, repo_name_formatted)

    github._deploy(repo, workflows, init)


def deploy_to_group(github, group, init) -> None:
    '''
    Deploy workflows to group(multiple repositories)
    '''

    all_repositories = github._get_all_repositories()
    repo_names = _filter_match_repository_topics_to_group(group, all_repositories)

    for repo_name in  repo_names:
        deploy_to_repository(github, repo_name, init)


def _format_repo_name(org_name: str, repo_name_full: str) -> str:
    '''
    Format repo name by deleting '{github organization name}/'
    '''
    return repo_name_full[len(org_name) + 1:]


def _get_workflow_path(group, repo_name: str) -> str:
    '''
    Provide workflow path in group-level or repo-level
    '''
    workflow_group_level_path = f'./{group}/workflows'
    workflow_repo_level_path = workflow_group_level_path + f'/{repo_name}'

    try:
        if os.path.isdir(workflow_repo_level_path):
            return workflow_repo_level_path
        else:
            return workflow_group_level_path
    except FileNotFoundError as e:
        logging.error(e)
        sys.exit(1)
    except Exception as e:
        raise e


def _get_workflows(group, repo_name ="None") -> list:
    '''
    Provide Workflow List (path & file contents).
    repo_name default value is "None" for init flag,
    which indicates sync-only option delivering sync_ci file only
    '''

    try:
        workflow_path = _get_workflow_path(group, repo_name)
        workflow_list = os.listdir(workflow_path)
    except FileNotFoundError as e:
        logging.error(e)
        sys.exit(1)
    except Exception as e:
        raise e

    workflows = []
    for workflow_name in workflow_list:

        workflow = _read_workflow(workflow_path, workflow_name)
        workflows.append(workflow)

    return workflows


def _read_workflow(workflow_path, workflow_name) -> dict:
    '''
    read workflow file contents by path
    '''
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
