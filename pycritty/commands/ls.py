from typing import List, Dict, Any
from .command import Command
from .. import PycrittyError
from ..resources import fonts_file, themes_dir, saves_dir, hosts_dir, shells_dir, commands_dir, positions_dir, profiles_dir
from ..resources.resource import Resource
from ..io import log
from ..io.yio import read_yaml
from pathlib import Path
import psutil

class ListResource(Command):
    def __init__(self):
        self.options = {
            'themes': ('Themes', log.Color.BLUE, self.list_themes),
            'fonts': ('Fonts', log.Color.PURPLE, self.list_fonts),
            'configs': ('Configs', log.Color.CYAN, self.list_configs),
            'pids': ('Pids', log.Color.YELLOW, self.list_pids),
            'hosts': ('Hosts', log.Color.GREEN, self.list_hosts),
            'shells': ('Shells', log.Color.RED, self.list_shells),
            'commands': ('Commands', log.Color.PURPLE, self.list_commands),
            'positions': ('Positions', log.Color.YELLOW, self.list_positions),
            'profiles': ('Profiles', log.Color.YELLOW, self.list_profiles),
        }

    def _list_dir(self, directory: Resource):
        return [file.stem for file in directory.path.iterdir()]

    def list_themes(self) -> List[str]:
        if not themes_dir.exists():
            raise PycrittyError(
                f'Failed listing themes, directory {themes_dir.path} not found'
            )

        return self._list_dir(themes_dir)

    def list_shells(self) -> List[str]:
        if not shells_dir.exists():
            raise PycrittyError(
                f'Failed listing shells, directory {shells_dir.path} not found'
            )
        return self._list_dir(shells_dir)

    def list_profiles(self) -> List[str]:
        Path( profiles_dir.path ).mkdir( parents=True, exist_ok=True )
        if not profiles_dir.exists():
            raise PycrittyError(
                f'Failed listing profiles, directory {profiles_dir.path} not found'
            )
        return self._list_dir(profiles_dir)

    def list_positions(self) -> List[str]:
        Path( positions_dir.path ).mkdir( parents=True, exist_ok=True )
        if not positions_dir.exists():
            raise PycrittyError(
                f'Failed listing positions, directory {positions_dir.path} not found'
            )
        return self._list_dir(positions_dir)

    def list_commands(self) -> List[str]:
        if not commands_dir.exists():
            raise PycrittyError(
                f'Failed listing commands, directory {commands_dir.path} not found'
            )
        return self._list_dir(commands_dir)

    def list_hosts(self) -> List[str]:
        if not hosts_dir.exists():
            raise PycrittyError(
                f'Failed listing hosts, directory {hosts_dir.path} not found'
            )
        return self._list_dir(hosts_dir)

    def list_pids(self) -> List[str]:
        pids = []
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info["name"] == "alacritty":
                if not proc.info["pid"] in pids:
                    pids.append(proc.info["pid"])
        return pids

    def list_configs(self) -> List[str]:
        if not saves_dir.exists():
            raise PycrittyError(f'Cannot list saves, {saves_dir} not found')

        return self._list_dir(saves_dir)

    def list_fonts(self) -> List[str]:
        if not fonts_file.exists():
            raise PycrittyError(
                f'Failed listing fonts, file {fonts_file.path} not found'
            )

        fonts_yaml = read_yaml(fonts_file)
        if fonts_yaml is None or 'fonts' not in fonts_yaml:
            fonts = []
        else:
            fonts = fonts_yaml['fonts'].keys()

        return fonts

    def print_list(self, option: str, iterable=True):
        header, color, get_list = self.options[option]
        if not iterable:
            log.color_print(f'{header}:', default_color=log.Color.BOLD)
        ls = get_list()
        tabs = '    ' if not iterable else ''
        if len(ls) < 1 and not iterable:
            log.color_print(log.Color.ITALIC, log.Color.YELLOW, f'{tabs}Empty directory')
        else:
            for item in ls:
                log.color_print(f'{tabs}{item}', default_color=color)
            
    def execute(self, args: Dict[str, Any]):
        iterable = False
        if 'iterable' in args:
            iterable = True
            args.pop('iterable')
        if len(args) < 1:
            args['all'] = True
        if 'all' in args:
            for opt in self.options:
                args[opt] = True
            args.pop('all')
        for opt in args:
            if opt in self.options:
                self.print_list(opt, iterable)
