from connector.github_connector import GithubConnector

import os, logging, sys


class ActionsService:
    def __init__(self, org_name):
        self.org_name = org_name
        self.github_connector = GithubConnector()

    def deploy_to_repository(self, repo_name, init) -> None:
        '''
        Deploy workflows to single repository
        '''

        github_repo = self.github_connector.get_repo(repo_name)
        group = self._get_group(github_repo)

        if init:
            workflows = self._get_workflows('common')
        else:
            repo_name_formatted = self._format_repo_name(self.org_name, repo_name)
            workflows = self._get_workflows(group, repo_name_formatted)

        self.github_connector.deploy(github_repo, workflows, init)

    def deploy_to_group(self, group, init) -> None:
        '''
        Deploy workflows to group(multiple repositories)
        '''

        all_github_repositories = self.github_connector.get_all_repositories()
        matched_repo_names = self._filter_match_repository_topics_to_group(group, all_github_repositories)

        for repo_name in matched_repo_names:
            self.deploy_to_repository(repo_name, init)

    def _get_workflows(self, group, repo_name="None") -> list:
        '''
        Provide Workflow List (path & file contents).
        repo_name default value is "None" for init flag,
        which indicates sync-only option delivering sync_ci file only
        '''

        try:
            workflow_path = self._get_workflow_path(group, repo_name)
            workflow_file_names = os.listdir(workflow_path)
        except FileNotFoundError as e:
            logging.error(e)
            sys.exit(1)
        except Exception as e:
            raise e

        workflows = []
        for workflow_file_name in workflow_file_names:
            workflow = self._read_workflow(workflow_path, workflow_file_name)
            workflows.append(workflow)

        return workflows

    @staticmethod
    def _format_repo_name(org_name: str, repo_name_full: str) -> str:
        '''
        Format repo name by deleting '{github organization name}/'
        '''
        return repo_name_full[len(org_name) + 1:]

    @staticmethod
    def _get_workflow_path(group, repo_name: str) -> str:
        '''
        Provide workflow path in group-level or repo-level
        '''
        workflow_group_level_path = f'./{group}/workflows'                      # has common workflows
        workflow_repo_level_path = workflow_group_level_path + f'/{repo_name}'  # has not common workflows, has specified workflows.

        try:
            if os.path.isdir(workflow_repo_level_path):
                return workflow_repo_level_path
            else:
                return workflow_group_level_path
        except Exception as e:
            raise e

    @staticmethod
    def _read_workflow(workflow_path, workflow_name) -> dict:
        '''
        read workflow file contents by path
        '''
        path = f'.github/workflows/{workflow_name}'
        with open(f'{workflow_path}/{workflow_name}', 'r') as f:
            body = f.read()


        return {
            path: body
        }

    @staticmethod
    def _filter_match_repository_topics_to_group(group, all_github_repositories) -> list:
        '''
        Filter repositories which topics and groups match.
        '''

        result = []
        for repository in all_github_repositories:
            if group in repository['topics']:
                result.append(repository['full_name'])

        if not result:
            logging.error("No matching repositories.")
            sys.exit(1)

        return result

    @staticmethod
    def _get_group(github_repo) -> str:
        '''
        Return group name which repository topic matches the directory.
        '''

        topics = github_repo.get_topics()
        groups = []

        # group list from current working dir(actions)
        group_dir_list = os.listdir('./')

        for group_dir in group_dir_list:
            if os.path.isdir(group_dir):
                groups.append(group_dir)

        for topic in topics:
            if topic in groups:
                return topic

        logging.error('There are no matching topics in the workflow group!')
        sys.exit(1)
