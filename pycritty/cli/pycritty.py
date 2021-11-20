import argparse
from .. import __version__


def formatter(indent_increment=2, max_help_position=40, width=None):
    return lambda prog: argparse.HelpFormatter(
        prog,
        indent_increment,
        max_help_position,
        width, 
    )


parser = argparse.ArgumentParser(
    prog='pycritty',
    description='Manage Alacritty Config',
    argument_default=argparse.SUPPRESS,
    formatter_class=formatter(),
)
parser.add_argument(
    '-v', '--version',
    action='version',
    version=__version__,
)

parser.add_argument(
    '-T', '--tmux',
    dest='enable_tmux_mode',
    metavar='TMUX_ENABLED',
    help='Enable Tmux mode',
)
parser.add_argument(
    '-t', '--theme',
    dest='change_theme',
    metavar='THEME',
    help='Change theme, choose from ~/.config/alacritty/themes',
)
parser.add_argument(
    '-H', '--host',
    dest='change_host',
    metavar='HOST',
    help='Change host',
)
parser.add_argument(
    '-S', '--shell',
    dest='change_shell',
    metavar='SHELL',
    help='Change shell',
)
parser.add_argument(
    '-L', '--local-ports',
    dest='change_local_ports',
    metavar='LOCAL_PORTS',
    help='Change local ports',
)
parser.add_argument(
    '-U', '--user',
    dest='change_user',
    metavar='ARGS',
    help='Change user',
)
parser.add_argument(
    '-A', '--args',
    dest='change_args',
    metavar='ARGS',
    help='Change args',
)
parser.add_argument(
    '-f', '--font',
    dest='change_font',
    metavar='FONT',
    help='Change font family, choose from ~/.config/alacritty/fonts.yaml',
)
parser.add_argument(
    '-s', '--size',
    type=float,
    dest='change_font_size',
    metavar='SIZE',
    help='Change font size',
)
parser.add_argument(
    '-o', '--opacity',
    type=float,
    dest='change_opacity',
    metavar='OPACITY',
    help='Change background opacity',
)
parser.add_argument(
    '-r', '--rows',
    type=int,
    nargs=1,
    dest='change_rows',
    help='Change rows',
)
parser.add_argument(
    '-c', '--columns',
    type=int,
    nargs=1,
    dest='change_columns',
    help='Change columns',
)
parser.add_argument(
    '-p', '--position',
    metavar=('X', 'Y'),
    type=int,
    nargs=2,
    dest='change_position',
    help='Change window position X Y values',
)
parser.add_argument(
    '-P', '--padding',
    metavar=('X', 'Y'),
    type=int,
    nargs=2,
    dest='change_padding',
    help='Change window padding X Y values',
)
parser.add_argument(
    '-O', '--offset',
    metavar=('X', 'Y'),
    type=int,
    nargs=2,
    dest='change_font_offset',
    help='Change offset, X is space between chars and Y is line height',
)

subparsers = parser.add_subparsers(title='subcommands', dest='subcommand',)
