import json
from os import name
from pathlib import Path

class Config():
    def __init__(self, game_folder: Path) -> None:
        self.config_folder = game_folder / "config.json"

    def load(self):
        if self.config_folder.exists() and self.config_folder.is_file():
            print(f"config.json found for {self.config_folder.parent}")
            config = json.loads(self.config_folder.read_text())

            # self.size = config["size"]
            self.working_dir = Path(config["working_dir"]) if config["working_dir"] else None
            self.executable_path = Path(config["executable_path"]) if config["executable_path"] else None
            self.app_id = config["app_id"]
            self.name = config["name"]
            self.arguments = config["arguments"]
            self.id = config["id"]
            return True

        return False

    def write(self):
        config = {
            # "size": self.size,
            "working_dir": self.working_dir.as_posix() if self.working_dir else None,
            "executable_path": self.executable_path.as_posix() if self.executable_path else None,
            "app_id": self.app_id,
            "name": self.name,
            "arguments": self.arguments,
            "id": self.id
        }

        #TODO: add this in after testing
        if self.config_folder.exists():
            print(f"Config already exists")
            pass

        self.config_folder.touch()
        self.config_folder.write_text(json.dumps(config))



