from collections import deque
from pathlib import Path
from os import getenv
import zipfile
from urllib import request
from os import chdir
from utils.steam_api import LaunchOptions

def find_file(file_target: str, source_folder: Path):
    for file in source_folder.glob(f"**/{file_target}"):
        print(file)

def _recursive_zip(fp, path, root_folder):

    for f in path.iterdir():
        if f.suffix == ".zip":
            continue

        print(f"zipping: {f}")
        # cannot see f relative to root unless cwd is in root
        fp.write(f.relative_to(root_folder))

        if f.is_dir():
            _recursive_zip(fp,f, root_folder)

def create_zip(dest: Path, folder_to_zip: Path):
    # needed to keep the directory context relative to the root folder
    chdir(folder_to_zip)
    print(f"zipping: {folder_to_zip}")

    with zipfile.ZipFile(dest, "w") as fp:
        _recursive_zip(fp, path=folder_to_zip, root_folder=folder_to_zip)

    return dest


def download():
    url = "http://127.0.0.1:8000/download/308836784772523141175612368748750693433"
    r = request.Request(url, headers={
        "Content-Type": "application/zip",
        "Connection": "keep-alive",
    })

    resp = request.urlopen(r)
    chunk_size = 10 * 1024

    with open("SIGNALIS3.zip", "wb") as fp:
        while chunk := resp.read(chunk_size):
            fp.write(chunk)



def locate_launch_config(game_folder: Path, launch_option: LaunchOptions):
    print(f"Locating launchoption: {launch_option} in {game_folder}")
    # get the the default launch config
    # pprint(game_config["config"])

    arguments = launch_option.get("arguments")

    # replace window \ with linux /
    executable_name = launch_option["executable"].replace("\\", "/")

    try:
        # search for executable_name in file
        # executable_name can be a path ex. x86/hades.exe
        #TODO: try out all different launch_config if fails
        executable_path = [file for file in game_folder.glob(f"**/{executable_name}")][0]

    except IndexError as e:
        print(f"Cannot find executable {executable_name}")
        print(e)
        return


    # use workingdir from steam 
    # if not default to the parent folder of exe
    try: 
        working_dir = launch_option.get("workingdir", "")
        working_dir = working_dir.replace("\\", "/")
        working_dir = [dir for dir in game_folder.glob(f"**/{working_dir}")][0]
        print(f"Working dir found {working_dir}")
    except:
        working_dir = executable_path.parent
        print(f"Working dir not found fall back to {working_dir}")

    working_dir = Path(working_dir.relative_to(game_folder))
    executable_path = Path(executable_path.relative_to(game_folder))

    return {
            "working_dir": working_dir,
            "executable_path": executable_path,
            "arguments": arguments,
    }

