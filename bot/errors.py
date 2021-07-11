from discord.ext import commands
import discord

def handle_invalid_token():
    embed = discord.Embed(title="Command Error", color=0xE50000)
    embed.description = '''This token is not supported\n
                See `$tokens` for a list of supported tokens'''

    return embed

def handle_deposit(error):
    embed = discord.Embed(title="Command Error", color=0xE50000)
    if isinstance(error, commands.MissingRequiredArgument):
        embed.description = '''You need to include a token code (FTM, TOMB, \
                etc.)\n\ne.g. `$deposit FTM`'''
    else:
        embed.description = "Unknown error occurred"

    return embed
