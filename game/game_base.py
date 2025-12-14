from abc import abstractmethod
import json
import requests
from typing import Any, Literal, TypedDict
from pprint import pprint
from pathlib import Path
import textwrap
from uuid import uuid4
from abc import ABC

class SteamShortCut(TypedDict):
    working_dir: str
    executable_path: str
    name: str
    arguments: str

class GameConfig(SteamShortCut):
    config_type: Literal["steam", "manual"]
    id: str


class GameAssets(ABC):
    def __init__(self, game_folder: Path) -> None:
        super().__init__()
        self.game_folder = game_folder

        self.icon_path = game_folder / "icon.ico"
        self.capsule_path = game_folder / "capsule.jpg"
        self.hero_path = game_folder / "hero.jpg"
        self.logo_path = game_folder / "logo.png"
    
    def check_asset_exists(self, path: Path):
        if path.exists():
            print(f"{path} already exists skipping download")
            return True
        print(f"downloading {path.stem} to {path}")
        return False

    @abstractmethod
    def get_icon_url(self) -> str:
        pass

    @abstractmethod
    def get_capsule_url(self) -> str:
        pass

    @abstractmethod
    def get_hero_url(self) -> str:
        pass

    @abstractmethod
    def get_logo_url(self) -> str:
        pass


    def download_icon(self) -> bool:
        path = self.icon_path
        if self.check_asset_exists(path): return False

        url = self.get_icon_url()
        resp = requests.get(url)
        with path.open("wb+") as fp:
            fp.write(resp.content)

        return True

    def download_capsule(self) -> bool:
        path = self.capsule_path
        if self.check_asset_exists(path): return False

        url = self.get_capsule_url()
        resp = requests.get(url)
        with path.open("wb+") as fp:
            fp.write(resp.content)

        return True

    def download_hero(self) -> bool:
        path = self.hero_path
        if self.check_asset_exists(path): return False

        url = self.get_hero_url()
        resp = requests.get(url)
        with path.open("wb+") as fp:
            fp.write(resp.content)
        return True

    def download_logo(self) -> bool:
        path = self.logo_path
        if self.check_asset_exists(path): return False

        url = self.get_logo_url()
        resp = requests.get(url)
        with path.open("wb+") as fp:
            fp.write(resp.content)
        return True

    def fetch_assets_if_needed(self):
       self.download_icon()
       self.download_capsule()
       self.download_hero()
       self.download_logo()



class AbstractGame(ABC):
    def __init__(
            self, 
            *,
            id: str, 
            working_dir: Path, 
            executable_path: Path, 
            name: str, 
            arguments: str,
            game_folder: Path,
            assets: GameAssets,
        ) -> None:

        super().__init__()
        self.id = id
        self.working_dir = working_dir
        self.executable_path = executable_path
        self.name = name
        self.arguments = arguments

        self.games_folder = game_folder
        self.config_path = game_folder / "config.json"
        self.assets = assets

    @classmethod
    @abstractmethod
    #Generate class from config file
    def from_config(cls, game_path: Path, config_file: Path) -> "AbstractGame":
        pass


    @classmethod
    @abstractmethod
    #generate class by fetching other sources
    def create(cls, game_path: Path) -> "AbstractGame | None":
        pass

    @abstractmethod
    #construct a json config that can be loaded later on
    def construct_save_config(self) -> GameConfig:
        pass

    @staticmethod
    def generate_id():
        return f"{uuid4().int}"

    def create_steam_shortcut(self) -> SteamShortCut:
        return {
            "working_dir": self.working_dir.as_posix(),
            "executable_path": self.executable_path.as_posix(),
            "name": self.name,
            "arguments": self.arguments,
        }

    def save_config(self):
        print(f"saving config {self.config_path}")
        with self.config_path.open("w+") as fp:
            fp.write(json.dumps(self.construct_save_config()))


    def __repr__(self) -> str:
        return textwrap.dedent(f"""
            working_dir: {self.working_dir}
            executable_path: {self.executable_path}
            name: {self.name}
            arguments: {self.arguments}
        """)





    








