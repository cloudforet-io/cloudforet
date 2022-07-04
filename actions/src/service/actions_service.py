from connector.github_connector import GithubConnector
from interface.directory_interface import DirectoryInterface
import logging
import sys


class ActionsService:
    def __init__(self, org_name):
        self.github_connector = GithubConnector(org_name)
        self.directory_interface = DirectoryInterface()

    def deploy_to_repository(self, repo_name, init) -> None:
        '''
        Deploy workflows to single repository
        '''

        repo = self.github_connector.get_repo(repo_name)
        group = self._get_group(repo)

        if init:
            workflows = self.directory_interface.get_workflow_path('common')
        else:
            repo_name_formatted = self._format_repo_name(repo_name)
            workflows = self.directory_interface.get_workflows(group, repo_name_formatted)

        self.github_connector.deploy(repo, workflows, init)
        self.clean_up_old_workflow(repo, workflows)

    def deploy_to_group(self, group, init) -> None:
        '''
        Deploy workflows to group(multiple repositories)
        '''

        all_repositories = self.github_connector.get_all_repositories()
        repo_names = self._filter_match_repository_topics_to_group(group, all_repositories)

        for repo_name in repo_names:
            self.deploy_to_repository(repo_name, init)

    def clean_up_old_workflow(self, repo, workflows) -> None:
        '''
        Clean up old workflows that are not in the actual directory
        '''

        managed_workflows = []
        for workflow in workflows:
            for path, _ in workflow.items():
                managed_workflows.append(path)

        all_contents = repo.get_contents('.github/workflows')
        for content in all_contents:
            if "actions" in content.path and content.path not in managed_workflows:
                self.github_connector.delete(repo, content)


    def _get_group(self, repo) -> str:
        '''
        Return group name which repository topic matches the directory.
        '''

        topics = repo.get_topics()
        groups = self.directory_interface.get_group_list('./actions/')

        # group list from current working dir
        for topic in topics:
            if topic in groups:
                return topic

        logging.error('There are no matching topics in the workflow group!')
        sys.exit(1)

    @staticmethod
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

    @staticmethod
    def _format_repo_name(repo_name_full: str) -> str:
        '''
        Format repo name by deleting '{github organization name}/'
        '''
        return repo_name_full.split("/")[1]