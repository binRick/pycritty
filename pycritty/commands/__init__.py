from .pycritty import Pycritty
from .ls import ListResource
from .save import SaveConfig
from .create import CreateBinary
from .run import RunConfig
from .load import LoadConfig
from .install import Install
from .rm import Remove

subcommands = {
    'ls': ListResource,
    'save': SaveConfig,
    'run': RunConfig,
    'binary': CreateBinary,
    'load': LoadConfig,
    'install': Install,
    'rm': Remove,
}
