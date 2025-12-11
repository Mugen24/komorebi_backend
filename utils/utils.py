from collections import deque
from pathlib import Path
from os import getenv
import zipfile
from urllib import request
from os import chdir

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

    with zipfile.ZipFile(dest, "w") as fp:
        print(f"zipping: {folder_to_zip}")
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


if __name__ == "__main__":
    pass
    


