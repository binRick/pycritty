from typing import Dict, Any, Union
import sys
from pathlib import Path
from .. import PycrittyError
from .command import Command
from ..io import log, yio
from ..resources import config_file, saves_dir
from ..resources.resource import ConfigFile
from rich import print, pretty, inspect
from rich.console import Console
from .pycritty import Pycritty
console = Console()


class RunConfig(Command):
    def run_config(
        self,
        config_name: str,
        read_from: Union[str, Path, ConfigFile] = config_file,
        dest_parent=saves_dir,
        override=False
    ):
        dest_file = ConfigFile(dest_parent.get_or_create(), config_name, ConfigFile.YAML)
        if dest_file.exists() and not override:
            raise PycrittyError(
                f'Config "{config_name}" already exists, use -o to override'
            )

        conf = yio.read_yaml(read_from)
        if conf is None or len(conf) < 1:
            log.warn(f'"{read_from}" has no content')
        else:
            dest_file.create()
            yio.write_yaml(conf, dest_file)
            log.ok('Config saved =>', log.Color.BLUE, dest_file)
            if False:
               print(conf)
               console.print("Hello", "World!", style="bold red")
               console.print(":smiley: :vampire: :pile_of_poo: :thumbs_up: :raccoon:")



    def execute(self, args: Dict[str, Any]):
        #inspect(args, all=True)
        new_conf = Pycritty()
        if False:
            pass
        if True:
            if 'change_base_config' in dict(args).keys():
                new_conf.base_config=args['change_base_config']
            if 'change_host' in dict(args).keys():
    #            new_conf.host = args['change_host']
                new_conf.change_host(args['change_host'])
            if 'change_font' in dict(args).keys():
                new_conf.font =args['change_font']

            if 'change_shell' in dict(args).keys():
                new_conf.shell = args['change_shell']
            if 'change_user' in dict(args).keys():
                new_conf.change_user(args['change_user'])
            if 'change_font_size' in dict(args).keys():
                new_conf.font_size = args['change_font_size']
            if 'change_theme' in dict(args).keys():
                new_conf.theme = args['change_theme']
            if 'change_args' in dict(args).keys():
                new_conf.change_args(args['change_args'])
            if 'change_position' in dict(args).keys():
                new_conf.change_position(args['change_position'])
        if True:
            exec_cmd = f'eval ssh '
            exec_cmd = new_conf.get_ssh_cmd()
            exec_cmd = f"{exec_cmd} \"{new_conf.config['shell']['program']}"
            for a in new_conf.config['shell']['args']:
                exec_cmd = f"{exec_cmd} {a}"
            exec_cmd = f"{exec_cmd}\""
            print(exec_cmd)
            Args = ['bash','--noprofile','--norc', exec_cmd]
            new_conf.config['shell']['args'] = Args
            new_conf.config['shell']['program'] = 'env'
        if False:
            print(new_conf.config)
        if False:
            pass
        if True:
            print(new_conf.config['shell'])
            print('args>', dict(args))
        if False:
            inspect(new_conf, private=True, methods=True)
            console.print(f"\nRUNNING > :smiley: \n#{exec_cmd}\n", style="bold yellow")
#        print(new_conf)
        #>>> conf.apply()        
        #config_name = actions['name']
        #override = 'override' in actions
        #self.run_config(config_name, override=override)
