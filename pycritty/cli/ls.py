import argparse
from .pycritty import subparsers, formatter

from rich import print
import psutil



list_parser = subparsers.add_parser(
    'ls',
    help='List available resources',
    formatter_class=formatter(),
    argument_default=argparse.SUPPRESS,
)

list_parser.add_argument(
    '-t', '--themes',
    action='store_true',
    help='List themes',
)

list_parser.add_argument(
    '-f', '--fonts',
    action='store_true',
    help='List fonts',
)

list_parser.add_argument(
    '-c', '--configs',
    action='store_true',
    help='List saved configs',
)

list_parser.add_argument(
    '-a', '--all',
    action='store_true',
    help='List all (default)',
)

list_parser.add_argument(
    '-H', '--hosts',
    action='store_true',
    help='List Hosts',
)
list_parser.add_argument(
    '-p', '--pids',
    action='store_true',
    help='Outlist of alacritty pids',
)

list_parser.add_argument(
    '-i', '--iterable',
    action='store_true',
    help='Output list in iterable format (for scripts)',
)
