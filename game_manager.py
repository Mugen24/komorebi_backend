import json
from typing import Any
from config_manager import Config
from pprint import pprint
from utils.steam_api import SteamMetadata
from pathlib import Path
import textwrap
from uuid import uuid4

class Game():
    def __init__(self, game_folder: Path) -> None:
        self.root = game_folder
        self.steamcli = SteamMetadata.create() 
        self.config = Config(game_folder)

        if not self.config.load():
            self.config.id = self.generate_id()
            self.generate_config_from_steam()
            self.config.write()



        
    def generate_id(self):
        return f"{uuid4().int}"

    def generate_config_from_steam(self):
        # chose the first option return from store
        OPTION_INDEX = 0
        game_folder = self.root
        
        steam_config = self.steamcli.store_search(game_folder.name)

        if len(steam_config.items) <= 0:
            raise Exception(f"Cannot find game: {game_folder.name} on steam. Perhaps folder was not formatted to game name?")

        # pick the first game that was return
        game_overview = steam_config.items[OPTION_INDEX]
        self.config.name = game_overview.name
        self.config.app_id = game_overview.app_id

        # get launch configuration
        game_config = self.steamcli.get_game_configuration(self.config.app_id) 


        # get the the default launch config
        default_launch_config = game_config.launch[0]
        self.config.arguments = default_launch_config.arguments


        # replace window \ with linux /
        executable_name = default_launch_config.executable.replace("\\", "/")

        try:
            # search for executable_name in file
            # executable_name can be a path ex. x86/hades.exe
            executable_path = [file for file in game_folder.glob(f"**/{executable_name}")][0]
        except IndexError as e:
            print(f"Cannot find executable {executable_name}")
            print(e)
            return

        try:
            # use workingdir from steam 
            # if not default to the parent folder of exe
            if default_launch_config.workingdir:
                default_launch_config.workingdir = default_launch_config.workingdir.replace("\\", "/")
                working_dir = [dir for dir in game_folder.glob(f"**/{default_launch_config.workingdir}")][0]
            else:
                working_dir = executable_path.parent
        except IndexError as e:
            print(f"Cannot find working directory of {executable_name}")
            print(default_launch_config)
            print(e)
            return


        self.config.working_dir = Path(working_dir.relative_to(game_folder))
        self.config.executable_path = Path(executable_path.relative_to(game_folder))

    def __repr__(self) -> str:
        return textwrap.dedent(f"""
            working_dir: {self.config.working_dir}
            executable_path: {self.config.executable_path}
            app_id: {self.config.app_id}
            name: {self.config.name}
            arguments: {self.config.arguments}
            id: {self.config.id} 
        """)

    def toJSON(self) -> dict[str, Any]:
        return {
            "working_dir": self.config.working_dir.as_posix() if self.config.working_dir else None,
            "executable_path": self.config.executable_path.as_posix() if self.config.executable_path else None, 
            "app_id": self.config.app_id,
            "name": self.config.name,
            "arguments": self.config.arguments,
            "id": self.config.id, 
        }



class GameManager():
    def __init__(self, game_folder: Path) -> None:
        self.game_folder = game_folder
        self.games: list[Game] = []

        self.load_games()

    def load_games(self):
        for game in self.game_folder.iterdir():
            self.games.append(Game(game))

    def list_games(self):
        print(self.games)
        return self.games

    def get_game(self, id: str):
        for game in self.games:
            print(game)
            if game.config.id == id:
                return game

        print(f"Cannot find game of id: {id}")








