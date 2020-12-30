from typing import List, Dict, Union
from pathlib import Path
from .strategies import strategy_mapping


class PackageInstaller:
    @staticmethod
    def install_packages(
        workdir: Union[str, Path], packages: List[Dict[str, str]], package_manager: str
    ):
        strategy = strategy_mapping.get(package_manager)
        strategy.install_packages(workdir=workdir, packages=packages)
