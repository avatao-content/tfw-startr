from typing import Dict, Type
from .strategy_base import InstallStrategy
from .pip_strategy import PipInstallStrategy


strategy_mapping: Dict[str, Type[InstallStrategy]] = {
    "pip": PipInstallStrategy,
}
