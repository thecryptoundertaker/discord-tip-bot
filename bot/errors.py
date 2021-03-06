from loguru import logger
from discord.ext import commands
import discord


@logger.catch
def handle_not_admin():
    embed = discord.Embed(title="Command Error", color=0xE50000)
    embed.description = '''Only admins can run this command. Please contact \
**@0xKalakaua**.'''

    return embed

@logger.catch
def handle_unknown_error():
    embed = discord.Embed(title="Unknown Error", color=0xE50000)
    embed.description = '''An unknown error occurred. Please try again. If \
this error persists please contact **@0xKalakaua**.'''

    return embed

@logger.catch
def handle_invalid_token():
    embed = discord.Embed(title="Command Error", color=0xE50000)
    embed.description = '''This token is not supported\n
See `$tokens` for a list of supported tokens'''

    return embed

@logger.catch
def handle_deposit(error):
    embed = discord.Embed(title="Command Error", color=0xE50000)
    if isinstance(error, commands.PrivateMessageOnly):
        embed.description = "This command can only be used in DM."
    else:
        embed.description = "Unknown error occurred. Try again."

    return embed

@logger.catch
def handle_invalid_address():
    embed = discord.Embed(title="Invalid Address", color=0xE50000)
    embed.description = "The address you provided is invalid."
    return embed

@logger.catch
def handle_insufficient_balance(amount, token, balance):
    token = token.upper()
    embed = discord.Embed(title="Insufficient Balance", color=0xE50000)
    embed.add_field(name="Your balance", value=f"**{float(balance):g} {token}**")

    return embed

@logger.catch
def handle_no_funds(token):
    token = token.upper()
    embed = discord.Embed(title="Insufficient Balance", color=0xE50000)
    embed.description = f'''You don't have any **{token}**. Please deposit \
some using the `$deposit` command.'''

    return embed

@logger.catch
def handle_not_enough_gas(min_gas):
    embed = discord.Embed(title="Not enough gas", color=0xE50000)
    embed.description = f'''You don't have enough **FTM** to cover gas fees. \
You need at least {min_gas} FTM. Please deposit some using the \
`$deposit` command.'''

    return embed

@logger.catch
def handle_tip_too_small():
    embed = discord.Embed(title="Tip too small", color=0xE50000)
    embed.description = '''The amount you are trying to tip is too small. Come \
on, you can do better.'''

    return embed

@logger.catch
def handle_withdrawal_too_small():
    embed = discord.Embed(title="Withdrawal too small", color=0xE50000)
    embed.description = '''The amount you are trying to withdraw is too small. \
the mininum is 1e-6.'''

    return embed

@logger.catch
def handle_invalid_amount():
    embed = discord.Embed(title="Invalid amount", color=0xE50000)
    embed.description = "This amount is invalid. Please start again."

    return embed

@logger.catch
def handle_withdrawal(error):
    embed = discord.Embed(title="Command Error", color=0xE50000)
    if isinstance(error, commands.MissingRequiredArgument):
        embed.description = '''You need to include a token code (FTM, TOMB, \
etc.)\n\ne.g. `$withdraw FTM`'''
    elif isinstance(error, commands.PrivateMessageOnly):
        embed.description = "This command can only be used in DM."
    else:
        embed.description = "Unknown error occurred. Try again."

    return embed

@logger.catch
def handle_balance(error):
    embed = discord.Embed(title="Command Error", color=0xE50000)
    if isinstance(error, commands.MissingRequiredArgument):
        embed.description = '''You need to include a token code (FTM, TOMB, \
etc.)\n\ne.g. `$balance FTM`'''
    else:
        embed.description = "Unknown error occurred. Try again."

    return embed

@logger.catch
def handle_tipping(error):
    embed = discord.Embed(title="Command Error", color=0xE50000)
    if isinstance(error, commands.MissingRequiredArgument):
        embed.description = '''Usage: `$tip @user <amount> <token>`\
\n\ne.g. `$tip @0xKalakaua 1 FTM`'''
    elif isinstance(error, commands.MemberNotFound):
        embed.description = str(error)
    else:
        embed.description = "Unknown error occurred. Try again."

    return embed
