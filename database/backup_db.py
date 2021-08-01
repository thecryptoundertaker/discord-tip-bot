from loguru import logger
import time
import os
import subprocess

@logger.catch(level="CRITICAL")
def backup(db_file):
    if not os.path.isdir("backups"):
        os.makedirs("backups")
    logger.info("Backing up {} database", db_file)
    subprocess.run(["sqlite3", db_file,
                    f".backup 'backups/backup_{int(time.time())}_{db_file}'"])


@logger.catch(level="CRITICAL")
def backup_periodically(db_file, interval=86400):
    logger.info("Periodic backup started. Backing {} every {} seconds.",
                db_file, interval)
    while 1:
        backup(db_file)
        time.sleep(interval)
