from typing import Any, Dict, Literal, NewType, Optional
import requests 
from pathlib import Path
from dataclasses import dataclass
from steam.client import SteamClient
from pprint import pprint
import re
# from .steam_types import URL

URL = NewType("URL", str)

@dataclass
class GameID():
    app_id: int 
    name: str

@dataclass
class StoreResults():
    items: list[GameID]



@dataclass
class OSData():
    osarch: Optional[Literal["32", "64"]] = None
    oslist: Optional[Literal["windows"]] = None

@dataclass 
class LaunchOptions():
    executable: str
    type: Literal["default", "option1"] # whatever that means
    arguments: Optional[str] = None # launch_options
    description: Optional[str] = None
    workingdir: Optional[str] = None
    config: Optional[OSData] = None


@dataclass 
class ExecutableMetadata():
    installdir: str
    launch: list[LaunchOptions]
    depots: dict[Any, Any] #technically can be used to install dep


def make_launch_options(launch: Dict[str, Any]):
    config = launch.get("config")
    return LaunchOptions(
            launch["executable"],
            launch["type"],
            launch.get("arguments"),
            launch.get("description"),
            launch.get("workingdir"),
            OSData(config.get("osarch"), config.get("oslist")) if config else None
    )

def make_executable_metadata(product_info: Dict[str, Any]):
    config = product_info["config"]
    installdir = config["installdir"]
    launch = [make_launch_options(opt) for opt in config["launch"].values()]
    return ExecutableMetadata(installdir, launch, product_info["depots"])


#/search/results
#https://github.com/Revadike/InternalSteamWebAPI/wiki/Get-Search-Results

#/search/suggest
#https://github.com/Revadike/InternalSteamWebAPI/wiki/Get-Search-Suggestions

class SteamMetadata():
    #TODO: add rate limit
    #There's a limit to 300 store requests per 5 mins.
    INSTANCE: "SteamMetadata | None" = None
    ENDPOINT: str = "https://store.steampowered.com"
    client: SteamClient
    
    def __init__(self) -> None:
        print("SteamMetadata init")
        self.client = SteamClient()
        self.client.anonymous_login()

    @staticmethod
    def create():
        if SteamMetadata.INSTANCE is None:
            SteamMetadata.INSTANCE = SteamMetadata()
        return SteamMetadata.INSTANCE

    # def get_game_media(self, app_id: int) -> None:
    #     #TODO: error handling
    #     response = requests.get(
    #         f"{SteamMetadata.ENDPOINT}/api/appdetails",
    #         {
    #             "appids": app_id,
    #             "filters": "type,name,steam_appid,header_image,capsule_image,capsule_imagev5"
    #         }
    #     )
    #     return response.json()

    def store_search(self, term: str, cc="US", l="english"):
        #TODO: error handling
        # response = requests.get(
        #     f"{SteamMetadata.ENDPOINT}/storesearch",
        #     {
        #         "term": term,
        #         "cc": cc,
        #         "l": l
        #     }
        # )

        # response = requests.get(
        #     f"{SteamMetadata.ENDPOINT}/search/suggest",
        #     {
        #         "term": term,
        #         "cc": cc,
        #         "l": l,
        #         "realm": 1,
        #         # "origin": ""
        #         "f": "jsonfull",
        #         "require_type": "game"

        #     }
        # )

        response = requests.get(
            f"{SteamMetadata.ENDPOINT}/search/results",
            {
                "ignore_preference": 1,
                "category1": 998,
                "json": 1,
                "term": term
            }
        ).json()
        
        gameids = []
        for item in response["items"]:
            match = re.search(r"apps\/(?P<appid>\d*)\/", item["logo"])
            appid = match.group("appid")
            gameids.append(GameID(app_id=int(appid), name=item["name"]))

        return StoreResults(items=gameids)

    def get_game_configuration(self, appid: int):
        product_info: Any = self.client.get_product_info(apps=[appid])
        product_info = product_info["apps"][appid]
        return make_executable_metadata(product_info)


if __name__ == "__main__":
    from pprint import pprint
    s = SteamMetadata()
    pprint(s.store_search("Hades"))
         

