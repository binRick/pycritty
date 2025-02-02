from pathlib import Path
from .resource import ConfigFile,  ConfigDir


base_dir = ConfigDir(Path().home() / '.config' / 'alacritty')
config_file = ConfigFile(base_dir.path, 'alacritty', ConfigFile.YAML)
fonts_file = ConfigFile(base_dir.path, 'fonts', ConfigFile.YAML)
themes_dir = ConfigDir(base_dir.path / 'themes')
saves_dir = ConfigDir(base_dir.path / 'saves')
hosts_dir = ConfigDir(base_dir.path / 'hosts')
shells_dir = ConfigDir(base_dir.path / 'shells')
commands_dir = ConfigDir(base_dir.path / 'commands')
positions_dir = ConfigDir(base_dir.path / 'positions')
positions_dir = ConfigDir(base_dir.path / 'positions')
profiles_dir = ConfigDir(base_dir.path / 'profiles')
tmuxp_profiles_dir = ConfigDir(base_dir.path / 'tmuxp')


def get_theme(theme: str) -> ConfigFile:
    return ConfigFile(themes_dir.get_or_create(), theme, ConfigFile.YAML)
