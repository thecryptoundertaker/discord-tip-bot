from utils.fantom import connect_to_fantom
from config import config
from discord.ext import commands
import logging

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

fantom = connect_to_fantom(config["PROVIDER_ADDRESS"])
print(f"* Connected to Fantom!")
print(f"* Node Address: {config['PROVIDER_ADDRESS']}")
print(f"* Provider Type: {config['PROVIDER_TYPE']}")
print(f"* Current Block: {fantom.eth.block_number}")

bot = commands.Bot(command_prefix="$")

@bot.event
async def on_message(message):
    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready!")

bot.run(config["TOKEN"])
