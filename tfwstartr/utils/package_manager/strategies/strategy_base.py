from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Union


class InstallStrategy(ABC):
    @staticmethod
    @abstractmethod
    def install_packages(workdir: Union[str, Path], packages: Dict[str, str]) -> None:
        pass

    @staticmethod
    @abstractmethod
    def get_packages_from_file(file_content: str) -> Dict[str, str]:
        pass
