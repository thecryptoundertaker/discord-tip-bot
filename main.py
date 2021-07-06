from config import config
from utils.fantom import connect_to_fantom
<<<<<<< HEAD

from db.utils import get_db
from bot.discord import get_discord_bot
=======
from bot.discord import run_discord_bot
from database.database import init_db

from utils.fantom import get_balance_for_address
>>>>>>> a63d27ee4274d7465bfa9c02451584c3b268b911

import logging

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def main():
    config = get_config()
    logging.info('Tip Bot Started')
    db = get_db(config['DATABASE_FILE'])
    fantom = connect_to_fantom(config["PROVIDER_ADDRESS"])
    bot = get_discord_bot(config)
    bot.run(config["DISCORD_TOKEN"])
    fantom = connect_to_fantom(config["PROVIDER_ADDRESS"])
    return 

if __name__ == "__main__":
    main()
