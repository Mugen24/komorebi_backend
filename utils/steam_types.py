from typing import NewType
from dataclasses import dataclass
from pathlib import Path

URL = NewType("URL", str)

@dataclass
class Media:
    #TODO: return base64 encoded
    capsule: Path | None = None # 600px x 900px appear in the library collection overview
    hero: Path | None = None # 3840px x 1240px wide image grid in game detail page
    icon: Path | None = None
        
    def to_dict(self):
        return {
            "capsule": self.capsule.as_posix() if self.capsule else "", 
            "hero": self.hero.as_posix() if self.hero else "",
            "icon": self.icon.as_posix() if self.icon else "",
        }


#TODO: unifi type between plugin and server
@dataclass
class ServerAuth:
    ip: str
    port: int
