from discord.ext import commands

class TipBot(commands.Bot):
    def __init__(self, config):
        super().__init__(command_prefix="$")
        self.token = config["TOKEN"]

    async def on_ready(self):
        print(f"Bot {self.user} is ready!")

    async def on_message(self, message):
        if message.content.startswith("$hello"):
            await message.channel.send("Hello!")

    def exec(self):
        self.run(self.token)
