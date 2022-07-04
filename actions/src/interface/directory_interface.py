import logging, os, sys

class DirectoryInterface():
    def get_workflow_path(self, group, repo_name: str) -> str:
        '''
        Provide workflow path in group-level or repo-level
        '''
        workflow_group_level_path = f'./actions/{group}/workflows'
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

    def get_workflows(self, group, repo_name ="None") -> list:
        '''
        Provide Workflow List (path & file contents).
        repo_name default value is "None" for init flag,
        which indicates sync-only option delivering sync_ci file only
        '''

        try:
            workflow_path = self.get_workflow_path(group, repo_name)
            workflow_list = os.listdir(workflow_path)
        except FileNotFoundError as e:
            logging.error(e)
            sys.exit(1)
        except Exception as e:
            raise e

        workflows = []
        for workflow_name in workflow_list:
            if os.path.isdir(f'{workflow_path}/{workflow_name}'):
                continue
            workflow = self._read_workflow(workflow_path, workflow_name)
            workflows.append(workflow)

        return workflows

    def _read_workflow(self, workflow_path, workflow_name) -> dict:
        '''
        read workflow file contents by path
        '''
        with open(f'{workflow_path}/{workflow_name}','r') as f:
            body = f.read()

        path = f'.github/workflows/{workflow_name}'

        workflow_meta = {}
        workflow_meta[path] = body

        return workflow_meta

    def get_group_list(self, path):
        group_list = os.listdir(path)

        groups = []
        for group in group_list:
            if os.path.isdir(f'actions/{group}'):
                groups.append(group)

        return groups