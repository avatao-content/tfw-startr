from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Union


class InstallStrategy(ABC):
    @staticmethod
    @abstractmethod
    def install_packages(
        workdir: Union[str, Path], packages: List[Dict[str, str]]
    ) -> None:
        pass
