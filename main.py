import logging
from pathlib import Path
from os import getenv, wait
from dataclasses import dataclass
from logging import Logger
from utils.steam_types import URL
from utils.steam_api import SteamMetadata
from game_manager import GameManager
from fastapi import FastAPI, Response, status
from fastapi.responses import FileResponse 
from shutil import make_archive
import tempfile



DEBUG = 1
GAME_LIBRARY_FOLDER = Path(getenv("GAME_PATH"))

logger = logging.getLogger(__name__)

class KomorebiServer():
    instance: 'KomorebiServer | None'= None
    DEFAULT_GAME_PATH: Path
    DEFAULT_SAVE_PATH: Path
    def __init__(self) -> None:
        SERVER_ROOT = getenv("SEVER_ROOT")
        self.SERVER_ROOT = Path(SERVER_ROOT) if SERVER_ROOT else Path("~/.komorebi")

        GAME_PATH = getenv("GAME_PATH")
        self.GAME_PATH = Path(GAME_PATH) if GAME_PATH else self.SERVER_ROOT / "games"

        SAVE_PATH = getenv("SAVE_PATH")
        self.SAVE_PATH = Path(SAVE_PATH) if SAVE_PATH else self.SERVER_ROOT / "saves"

        if DEBUG:
            self.GAME_PATH = GAME_LIBRARY_FOLDER

        self.game_manager = GameManager(self.GAME_PATH)



    @staticmethod
    def create():
        if not KomorebiServer.instance:
            KomorebiServer.instance = KomorebiServer()
        return KomorebiServer.instance



server = KomorebiServer()
app = FastAPI()
# print(server.game_manager.list_games())


# @app.put("/login")
# def login():
#     return ""
# app = Flask(__name__)
# 
@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/list-games")
def list_game():
    games = server.game_manager.list_games()
    return {
        "games": [game.toJSON() for game in games]
    }
 
@app.get("/download/{id}")
def download(id: str, response: Response):
    print("Download")
    game = server.game_manager.get_game(id)
    if game is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {}
    else:
        zip_file = game.root / f"{game.config.name}.zip"
        if zip_file.exists() and zip_file.is_file():
            print(f"Zip file found at: {zip_file}")
            return FileResponse(path=zip_file)
        else:
            print("Making archive: ")
            zip_file = make_archive(game.root / game.config.name, "zip", game.root)
            print(f"Archive created: {zip_file}")
            return FileResponse(path=zip_file)








