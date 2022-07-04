from module import argparse as ap
from service.actions_service import ActionsService

ARGS = ap.parse_args()


def main():
    init = ARGS.init
    actions = ActionsService("cloudforet-io")

    if ARGS.repo:
        repo_name = ARGS.repo
        actions.deploy_to_repository(repo_name, init)
    elif ARGS.group:
        group = ARGS.group
        actions.deploy_to_group(group, init)
    else:
        raise Exception(f'Unexpected action.')


if __name__ == "__main__":
    main()
