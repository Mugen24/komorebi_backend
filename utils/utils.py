from collections import deque
from pathlib import Path
from os import getenv


# def bfs_find_file(file_target: str, source_folder: Path, depth = 1):
#     if depth < 0:
#         return None
# 
#     if source_folder.is_dir():
#         q = [file for file in source_folder.iterdir()]
#     else:
#         return None
# 
#     for file in q:
#         if file.name == file_target: 
#             return file
# 
#     for file in q:
#         found_path = bfs_find_file(file_target, file, depth=depth - 1)
#         if found_path is not None: 
#             return found_path

def find_file(file_target: str, source_folder: Path):
    for file in source_folder.glob(f"**/{file_target}"):
        print(file)


if __name__ == "__main__":
    source = Path(getenv("GAME_PATH")) / "Hades"
    find_file("x64/Hades.exe", source)
    


