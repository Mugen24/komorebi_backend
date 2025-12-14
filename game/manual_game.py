from game.game_base import AbstractGame, GameAssets, GameConfig
from pathlib import Path
import json

class ManualGameConfig(GameConfig):
    pass


#TODO: Implement this
class ManualGameAssets(GameAssets):
    def __init__(self, game_folder: Path) -> None:
        super().__init__(game_folder)

    def get_icon_url(self) -> str:
        return "https://img.itch.zone/aW1nLzE4MTU5MDk4LnBuZw==/315x250%23c/eRBg8u.png"

    def get_capsule_url(self) -> str:
        return "https://img.itch.zone/aW1nLzE4MTU5MDk4LnBuZw==/315x250%23c/eRBg8u.png"

    def get_hero_url(self) -> str:
        return "https://img.itch.zone/aW1nLzE4MTU5MDk4LnBuZw==/315x250%23c/eRBg8u.png"

    def get_logo_url(self) -> str:
        return "https://img.itch.zone/aW1nLzE4MTU5MDk4LnBuZw==/315x250%23c/eRBg8u.png"


class ManualGame(AbstractGame):
    def __init__(self, *, id: str, working_dir: Path, executable_path: Path, name: str, arguments: str, game_folder: Path, assets: GameAssets) -> None:
        super().__init__(id=id, working_dir=working_dir, executable_path=executable_path, name=name, arguments=arguments, game_folder=game_folder, assets=assets)

    @classmethod
    def create(cls, game_path: Path) -> "ManualGame":

        working_dir = Path(input("working_dir: "))
        executable_path = Path(input("executable_path: "))
        name = input("name: ")
        game_folder = game_path
        id = ManualGame.generate_id()
        assets = ManualGameAssets(game_folder=game_path)

        return cls(id=id, working_dir=working_dir, executable_path=executable_path, name=name, game_folder=game_folder, arguments="", assets=assets)

    @classmethod
    def from_config(cls, game_path: Path, config_file: Path) -> "ManualGame":
        config: ManualGameConfig = json.loads(config_file.read_text())
        assets = ManualGameAssets(game_path)
        return cls(
                id=config["id"], 
                working_dir=Path(config["working_dir"]),
                executable_path=Path(config["executable_path"]),
                name=config["name"],
                game_folder=Path(game_path),
                arguments=config["arguments"],
                assets=assets
        )


    def construct_save_config(self) -> GameConfig:
        return {
            "id": self.id,
            "config_type": "manual",
            "arguments": self.arguments,
            "executable_path": self.executable_path.as_posix(),
            "name": self.name,
            "working_dir": self.working_dir.as_posix()
        }







if __name__ == "__main__":
    ManualGame()
