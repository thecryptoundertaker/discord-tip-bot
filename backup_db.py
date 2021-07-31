from config import config
import time
import os
import subprocess

if not os.path.isdir("backups"):
    os.makedirs("backups")
subprocess.run(["sqlite3", config["DATABASE_FILE"],
    f".backup 'backups/backup_{int(time.time())}_{config['DATABASE_FILE']}'"])
