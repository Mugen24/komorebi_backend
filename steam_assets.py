from pathlib import Path
import requests
from utils.steam_api import GameInfo, SteamMetadata

class SteamAssets():
   def __init__(self, app_id: int, game_folder: Path, steam_config: GameInfo, auto_fetch_assets: bool = True):
      self.steam_info = steam_config
      self.app_id = app_id
      self.library_assets = steam_config["common"]["library_assets_full"]
      self.game_folder = game_folder

      self.icon_path = self.game_folder / "icon.ico"
      self.capsule_path = self.game_folder / "capsule.jpg"
      self.hero_path = self.game_folder / "hero.jpg"
      self.logo_path = self.game_folder / "logo.png"

      # try and fetch assets if needed
      if auto_fetch_assets:
         self.fetch_assets_if_needed()

   def get_icon_url(self):
      # iamge that gets overlayed onto the hero (bottom left)
      url = f"https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/{self.app_id}/{self.steam_info["common"]["clienticon"]}.ico"
      return url


   def get_capsule_url(self):
      # image that shows up in library overview
      # url = f"https://shared.steamstatic.com/store_item_assets/steam/apps/${self.app_id}/${self.library_assets["library_capsule"]["image"]["english"]}t=${meta.store_asset_mtime}"
      url = f"https://shared.steamstatic.com/store_item_assets/steam/apps/{self.app_id}/{self.library_assets["library_capsule"]["image"]["english"]}"
      return url

   # def get_library_wide_capsule(self):
   #    # we don't really need this
   #    url = f"https://shared.steamstatic.com/store_item_assets/steam/apps/${self.app_id}/${self.meta.header_image_full[lang]}?t=${meta.store_asset_mtime}"

   def get_hero_url(self):
      # image that shows up in game detail page
      url = f"https://shared.steamstatic.com/store_item_assets/steam/apps/{self.app_id}/{self.library_assets["library_hero"]["image"]["english"]}"
      return url

   def get_logo_url(self):
      url = f"https://shared.steamstatic.com/store_item_assets/steam/apps/{self.app_id}/{self.library_assets["library_logo"]["image"]["english"]}"
      return url

   def check_asset_exists(self, path: Path):
      if path.exists():
         print(f"{path} already exists skipping download")
         return True
      print(f"downloading {path.stem} to {path}")
      return False

   def download_icon(self):
      path = self.icon_path
      if self.check_asset_exists(path): return
      url = self.get_icon_url()
      resp = requests.get(url)
      with path.open("wb+") as fp:
         fp.write(resp.content)

   def download_capsule(self):
      path = self.capsule_path
      if self.check_asset_exists(path): return

      url = self.get_capsule_url()
      resp = requests.get(url)

      with path.open("wb+") as fp:
         fp.write(resp.content)

   def download_hero(self):
      path = self.hero_path
      if self.check_asset_exists(path): return

      url = self.get_hero_url()
      resp = requests.get(url)

      with path.open("wb+") as fp:
         fp.write(resp.content)

   def download_logo(self):
      # Yeah it's png for some reason
      path = self.logo_path
      if self.check_asset_exists(path): return

      url = self.get_logo_url()
      resp = requests.get(url)

      with path.open("wb+") as fp:
         fp.write(resp.content)


   def fetch_assets_if_needed(self):
      self.download_icon()
      self.download_capsule()
      self.download_hero()
      self.download_logo()

if __name__ == "__main__":
   cli = SteamMetadata.create()
   app_id = 1145360
   config = cli.get_game_configuration(app_id)
   s = SteamAssets(app_id, Path("."), config)
   print(s.get_hero_url())

