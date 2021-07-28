from loguru import logger
from bot import embeds


@logger.catch
def help_commands(bot):

    @bot.group(invoke_without_command=True)
    async def help(ctx):
        await ctx.send(embed=embeds.help())

    @help.command()
    async def balance(ctx):
        await ctx.send(embed=embeds.help_balance())

    @help.command()
    async def deposit(ctx):
        await ctx.send(embed=embeds.help_deposit())

    @help.command()
    async def tip(ctx):
        await ctx.send(embed=embeds.help_tip())

    @help.command()
    async def withdraw(ctx):
        await ctx.send(embed=embeds.help_withdraw())

    @help.command(name="tokens")
    async def _tokens(ctx):
        await ctx.send(embed=embeds.help_tokens())
