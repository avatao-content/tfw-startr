from typing import Dict, Type
from .strategy_base import InstallStrategy
from .pip_strategy import PipInstallStrategy
from .npm_strategy import NpmInstallStrategy


strategy_mapping: Dict[str, Type[InstallStrategy]] = {
    "pip": PipInstallStrategy,
    "npm": NpmInstallStrategy
}
