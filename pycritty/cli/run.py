import argparse
from .pycritty import subparsers, formatter

run = subparsers.add_parser(
    'run',
    help='Run Config',
    formatter_class=formatter(),
    argument_default=argparse.SUPPRESS,
)



run.add_argument(
    '-c', '--config',
    dest='change_base_config',
    metavar='EXISTING_CONFIG_NAME',
    help='Saved Config Name to Base Config File from',
)
