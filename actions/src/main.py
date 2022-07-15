from module import argparse as ap
from service.actions_service import ActionsService

ARGS = ap.parse_args()
ORG_NAME = "cloudforet-io"


def main():
    actions = ActionsService(ORG_NAME)
    init = ARGS.init

    if ARGS.repo:
        repo_name = ARGS.repo
        actions.deploy_to_repository(repo_name, init)
    elif ARGS.group:
        group = ARGS.group
        actions.deploy_to_group(group, init)
    else:
        raise Exception


if __name__ == "__main__":
    main()
