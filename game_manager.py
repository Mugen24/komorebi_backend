import json
from typing import Any
from pprint import pprint
from steam_assets import SteamAssets
from utils.steam_api import GameInfo, SteamMetadata
from pathlib import Path
import textwrap
from uuid import uuid4
    
class Game():
    def __init__(
        self, 
        game_folder: Path,
        working_dir: Path | None,
        executable_path: Path | None,
        app_id: int | None, # may not be a steam game
        name: str,
        arguments: str | None,
        id: str,
        steam_config: GameInfo
    ) -> None:


        self.root = game_folder
        self.config_folder = game_folder / "config.json"

        self.working_dir = working_dir
        self.executable_path = executable_path
        self.app_id = app_id
        self.name = name
        self.arguments = arguments
        self.id = id
        self.steam_config = steam_config

        self.steamcli = SteamMetadata.create() 

        if self.app_id is not None:
            self.assets = SteamAssets(self.app_id, game_folder=self.root, steam_config=steam_config)
        else:
            self.assets = None



    def save_config(self):
        config = {
            # "size": self.size,
            "working_dir": self.working_dir.as_posix() if self.working_dir else None,
            "executable_path": self.executable_path.as_posix() if self.executable_path else None,
            "app_id": self.app_id,
            "name": self.name,
            "arguments": self.arguments,
            "id": self.id,
            "steam_config": self.steam_config
        }

        #TODO: add this in after testing
        # if self.config_folder.exists():
        #     print(f"Config already exists")
        #     pass

        self.config_folder.touch()
        self.config_folder.write_text(json.dumps(config))


    @staticmethod
    def from_config(game_folder: Path):
        config_file = game_folder / "config.json"
        if config_file.exists() and config_file.is_file():
            print(f"config.json found for {config_file.parent}")
            config = json.loads(config_file.read_text())


            # self.size = config["size"]
            return Game(
                game_folder=game_folder,

                working_dir = Path(config["working_dir"]) if config["working_dir"] else None,
                executable_path = Path(config["executable_path"]) if config["executable_path"] else None,

                app_id = config["app_id"],
                name = config["name"],
                arguments = config["arguments"],
                id = config["id"],
                steam_config=config["steam_config"]
            )
        return None


    @staticmethod
    def generate_id():
        return f"{uuid4().int}"

    
    @staticmethod
    def _location_launch_config(steam_config: GameInfo):
        pass

    @staticmethod
    def generate_config_from_steam(game_folder: Path) -> "Game":
        # chose the first option return from store
        OPTION_INDEX = 0

        steamcli = SteamMetadata.create()

        game_folder = game_folder
        steam_config = steamcli.store_search(game_folder.name)

        if len(steam_config.items) <= 0:
            raise Exception(f"Cannot find game: {game_folder.name} on steam. Perhaps folder was not formatted to game name?")

        # pick the first game that was return
        game_overview = steam_config.items[OPTION_INDEX]

        app_name = game_overview.name
        app_id = game_overview.app_id

        # get launch configuration
        game_config = steamcli.get_game_configuration(app_id) 


        # get the the default launch config
        # pprint(game_config["config"])
        default_launch_config = game_config["config"]["launch"]["0"]

        arguments = default_launch_config.get("arguments")


        # replace window \ with linux /
        executable_name = default_launch_config["executable"].replace("\\", "/")

        try:
            # search for executable_name in file
            # executable_name can be a path ex. x86/hades.exe
            #TODO: try out all different launch_config if fails
            executable_path = [file for file in game_folder.glob(f"**/{executable_name}")][0]
        except IndexError as e:
            print(f"Cannot find executable {executable_name}")
            print(e)
            raise Exception()

        try:
            # use workingdir from steam 
            # if not default to the parent folder of exe
            working_dir = default_launch_config.get("workingdir")

            if working_dir:
                workingdir = working_dir.replace("\\", "/")
                working_dir = [dir for dir in game_folder.glob(f"**/{workingdir}")][0]
            else:
                working_dir = executable_path.parent

        except IndexError as e:
            print(f"Cannot find working directory of {executable_name}")
            print(default_launch_config)
            print(e)
            raise Exception()


        working_dir = Path(working_dir.relative_to(game_folder))
        executable_path = Path(executable_path.relative_to(game_folder))

        return Game(
                    game_folder=game_folder,
                    working_dir=working_dir,
                    executable_path=executable_path,
                    app_id=app_id,
                    name=app_name,
                    arguments=arguments,
                    id=Game.generate_id(),
                    steam_config=game_config
        )

    def __repr__(self) -> str:
        return textwrap.dedent(f"""
            working_dir: {self.working_dir}
            executable_path: {self.executable_path}
            app_id: {self.app_id}
            name: {self.name}
            arguments: {self.arguments}
            id: {self.id} 
        """)

    def to_json(self) -> dict[str, Any]:
        return {
            "working_dir": self.working_dir.as_posix() if self.working_dir else None,
            "executable_path": self.executable_path.as_posix() if self.executable_path else None, 
            "app_id": self.app_id,
            "name": self.name,
            "arguments": self.arguments,
            "id": self.id, 
        }





class GameManager():
    def __init__(self, games_folder: Path) -> None:
        self.games_folder = games_folder
        self.games: list[Game] = []

        self.load_games()

    def load_games(self):
        for game_folder in self.games_folder.iterdir():
            print(f"Loading game config for: {game_folder.stem}")
            game = Game.from_config(game_folder)
            if game is None:
                game = Game.generate_config_from_steam(game_folder)
                game.save_config()

            self.games.append(game)

    def list_games(self):
        print(self.games)
        return self.games

    def get_game(self, id: str) -> Game | None:
        for game in self.games:
            print(game)
            if game.id == id:
                return game

        print(f"Cannot find game of id: {id}")








