import logging
from config import get_config
from database.database import get_db
from utils.fantom import connect_to_fantom, get_balance_for_address

from bot.discord import run_discord_bot


logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def main():
    config = get_config()
    db = get_db(config['DATABASE_FILE'])
    fantom = connect_to_fantom(config["PROVIDER_ADDRESS"])
    bot = run_discord_bot(config['DISCORD_TOKEN'])

if __name__ == "__main__":
    main()
