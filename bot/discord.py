import discord
from web3 import Web3
from discord.ext import commands
from utils.users import (get_address, get_user_balance, withdraw_to_address,
        tip_user)
from tokens.tokens import tokens
from bot import errors
from bot import embeds
from decimal import Decimal

def run_discord_bot(discord_token, conn, w3):
    command_prefix = "$"
    description = "A Python Discord bot."
    bot = commands.Bot(command_prefix=command_prefix, description=description)

    def to_lower(arg):
        return arg.lower()

    @bot.command()
    async def ping(ctx):
        """Check if bot is online."""
        await ctx.send("pong")

    @bot.command(name="tokens")
    async def _tokens(ctx):
        """Check the list of supported tokens"""
        await ctx.send(embed=embeds.list_tokens(tokens))

    @bot.command()
    async def deposit(ctx, *, token: to_lower):
        """
        Deposit tokens to your discord account.

        e.g. $deposit FTM
        """
        if token not in tokens:
            await ctx.send(embed=errors.handle_invalid_token())
            return

        address = get_address(conn, ctx.author)
        await ctx.send(embed=embeds.deposit_address(token, address))

    @deposit.error
    async def deposit_error(ctx, error):
        await ctx.send(embed=errors.handle_deposit(error))

    @bot.command()
    async def withdraw(ctx, token: to_lower):
        """
        Withdraw tokens to an address.

        e.g. $withdraw FTM
        """
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
        print(error, type(error))
        await ctx.send(f"Error: {error}")

    @bot.command()
    async def balance(ctx, token: to_lower):
        """Check your token's balance.

        e.g. $balance FTM
        """
        if token not in tokens:
            #TODO: handle invalid token error
            return
        amount = get_user_balance(conn, w3, ctx.author, token)
        await ctx.send(f"You have {amount} {token}.")

    @balance.error
    async def balance_error(ctx, error):
        #TODO: Implement balance error handler
        print(error, type(error))
        await ctx.send(f"Error: {error}")

    @bot.command()
    async def tip(ctx, receiver: discord.Member, amount: Decimal, token: to_lower):
        """Send tokens to another user.

        e.g. $tip @user 5 FTM
        """
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
        print(error, type(error))
        await ctx.send(f"Error: {error}")


    @bot.listen
    async def on_message(message):
        if "help" in message.content.lower():
            await message.channel.send("<Help message here>")
            await bot.process_commands(message)

    @bot.event
    async def on_ready():
        print(f"Bot {bot.user} is ready!")

    bot.run(discord_token)
