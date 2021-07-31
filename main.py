from loguru import logger
from config import config
from database.database import get_db
from utils.fantom import connect_to_fantom

from bot.discord import run_discord_bot

logger.add("logs/{time:YYYY-MM-DD}.log", level=config["LOG_LEVEL"], rotation="100 MB")

@logger.catch
def main():
    conn = get_db(config['DATABASE_FILE'])
    w3 = connect_to_fantom(config["PROVIDER_ADDRESS"])
    bot = run_discord_bot(config["DISCORD_TOKEN"], conn, w3)

if __name__ == "__main__":
    main()
