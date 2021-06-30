from utils.fantom import connect_to_fantom
from config import config
import discord
from discord.ext import commands
import logging

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="bot.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

fantom = connect_to_fantom(config["PROVIDER_ADDRESS"])
print(f"* Connected to Fantom!")
print(f"* Node Address: {config['PROVIDER_ADDRESS']}")
print(f"* Provider Type: {config['PROVIDER_TYPE']}")
print(f"* Current Block: {fantom.eth.block_number}")

bot = commands.Bot(command_prefix="$")

@bot.command()
async def ping(ctx: commands.Context):
    """Check if bot is online."""
    await ctx.send("pong")

# ebot.command()
# async def help(ctx):
    # await ctx.send("<Help message here>")

@bot.command()
# async def deposit(ctx, amount: float, coin: str, address: str):
async def deposit(ctx, coin: str):
    """Deposit coins to your discord account.

    e.g. $deposit FTM
    """
    #TODO: Check if coin is valid


    #TODO: Implement get_address() function
    #TODO: Associate the address to the discord user in question
    address = "<VALID ADDRESS>"
    await ctx.send(f"Deposit {coin.upper()} to this address => {address}")


@deposit.error
async def deposit_error(ctx, error):
    #TODO: Implement deposit error handler
    if isinstance(error, commands.BadArgument):
        await ctx.send("[BadArgument] A deposit error occurred.")
    else:
        print(error)
        await ctx.send("[Other] A deposit error occurred.")

@bot.command()
# async def withdraw(ctx, amount: float, coin: str, address: str):
async def withdraw(ctx, coin: str):
    """Send coins to an address.

    e.g. $withdraw FTM
    """
    #TODO: Implement withdraw function

    def is_valid(msg):
        return msg.channel == ctx.channel and msg.author == ctx.author

    await ctx.send(f"Enter your {coin} destination address.")
    address = await bot.wait_for("message", check=is_valid)

    #TODO: Check if adress is valid
    if address.content == "invalid":
        await ctx.send("You provided an invalid address.")
    else:
        balance = 100 #TODO: Get user's balance (same function used in $balance command)
        await ctx.send(f"How much do you want to withdraw?\nYou currently have {balance} {coin}")
        amount = await bot.wait_for("message", check=is_valid)
        _amount = float(amount.content)
        if 0 < _amount <= balance:
            #TODO: Ok prompt to avoid withdrawals mistakes by users
            #TODO: Implement withdraw(user, coin, balance, address) function
            await ctx.send(f"Withdrawing {_amount} {coin} to {address.content}")
        else:
            await ctx.send(f"You can't withdraw {_amount} {coin}.\nYou currently have {balance} {coin}")

@withdraw.error
async def withdraw_error(ctx, error):
    #TODO: Implement withdraw error handler
    await ctx.send("A withdrawal error occurred.")

@bot.command()
async def balance(ctx, coin: str):
    """Check your coin's balance.

    e.g. $balance FTM
    """
    amount = 100 #TODO: Implement get_balance(user, coin)
    await ctx.send(f"You have {amount} {coin}.")

@balance.error
async def balance_error(ctx, error):
    #TODO: Implement balance error handler
    await ctx.send("A balance error occurred.")

@bot.command()
async def tip(ctx, user: discord.Member, amount: float, coin: str):
    """Send coins to another user.

    e.g. $tip @user 5 FTM
    """
    balance = 100 #TODO: get_balance function from above
    if amount > balance:
        await ctx.send(f"Insufficient balance.")
    #TODO: Implement _tip(sender, receiver, coin, amount) function
    await ctx.send(f"You sent {amount} {coin} to {user}.")

@tip.error
async def tip_error(ctx, error):
    #TODO: Implement tip error handler
    await ctx.send("A tip error occurred.")


@bot.listen
async def on_message(message):
    if "help" in message.content.lower():
        await message.channel.send("<Help message here>")
        await bot.process_commands(message)

@bot.event
async def on_ready():
    print(f"Bot {bot.user} is ready!")

bot.run(config["TOKEN"])
