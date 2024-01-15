import os
import git
from datetime import datetime

folder_path = "/home/ferit/shoka/400-499 vault"

if not os.path.exists(os.path.join(folder_path, ".git")):
    repo = git.Repo.init(folder_path)
else:
    repo = git.Repo(folder_path)

os.chdir(folder_path)

repo.remotes.origin.pull()
repo.index.add("*")

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
repo.index.commit(f"{timestamp} ewdows usual")

repo.remote("origin").push()

