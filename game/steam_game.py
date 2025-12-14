from pathlib import Path
from game.game_base import AbstractGame, GameAssets, GameConfig
from utils.steam_api import GameInfo, SteamMetadata
from utils.utils import locate_launch_config
import json
import textwrap

class SteamConfig(GameConfig):
    app_id: int
    steam_config: GameInfo

class SteamAssets(GameAssets):
   def __init__(self, *, app_id: int, game_folder: Path, steam_config: GameInfo):
      super().__init__(game_folder=game_folder)

      self.steam_info = steam_config
      self.app_id = app_id
      self.library_assets = self.steam_info["common"]["library_assets_full"]
      self.game_folder = game_folder

      self.icon_path = self.game_folder / "icon.ico"
      self.capsule_path = self.game_folder / "capsule.jpg"
      self.hero_path = self.game_folder / "hero.jpg"
      self.logo_path = self.game_folder / "logo.png"


   def get_icon_url(self):
      # iamge that gets overlayed onto the hero (bottom left)
      url = f"https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/{self.app_id}/{self.steam_info['common']['clienticon']}.ico"
      return url

   def get_capsule_url(self):
      # image that shows up in library overview
      # url = f"https://shared.steamstatic.com/store_item_assets/steam/apps/${self.app_id}/${self.library_assets["library_capsule"]["image"]["english"]}t=${meta.store_asset_mtime}"
      url = f"https://shared.steamstatic.com/store_item_assets/steam/apps/{self.app_id}/{self.library_assets['library_capsule']['image']['english']}"
      return url

   # def get_library_wide_capsule(self):
   #    # we don't really need this
   #    url = f"https://shared.steamstatic.com/store_item_assets/steam/apps/${self.app_id}/${self.meta.header_image_full[lang]}?t=${meta.store_asset_mtime}"

   def get_hero_url(self):
      # image that shows up in game detail page
      url = f"https://shared.steamstatic.com/store_item_assets/steam/apps/{self.app_id}/{self.library_assets['library_hero']['image']['english']}"
      return url

   def get_logo_url(self):
      url = f"https://shared.steamstatic.com/store_item_assets/steam/apps/{self.app_id}/{self.library_assets['library_logo']['image']['english']}"
      return url

class SteamGame(AbstractGame):
    def __init__(
        self, 
        game_folder: Path,
        working_dir: Path,
        executable_path: Path,
        app_id: int,
        name: str,
        arguments: str,
        id: str,
        steam_config: GameInfo,
        assets: GameAssets

    ) -> None:
        super().__init__(
                id=id,
                working_dir=working_dir,
                executable_path=executable_path,
                name=name,
                arguments=arguments,
                game_folder=game_folder,
                assets=assets
        )

        self.app_id = app_id
        self.steam_config = steam_config
        self.steamcli = SteamMetadata.create() 

    @classmethod
    def from_config(cls, game_path: Path, config_file: Path):
            config: SteamConfig = json.loads(config_file.read_text())
            # self.size = config["size"]
            return cls(
                game_folder=game_path,
                working_dir = Path(config["working_dir"]) ,
                executable_path = Path(config["executable_path"]),
                app_id = config["app_id"],
                name = config["name"],
                arguments = config["arguments"],
                id = config["id"],
                steam_config=config["steam_config"],
                assets=SteamAssets(app_id=config["app_id"], game_folder=game_path, steam_config=config["steam_config"])
            )


    @classmethod
    def create(cls, game_path: Path) -> "SteamGame | None":
        print("Generating config from steam")
        # chose the first option return from store
        OPTION_INDEX = 0
        MAX_OPTION = 10

        steamcli = SteamMetadata.create()
        game_folder = game_path

        store_results = steamcli.store_search(game_folder.name)

        if len(store_results.items) <= 0:
            raise Exception(f"Cannot find game: {game_folder.name} on steam. Perhaps folder was not formatted to game name?")

        for key, item in enumerate(store_results.items):
            if key >= MAX_OPTION:
                break
            print(textwrap.dedent(f"""{key}: {item.name}"""))
        
        print(game_folder)
        selected_game = input("Select game [q=quit]: ")
        if selected_game == "q":
            raise Exception("Quit")

        # pick the first game that was return
        game_overview = store_results.items[OPTION_INDEX]

        app_name = game_overview.name
        app_id = game_overview.app_id

        # get launch configuration
        game_config: GameInfo = steamcli.get_game_configuration(app_id) 
        
        # get the the default launch config
        if game_config.get("config") is None or game_config["config"].get("launch") is None:
            print(game_config)
            raise Exception(f"Game: {app_name} has no launch config")


        launch_configs = game_config["config"]["launch"]

        suitable_launch_config = None
        for launch_key, launch_config in launch_configs.items():

            # Ignore 84x architecture
            # bruh why no type inference??
            # TODO: probably macos as well
            if launch_config.get("config") is not None: 
                os_config = launch_config.get("config")
                assert(os_config is not None)
                if os_config.get("osarch") == "32": 
                    continue

                if os_config.get("oslist") == "macos":
                    continue


            result = locate_launch_config(game_folder, launch_config)
            if result is not None:
                suitable_launch_config = result
                break


        if suitable_launch_config is not None:
            return cls(
                        game_folder=game_folder,
                        working_dir=suitable_launch_config["working_dir"],
                        executable_path=suitable_launch_config["executable_path"],
                        app_id=app_id,
                        name=app_name,
                        arguments=suitable_launch_config["arguments"],
                        id=AbstractGame.generate_id(),
                        steam_config=game_config,
                        assets=SteamAssets(app_id=app_id, game_folder=game_folder, steam_config=game_config)
            )
        else:
            #TODO: work on this
            raise Exception(f"Cannot location executable directory: ")

    # Return a steamshortcut compatible json
    def construct_save_config(self) -> SteamConfig:
        return {
                "working_dir": self.working_dir.as_posix(),
                "executable_path": self.executable_path.as_posix(), 
                "name": self.name,
                "arguments": self.arguments,
                "id": self.id, 
                "app_id": self.app_id,
                "steam_config": self.steam_config,
                "config_type": "steam"
        }
