import json
import os
import shutil
import secrets
import importlib.resources
from functools import cached_property
from typing import List, Dict, Optional
from git import repo
from .config import STARTER_WORKDIR
from .utils import GitHelper


class Startr:
    def __init__(self) -> None:
        self._git_helper = GitHelper()
        self._languages = self.__load_starters()
        self._archive: str = ''

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if os.path.exists(self._archive):
            os.remove(self._archive)

    @staticmethod
    def __load_starters():
        data = importlib.resources.read_text(__package__, "languages.json")
        return json.loads(data)

    @cached_property
    def languages(self):
        return self._languages  # TODO: filter the extra JSON fields

    def prepare_and_zip(
        self,
        language_name: str,
        framework_name: str,
        starter_name: str,
        extra_packages: Optional[List[Dict[str, str]]] = None,
    ) -> str:
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
        
        workdir = os.path.join(STARTER_WORKDIR, f'{starter_name}-{secrets.token_hex(6)}')
        print(f'Workdir is {workdir}')
        # clone
        self._git_helper.clone_repo(repo_url, workdir, branch)
        print(f'Cloning done, wokrdir content is: {os.listdir(workdir)}')
        # install extra_packages (if any)
        if extra_packages:
            pass  # TODO

        # delete .git folder
        self.__cleanup_directory(os.path.join(workdir, ".git"))
        print(f".git dir deleted at {os.path.join(workdir, '.git')}")
        # git init
        self._git_helper.init_starter_repo(workdir)
        print(f'.git init at {workdir}')
        # zip 
        self._archive = self.__generate_zip(workdir)
        return self._archive

    @staticmethod
    def __cleanup_directory(dir_path: str) -> None:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    @staticmethod
    def __generate_zip(dir_path: str) -> str:
        return shutil.make_archive(
            base_name=dir_path,
            format="zip",
            root_dir=dir_path,
        )
