from typing import Dict, Callable, Any
from collections.abc import Mapping
from .command import Command
from .. import resources, PycrittyError
from ..io import log, yio
from rich import print, pretty, inspect
import json, base64, os, sys
import distutils.spawn

class ConfigError(PycrittyError):
    def __init__(self, message='Error applying configuration'):
        super().__init__(message)


class Pycritty(Command):
    """Applies changes to the config

    >>> conf = Pycritty()
    >>> conf.change_theme('dracula')
    >>> conf.change_font('UbuntuMono')
    >>> conf.apply()
    """

    def __init__(self):
        self.config = yio.read_yaml(resources.config_file.get_or_create())
        self.shell_changed = False
        self.local_paths = {
           'bash': distutils.spawn.find_executable("bash"),
           'alacritty': distutils.spawn.find_executable("alacritty"),
        }
        self.tmux_enabled = False
        self.host = None
        self.base_config = None
        self.user = None
        self.shell = None
        self.remote_host = None
        self.local_ports = []
        self.remote_port = 22
        self.remote_user = 'root'
        self.remote_cmd = None
        self.remote_args = []
        if self.config is None:
            self.config = {}
        inspect(self)

    def get_ssh_cmd(self):
        if self.remote_host == None:
            self.remote_host = self.host
        cmd = f"command ssh -tt -q -oUser={self.remote_user} -oHostname={self.remote_host} -oPort={self.remote_port} -oLogLevel=QUIET -oForwardAgent=yes -oStrictHostKeyChecking=no -tt -oControlMaster=auto"
        #-oRemoteCommand=\"{self.remote_cmd}\""
        if self.remote_cmd != None:
            cmd = f'{cmd} -oRemoteCommand=\"{self.remote_cmd}\"'
        cmd = f'{cmd} \"{self.host}\"'
        return cmd

    def apply(self):
        yio.write_yaml(self.config, resources.config_file)
    
    def execute(self, actions: Dict[str, Any]):
        if len(actions) < 1:
            log.warn('Nothing to do, use -h for help')
            return

        errors = 0
        for method, args in actions.items():
            try:
                call = getattr(self, method)
                call(args)
            except (PycrittyError, AttributeError) as e:
                log.err(e)
                errors += 1

        self.apply()

        if errors > 0:
            raise PycrittyError(f'\n{errors} error(s) found')

    def set(self, **kwargs):
        """Set multiple changes at once

        >>> conf = SetConfig()
        >>> conf.set(theme='onedark', font='UbuntuMono', font_size=14, opacity=1)
        >>> conf.apply()
        """

        options: Dict[str, Callable[[Any], Any]] = {
            'theme': self.change_theme,
            'font': self.change_font,
            'font_size': self.change_font_size,
            'font_offset': self.change_font_offset,
            'padding': self.change_padding,
            'opacity': self.change_opacity,
            'args': self.change_args,
            'shell': self.change_shell,
            'base_config': self.change_base_config,
        }

        for opt, arg in kwargs.items():
            if opt in options:
                options[opt](arg)

    def enable_tmux_mode(self, dat: bool):
        self.tmux_enabled = True
        print('tmux_enabled: ', self.tmux_enabled)

    def change_base_config(self, name: str):
        print('change_base_config: ', name)

    def change_theme(self, theme: str):
        theme_file = resources.get_theme(theme)
        if not theme_file.exists():
            raise PycrittyError(f'Theme "{theme}" not found')

        theme_yaml = yio.read_yaml(theme_file)
        if theme_yaml is None:
            raise ConfigError(f'File {theme_file} is empty')
        if 'colors' not in theme_yaml:
            raise ConfigError(f'{theme_file} does not contain color config')

        expected_colors = [
            'black',
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
            'white',
        ]

        expected_props = {
            'primary': ['background', 'foreground'],
            'normal': expected_colors,
            'bright': expected_colors,
        }

        for k in expected_props:
            if k not in theme_yaml['colors']:
                log.warn(f'Missing "colors:{k}" for theme "{theme}"')
                continue
            for v in expected_props[k]:
                if v not in theme_yaml['colors'][k]:
                    log.warn(f'Missing "colors:{k}:{v}" for theme "{theme}"')

        self.config['colors'] = theme_yaml['colors']
        log.ok(f'Theme {theme} applied')

    def change_font(self, font: str):
        if 'font' not in self.config:
            self.config['font'] = {}
            log.warn(f'"font" prop was not present in {resources.config_file}')

        fonts_file = resources.fonts_file.get_or_create()
        fonts = yio.read_yaml(fonts_file)
        if fonts is None:
            raise ConfigError(
                f'Failed changing font, file "{fonts_file}" is empty'
            )
        if 'fonts' not in fonts:
            raise ConfigError(
                f'Could not change font, "font" config not found in {fonts_file}'
            )

        fonts = fonts['fonts']
        if font not in fonts:
            raise ConfigError(
                f'Config for font "{font}" not found in {fonts_file}'
            )

        font_types = ['normal', 'bold', 'italic']

        if isinstance(fonts[font], str):
            font_name = fonts[font]
            fonts[font] = {}
            for t in font_types:
                fonts[font][t] = font_name

        if not isinstance(fonts[font], Mapping):
            raise ConfigError(
                f'Font "{font}" has wrong format at file {fonts_file}'
            )

        for t in font_types:
            if t not in fonts[font]:
                raise ConfigError(f'Font "{font}" does not have "{t}" property')
            if t not in self.config['font']:
                self.config['font'][t] = {'family': 'tmp'}
            self.config['font'][t]['family'] = fonts[font][t]

        log.ok(f'Font {font} applied')

    def change_font_size(self, size: float):
        if size <= 0:
            raise ConfigError('Font size cannot be negative or zero')

        if 'font' not in self.config:
            self.config['font'] = {}
            log.warn(f'"font" prop was not present in {resources.config_file}')
        self.config['font']['size'] = size
        log.ok(f'Font size set to {size:.1f}')

    def change_local_ports(self, local_ports: str):
        if ',' in local_ports:
            for lp in local_ports.split(','):
                if not lp in self.local_ports:
                    self.local_ports.append(int(lp, base=10))
        else:                    
            self.local_ports = [int(local_ports, base=10)]
        log.ok(f'changed local_ports to {self.local_ports}')

    def change_user(self, user: str):
        self.user = user
        log.ok(f'changed user to {self.user}')

    def change_host(self, host: str):
        self.host = host
        if host != 'localhost':
            self.remote_host = host
        log.ok(f'change host> host: {self.host}')

