import argparse
import textwrap

def parse_args():
    parser = argparse.ArgumentParser(
        description='File push to github repository',
        epilog=textwrap.dedent('''\
            Examples:
                python src/%(prog)s --repo spaceone/inventory
                python src/%(prog)s --repo spaceone/config --init
                python src/%(prog)s --group plugin
                python src/%(prog)s --group plugin --init
        '''),
        formatter_class=argparse.RawDescriptionHelpFormatter)

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument('--repo', metavar='<owner/repo>',
                        help='Select specified repository.')

    group.add_argument('--group', metavar='<group_name>',
                        help='Select specified group.')

    parser.add_argument('--init', action='store_true', default=False,
                        help='Deploy sync workflow only.')

    return parser.parse_args()