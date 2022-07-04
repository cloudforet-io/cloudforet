from github import Github
from github.GithubException import UnknownObjectException,GithubException

import requests, json, math, sys, os, logging
logging.basicConfig(level=logging.INFO)

class GithubConnector():

  def __init__(self, org_name: str):
    self.client = self._get_client()
    self.org_name = org_name

  def get_repo(self, repo_name) -> object:
      try:
          return self.client.get_repo(repo_name)
      except UnknownObjectException as e:
          logging.error(f'Failed to github client creation, Resource not found : {e}')
          sys.exit(1)
      except Exception as e:
          raise e

  def get_all_repositories(self) -> list:
      '''
      get all repositories from github using github api
      '''

      url = f'https://api.github.com/search/repositories?q=org:{self.org_name}'
      org_info = self._http_requests(url)
      total_page = math.ceil(org_info['total_count']/100)

      repositories = []
      for page in range(1, total_page+1):
          url = f'https://api.github.com/orgs/{self.org_name}/repos?simple=yes&per_page=100&page={page}'
          repositories += self._http_requests(url)

      return repositories

  def get_topic(self):
      return

  def _get_client(self) -> object:
      token = os.getenv('PAT_TOKEN', None)

      if not token:
          logging.error('PAT_TOKEN does not set')
          sys.exit(1)

      try:
          return Github(token)
      except Exception as e:
          raise e

  def _create_new_workflows_in_repository(self, repo, workflows) -> None:
      for workflow in workflows:
          self._create(repo,workflow)

  def _update_workflows_in_repository(self, repo, workflows) -> None:
      for workflow in workflows:
          self._update(repo,workflow)

  def _delete_all_workflows(self, repo) -> None:
      contents = repo.get_contents(".github/workflows", ref="master")
      for content in contents:
          self._delete(repo, content)

  def delete(self, repo, content) -> None:
      try:
          message = f'CI: remove workflows ({content.path})'
          repo.delete_file(path=content.path, message=message, sha=content.sha, branch="master")
          logging.info(f'{content.path} has been deleted.')
      except UnknownObjectException as e:
          logging.warning(e)

  def _create(self, repo, workflow) -> None:
      try:
          for path,content in workflow.items():
              ret = repo.create_file(path=path, message="[CI] Deploy CI", content=content, branch="master")
              logging.info(f'file has been created to {repo.full_name} : {ret}')
      except GithubException as e:
          logging.error(f'failed to file creation : {e}')
      except Exception as e:
          raise e

  def _update(self, repo, workflow) -> None:
      try:
          for path,content in workflow.items():
              contents = repo.get_contents(path,ref="master")
              ret = repo.update_file(path=contents.path,message="[CI] Update CI",content=content,sha=contents.sha,branch="master")
              logging.info(f'file has been updated in {repo.full_name} : {ret}')
      except UnknownObjectException as e:
          logging.warning(f'failed to update to {repo.full_name}: {e}')
          self._create(repo, workflow)
      except Exception as e:
          raise e

  def deploy(self, repo, workflows, init) -> None:
      if init:
          self._delete_all_workflows(repo)
          self._create_new_workflows_in_repository(repo, workflows)
      else:
          self._update_workflows_in_repository(repo, workflows)


  def _http_requests(self, url) -> list:
      headers = {
          "Accept" : "application/vnd.github.v3+json"
      }

      try:
          response = requests.get(url, headers=headers).json()
      except requests.exceptions.ConnectionError as e:
          raise Exception(f'Connection Error {e.response}')
      except requests.exceptions.HTTPError as e:
          raise Exception(f'HTTP Error {e.response}')
      except json.JSONDecodeError as e:
          raise Exception(f'Json Decode Error {e}')

      return response