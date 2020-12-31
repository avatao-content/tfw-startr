import yaml
import os
import shutil
import secrets
import tempfile
import importlib.resources
from functools import cached_property
from typing import Dict, Optional, Union
from pathlib import Path
from .config import STARTER_WORKDIR
from .utils import GitHelper, PackageManager


class Startr:
    def __init__(self) -> None:
        self._git_helper = GitHelper()
        self._package_manager = PackageManager
        self._languages = self.__load_starters()
        self._archive: Union[str, Path] = ""

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if os.path.exists(self._archive):
            os.remove(self._archive)

    @staticmethod
    def __load_starters():
        data = importlib.resources.read_text(__package__, "languages.yaml")
        return yaml.safe_load(data)

    @cached_property
    def languages(self):
        return self._languages  # TODO: filter the extra JSON fields

    def prepare_and_zip(
        self,
        language_name: str,
        framework_name: str,
        starter_name: str,
        extra_packages: Optional[Dict[str, str]] = None,
    ) -> Union[str, Path]:
        repo_url: str = self._languages.get("languages").get(language_name).get("repo")
        branch: str = (
            self._languages.get("languages")
            .get(language_name)
            .get("frameworks")
            .get(framework_name)
            .get("starters")
            .get(starter_name)
            .get("branch")
        )
        package_manager: str = (
            self._languages.get("languages")
            .get(language_name)
            .get("frameworks")
            .get(framework_name)
            .get("starters")
            .get(starter_name)
            .get("package_manager")
        )

        with tempfile.TemporaryDirectory() as workdir:
            self._git_helper.clone_repo(repo_url, workdir, branch)
            if extra_packages:
                self._package_manager.install_packages(
                    workdir=workdir,
                    packages=extra_packages,
                    package_manager=package_manager,
                )

            self.__cleanup_directory(os.path.join(workdir, ".git"))
            self._git_helper.init_starter_repo(workdir)
            self._archive = self.__generate_zip(
                archive_name=os.path.join(
                    STARTER_WORKDIR, f"{starter_name}-{secrets.token_hex(6)}"
                ),
                directory=workdir,
            )
            return self._archive

    @staticmethod
    def __cleanup_directory(dir_path: Union[str, Path]) -> None:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    @staticmethod
    def __generate_zip(
        archive_name: str, directory: Union[str, Path]
    ) -> Union[str, Path]:
        return shutil.make_archive(
            base_name=archive_name,
            format="zip",
            root_dir=directory,
        )
