import logging
from pathlib import Path
from os import getenv, wait
from dataclasses import dataclass
from logging import Logger
from utils.steam_api import SteamMetadata
from os import mkdir
from fastapi import FastAPI, Response, status
from fastapi.responses import FileResponse 
from shutil import make_archive
import tempfile
from game.game_manager import GameManager

from utils.utils import create_zip



# DEBUG = 1
# GAME_LIBRARY_FOLDER = Path(getenv("GAME_PATH"))

logger = logging.getLogger(__name__)

class KomorebiServer():
    instance: 'KomorebiServer | None'= None
    DEFAULT_GAME_PATH: Path
    DEFAULT_SAVE_PATH: Path
    def __init__(self) -> None:
        SERVER_ROOT = getenv("SEVER_ROOT")
        self.SERVER_ROOT = Path(SERVER_ROOT) if SERVER_ROOT else Path("~/.komorebi").expanduser()

        GAME_PATH = getenv("GAME_PATH")
        self.GAME_PATH = Path(GAME_PATH) if GAME_PATH else self.SERVER_ROOT / "games"

        SAVE_PATH = getenv("SAVE_PATH")
        self.SAVE_PATH = Path(SAVE_PATH) if SAVE_PATH else self.SERVER_ROOT / "saves"

        # if DEBUG:
        #     self.GAME_PATH = GAME_LIBRARY_FOLDER

        root = Path("~/.komorebi").expanduser()
        root.mkdir(exist_ok=True)
        (root / "games").mkdir(exist_ok=True)
        (root / "saves").mkdir(exist_ok=True)
        

        self.game_manager = GameManager(self.GAME_PATH)



    @staticmethod
    def create():
        if not KomorebiServer.instance:
            KomorebiServer.instance = KomorebiServer()
        return KomorebiServer.instance


from fastapi.middleware.cors import CORSMiddleware

server = KomorebiServer()
app = FastAPI()
# print(server.game_manager.list_games())



# origins = [
#     "http://localhost",
#     "http://localhost:8080",
#     "https://steamloopback.host"
# ]
# 
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_origin_regex=r"http://127.0.0.1:[0-9]*",
#     allow_methods=["*"],
#     allow_headers=["*"],
#     allow_credentials=True
# )


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
        "games": [game.create_steam_shortcut() for game in games]
    }
 
@app.get("/download/{id}")
def download(id: str, response: Response):
    print("Download")
    game = server.game_manager.get_game(id)
    if game is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return {}
    else:
        zip_file = game.game_folder / f"{game.name}.zip"
        if zip_file.exists() and zip_file.is_file():
            print(f"Zip file found at: {zip_file}")
            return FileResponse(path=zip_file)
        else:
            print("Making archive: ")
            # zip_file = make_archive(game.root / game.config.name, "zip", game.root)
            # but the zip file in the same game folder for now
            zip_file = create_zip(dest=game.game_folder / f"{game.name}.zip", folder_to_zip=game.game_folder)
            print(f"Archive created: {zip_file.as_posix()}")
            return FileResponse(path=zip_file.as_posix())


@app.get("/game/{id}/hero")
def get_hero(id: str, response: Response):
    game = server.game_manager.get_game(id)
    if game is None or game.assets is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return

    if not game.assets.hero_path.is_file():
        response.status_code = status.HTTP_204_NO_CONTENT
        return


    return FileResponse(game.assets.hero_path.as_posix())

@app.get("/game/{id}/capsule")
def get_capsule(id: str, response: Response):
    game = server.game_manager.get_game(id)
    if game is None or game.assets is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return

    if not game.assets.capsule_path.is_file():
        response.status_code = status.HTTP_204_NO_CONTENT
        return

    return FileResponse(game.assets.capsule_path.as_posix())

@app.get("/game/{id}/logo")
def get_logo(id: str, response: Response):
    game = server.game_manager.get_game(id)
    if game is None or game.assets is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return

    if not game.assets.logo_path.is_file():
        response.status_code = status.HTTP_204_NO_CONTENT
        return

    return FileResponse(game.assets.logo_path.as_posix())

@app.get("/game/{id}/icon")
def get_icon(id: str, response: Response):
    game = server.game_manager.get_game(id)
    if game is None or game.assets is None:
        response.status_code = status.HTTP_204_NO_CONTENT
        return

    if not game.assets.icon_path.is_file():
        response.status_code = status.HTTP_204_NO_CONTENT
        return

    return FileResponse(game.assets.icon_path.as_posix())



