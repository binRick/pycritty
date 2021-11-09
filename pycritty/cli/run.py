import argparse
from .pycritty import subparsers, formatter

run = subparsers.add_parser(
    'run',
    help='Run Config',
    formatter_class=formatter(),
    argument_default=argparse.SUPPRESS,
)

