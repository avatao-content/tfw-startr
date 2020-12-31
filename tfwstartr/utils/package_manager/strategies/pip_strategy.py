import os
from typing import List, Dict, Union
from pathlib import Path
from .strategy_base import InstallStrategy


class PipInstallStrategy(InstallStrategy):
    @staticmethod
    def install_packages(
        workdir: Union[str, Path], packages: List[Dict[str, str]]
    ) -> None:
        with open(
            os.path.join(workdir, "solvable/webservice", "requirements.txt"), "a"
        ) as requirements:
            for package in packages:
                if not requirements.read().endswith('\n'):
                    requirements.write('\n')
                requirements.write(f"{package.get('name')}=={package.get('version')}")
