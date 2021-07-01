from config import get_config
from utils.fantom import connect_to_fantom
from bot.discord import get_discord_bot

import logging

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def main():
    breakpoint()
    config = get_config()
    fantom = connect_to_fantom(config["PROVIDER_ADDRESS"])
    bot = get_discord_bot()
    bot.run(config["TOKEN"])
    return 

if __name__ == "__main__":
    main()
