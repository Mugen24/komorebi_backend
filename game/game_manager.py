from game.manual_game import ManualGame
from game.steam_game import SteamGame
from game.game_base import AbstractGame, GameConfig
import json
from pathlib import Path


class GameManager():
    GAME_READERS = {
            "steam": SteamGame,
            "manual": ManualGame
    }

    def __init__(self, games_folder: Path) -> None:
        self.games_folder = games_folder
        self.games: list[AbstractGame] = []
        self.load_games()

    def load_games(self):
        for game_folder in self.games_folder.iterdir():
            config_file = game_folder / "config.json"

            game: AbstractGame | None = None

            if config_file.exists() and config_file.is_file():
                config: GameConfig = json.loads(config_file.read_text())
                print(f"Config found at {config_file}")
                try: 
                    game = GameManager.GAME_READERS[config["config_type"]].from_config(game_folder, config_file)
                except KeyError as e: 
                    print(f"{game_folder.stem}")
                    # print(f"{game_folder.stem} config_type {config['config_type']} not implemented")
                    continue
            else:
                for key, reader in GameManager.GAME_READERS.items():
                    try:
                        game = reader.create(game_path=game_folder)
                    except Exception as e:
                        print("Exception:", e)
                        continue

                    if game is not None:
                        game.save_config()
                        break

            if game is not None:
                self.games.append(game)
                
    def list_games(self):
        print(self.games)
        return self.games

    def get_game(self, id: str) -> AbstractGame | None:
        for game in self.games:
            print(game)
            if game.id == id:
                return game

        print(f"Cannot find game of id: {id}")