#            local_tmux = distutils.spawn.find_executable("tmux")
#            local_ssh = distutils.spawn.find_executable("ssh")
    def change_shell(self, shell: str):
        log.ok(f'Change shell > shell={shell}, args={self.remote_args}')
        self.shell_changed = True
        self.shell = shell
        if self.host != None:
            local_shell = distutils.spawn.find_executable("bash")
            if self.remote_host != None:
                self.remote_host = self.host
            if not 'shell' in dict(self.config).keys():
                log.warn(f'Config is missing shell property!')
                self.config['shell'] = {
                    'program': '',
                    'args': [],
                }
            print(dict(self.config).keys())
            if 'shell' in dict(self.config).keys():
                if not 'program' in self.config['shell'].keys():
                    log.warn(f'Config is missing program property!')
                self.config['shell']['program'] = local_shell
                log.ok(f'Set Program Path to Local Shell {local_shell} [REMOTE]')
            if len(self.remote_args) == 0:
                remote_args = [self.shell,'-il']
                self.change_args(remote_args)
                log.ok(f'Set Shell Args to {remote_args}')
        else:
            self.config['shell']['program'] = shell
            log.ok(f'Set Program to Shell {shell} [LOCAL]')
        self.test_shell()
        log.ok(f"Changed shell OK- {self.config['shell']['program']}")

    def change_args(self, args: str):
        if len(args) == 0:
            return
#        if not self.shell_changed:
#            self.change_shell()
        if type(args) == list:
            args_decoded = ' '.join(args)
        else:
            if not args in os.environ.keys():
                log.warn(f'env is missing key {args}')
            args_decoded = os.environ[args]
        print('args:', args)
        print('args decoded:', args_decoded)
        print('shell:', self.shell)
        #print('remote shell:', self.remote_shell)
        print('remote args:', self.remote_args)
        print('remote host:', self.remote_host)
        print('program:', self.config['shell']['program'])
        shell_args = []
#        shell_args = ["--norc","--noprofile","-ilc"]
#        shell_args = ["-ilc"]
        if self.config['shell']['program'] == 'bash' or self.config['shell']['program'].endswith('/bash'):
            shell_args.append("--norc")
            shell_args.append("--noprofile")

        shell_args.append("-il")
        if len(args_decoded) > 0:
            shell_args.append("-c")
            if self.host != None:
                self.remote_cmd = args_decoded
                shell_args.append(self.get_ssh_cmd())
            else:
                shell_args.append(args_decoded)
        self.config['shell']['args'] = shell_args
        log.ok(f'Set Args to {args} / {shell_args}')

    def test_shell(self):
        TA = ''
        on = 0
        for a in self.config['shell']['args']:
            if on == (len(self.config['shell']['args'])-1):
                a = a.replace('"','\\\"')
                TA = f'{TA} "{a}"'
            else:
                TA = f'{TA} {a}'
            on += 1
#        TA = ' '.join(
        test_cmd = f"{self.config['shell']['program']} {TA}"
        sys.stdout.write(test_cmd + "\n")

    def change_opacity(self, opacity: float):
        if opacity < 0.0 or opacity > 1.0:
            raise ConfigError('Opacity should be between 0.0 and 1.0')

        self.config['window']['opacity'] = opacity
        log.ok(f'Opacity set to {opacity:.2f}')

    def change_padding(self, padding=(1, 1)):
        if len(padding) != 2:
            raise ConfigError('Padding should only have an x and y value')

        x, y = padding
        if 'window' not in self.config:
            self.config['window'] = {}
            log.warn(f'"window" prop was not present in {resources.config_file}')
        if 'padding' not in self.config['window']:
            self.config['window']['padding'] = {}
            log.warn(f'"padding" prop was not present in {resources.config_file}')

        self.config['window']['padding']['x'] = x
        self.config['window']['padding']['y'] = y
        log.ok(f'Padding set to x: {x}, y: {y}')

    def change_font_offset(self, offset=(0, 0)):
        if len(offset) != 2:
            raise ConfigError('Wrong offset format, should be (x, y)')

        x, y = offset
        if 'font' not in self.config:
            self.config['font'] = {}
        if 'offset' not in self.config['font']:
            log.warn('"offset" prop was not set')
            self.config['font']['offset'] = {}

        self.config['font']['offset']['x'] = x
        self.config['font']['offset']['y'] = y
        log.ok(f'Offset set to x: {x}, y: {y}')
