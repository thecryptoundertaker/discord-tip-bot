import logging
from config import get_config
from database.database import get_db
from utils.fantom import connect_to_fantom

from bot.discord import run_discord_bot


logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="local/bot.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def main():
    config = get_config()
    conn = get_db(config['DATABASE_FILE'])
    w3 = connect_to_fantom(config["PROVIDER_ADDRESS"])
    bot = run_discord_bot(config["DISCORD_TOKEN"], conn, w3)

if __name__ == "__main__":
    main()
