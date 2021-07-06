import discord
from web3 import Web3
from discord.ext import commands
from utils.fantom import connect_to_fantom, get_address, get_balance_for_address, withdraw_to_address
from tokens.tokens import tokens
from decimal import Decimal

def run_discord_bot(discord_token):
    command_prefix = "$"
    description = "A Python Discord bot."
    bot = commands.Bot(command_prefix=command_prefix, description=description)

    @bot.command()
    async def ping(ctx: commands.Context):
        """Check if bot is online."""
        await ctx.send("pong")

    @bot.command()
    async def deposit(ctx, token: str):
        """Deposit tokens to your discord account.

        e.g. $deposit FTM
        """
        token = token.lower()
        if token not in tokens:
            #TODO: handle invalid token error
            return
        #TODO: Check if token is valid

        address = get_address(ctx.author)
        await ctx.send(f"Deposit {token.upper()} to this address => {address}")


    @deposit.error
    async def deposit_error(ctx, error):
        #TODO: Implement deposit error handler
        if isinstance(error, commands.BadArgument):
            await ctx.send("[BadArgument] A deposit error occurred.")
        else:
            print(error)
            await ctx.send("[Other] A deposit error occurred.")

    @bot.command()
    async def withdraw(ctx, token: str):
        """Send tokens to an address.

        e.g. $withdraw FTM
        """
        token = token.lower()
        if token not in tokens:
            #TODO: handle invalid token error
            return

        def is_valid(msg):
            return msg.channel == ctx.channel and msg.author == ctx.author

        await ctx.send(f"Enter your {token} destination address.")
        address = await bot.wait_for("message", check=is_valid)

        if not Web3.isAddress(address.content):
            await ctx.send("You provided an invalid address.")
        else:
            balance = get_balance(ctx.author, token)
            await ctx.send(f"How much do you want to withdraw?\nYou currently have {balance} {token}")
            amount = await bot.wait_for("message", check=is_valid)
            _amount = Decimal(amount.content)
            if 0 < _amount <= balance:
                #TODO: Ok prompt to avoid withdrawals mistakes by users
                txn_hash = withdraw_to_address(ctx.author, token, _amount, address.content)
                await ctx.send(f"Withdrawing {_amount} {token} to {address.content}.\nTxn Hash: {txn_hash}")
            else:
                await ctx.send(f"You can't withdraw {_amount} {token}.\nYou currently have {balance} {token}")

    @withdraw.error
    async def withdraw_error(ctx, error):
        #TODO: Implement withdraw error handler
        print(error)
        await ctx.send("A withdrawal error occurred.")

    @bot.command()
    async def balance(ctx, token: str):
        """Check your token's balance.

        e.g. $balance FTM
        """
        token = token.lower()
        if token not in tokens:
            #TODO: handle invalid token error
            return
        amount = get_balance(ctx.author, token)
        await ctx.send(f"You have {amount} {token}.")

    @balance.error
    async def balance_error(ctx, error):
        #TODO: Implement balance error handler
        print(error)
        await ctx.send("A balance error occurred.")

    @bot.command()
    async def tip(ctx, user: discord.Member, amount: Decimal, token: str):
        """Send tokens to another user.

        e.g. $tip @user 5 FTM
        """
        token = token.lower()
        if token not in tokens:
            #TODO: handle invalid token error
            return

        balance = get_balance(ctx.author, token)
        if amount > balance:
            await ctx.send(f"Insufficient balance.")
        #TODO: Implement _tip(sender, receiver, token, amount) function
        await ctx.send(f"You sent {amount} {token} to {user}.")

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

    bot.run(discord_token)
