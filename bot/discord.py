import discord
from web3 import Web3
from discord.ext import commands
from utils.users import (get_address, get_user_balance, withdraw_to_address,
        tip_user)
from tokens.tokens import tokens
from decimal import Decimal

def run_discord_bot(discord_token, conn, w3):
    command_prefix = "$"
    description = "A Python Discord bot."
    bot = commands.Bot(command_prefix=command_prefix, description=description)

    @bot.command()
    async def ping(ctx: commands.Context):
        """Check if bot is online."""
        await ctx.send("pong")

    @bot.command()
    async def deposit(ctx, token: str):
        """
        Deposit tokens to your discord account.

        e.g. $deposit FTM
        """
        token = token.lower()
        if token not in tokens:
            #TODO: handle invalid token error
            return

        address = get_address(conn, ctx.author)
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
        """
        Withdraw tokens to an address.

        e.g. $withdraw FTM
        """
        token = token.lower()
        if token not in tokens:
            #TODO: handle invalid token error
            return

        def is_valid(msg):
            return msg.channel == ctx.channel and msg.author == ctx.author

        await ctx.send(f"Enter your {token.upper()} destination address.")
        address = await bot.wait_for("message", check=is_valid)

        if not Web3.isAddress(address.content):
            await ctx.send("You provided an invalid address.")
        else:
            balance = get_user_balance(conn, w3, ctx.author, token)
            await ctx.send(f"How much do you want to withdraw?\nYou currently have {balance} {token}")
            amount = await bot.wait_for("message", check=is_valid)
            _amount = Decimal(amount.content)
            if 0 < _amount <= balance:
                #TODO: Ok prompt to avoid withdrawals mistakes by users
                await ctx.send(f"You want to withdraw {_amount} {token.upper()} to {address.content}?\nReply with yes to confirm")
                confirmation = await bot.wait_for("message", check=is_valid)
                if confirmation.content.lower() == "yes":
                    txn_hash = withdraw_to_address(conn, w3, ctx.author, token, _amount, address.content)
                    await ctx.send(f"Withdrawing {_amount} {token.upper()} to {address.content}.\nTxn Hash: {txn_hash}")
                else:
                    #TODO cancel succesful message
                    pass
            else:
                await ctx.send(f"You can't withdraw {_amount} {token.upper()}.\nYou currently have {balance} {token.upper()}")

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
        amount = get_user_balance(conn, w3, ctx.author, token)
        await ctx.send(f"You have {amount} {token}.")

    @balance.error
    async def balance_error(ctx, error):
        #TODO: Implement balance error handler
        print(error)
        await ctx.send("A balance error occurred.")

    @bot.command()
    async def tip(ctx, receiver: discord.Member, amount: Decimal, token: str):
        """Send tokens to another user.

        e.g. $tip @user 5 FTM
        """
        token = token.lower()
        if token not in tokens:
            #TODO: handle invalid token error
            return

        balance = get_user_balance(conn, w3, ctx.author, token)
        if amount > balance:
            await ctx.send(f"Insufficient balance.")
        txn_hash = tip_user(conn, w3, ctx.author, receiver, amount, token)
        await ctx.send(f"You sent {amount} {token} to {receiver}.\nTxn Hash: {txn_hash}")

    @tip.error
    async def tip_error(ctx, error):
        #TODO: Implement tip error handler
        print(error)
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
