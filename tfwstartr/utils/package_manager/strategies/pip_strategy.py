import os
from typing import Dict, Union
from pathlib import Path
from .strategy_base import InstallStrategy


class PipInstallStrategy(InstallStrategy):
    @staticmethod
    def install_packages(workdir: Union[str, Path], packages: Dict[str, str]) -> None:
        with open(
            os.path.join(workdir, "solvable/webservice", "requirements.txt"), "a"
        ) as requirements:
            for name, version in packages:
                if not requirements.read().endswith("\n"):
                    requirements.write("\n")
                requirements.write(f"{name}=={version}")

    @staticmethod
    def get_packages_from_file(file_content: str) -> Dict[str, str]:
        packages = {}
        lines = file_content.split("\n")
        for line in lines:
            name, version = line.strip().split("==")
            packages[name] = version
        return packages
