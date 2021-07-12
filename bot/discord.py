import discord
from web3 import Web3
from discord.ext import commands
from utils.users import (get_address, get_user_balance, withdraw_to_address,
        tip_user)
from tokens.tokens import tokens
from bot import errors
from bot import embeds
from decimal import Decimal

#TODO add logging in all error functions
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
        print(error, type(error))
        await ctx.send(embed=errors.handle_deposit(error))

    @bot.command()
    async def withdraw(ctx, *, token: to_lower):
        """
        Withdraw tokens to an address.

        e.g. $withdraw FTM
        """
        if token not in tokens:
            await ctx.send(embed=errors.handle_invalid_token())
            return

        balance = get_user_balance(conn, w3, ctx.author, token)
        if balance == 0:
            await ctx.send(embed=errors.handle_no_funds(token))
            return

        def is_valid(msg):
            return msg.channel == ctx.channel and msg.author == ctx.author

        await ctx.send(embed=embeds.dst_address_prompt(token))
        address = await bot.wait_for("message", check=is_valid)
        address = address.content

        if address == "cancel":
            await ctx.send(embed=embeds.withdrawal_cancelled())
        elif not Web3.isAddress(address):
            await ctx.send(embed=errors.handle_invalid_address())
        else:
            balance = get_user_balance(conn, w3, ctx.author, token)
            await ctx.send(embed=embeds.withdrawal_amount_prompt(balance, token))
            amount = await bot.wait_for("message", check=is_valid)
            if amount.content == "cancel":
                await ctx.send(embed=embeds.withdrawal_cancelled())
                return
            if amount.content == "all":
                _amount = Decimal(balance)
                if token == "ftm":
                    _amount -= Decimal(0.0048) # To cover for gas fees
            else:
                _amount = Decimal(amount.content)
            if 0 < _amount <= balance:
                await ctx.send(embed=embeds.withdrawal_ok_prompt(_amount, token,
                    address))
                confirmation = await bot.wait_for("message", check=is_valid)
                if confirmation.content.lower() in ["yes", "y", "confirm"]:
                    txn_hash = withdraw_to_address(conn, w3, ctx.author, token, _amount, address)
                    await ctx.send(embed=embeds.withdrawal_successful(_amount,
                        token, address, txn_hash))
                else:
                    await ctx.send(embed=embeds.withdrawal_cancelled())
            else:
                await ctx.send(embed=errors.handle_insufficient_balance(_amount,
                    token, balance))

    @withdraw.error
    async def withdraw_error(ctx, error):
        print(error, type(error))
        await ctx.send(embed=errors.handle_withdrawal(error))

    @bot.command()
    async def balance(ctx, *, token: to_lower):
        """Check your token's balance.

        e.g. $balance FTM
        """
        if token not in tokens:
            await ctx.send(embed=errors.handle_invalid_token())
            return
        balance = get_user_balance(conn, w3, ctx.author, token)
        await ctx.send(embed=embeds.show_balance(ctx, balance, token))

    @balance.error
    async def balance_error(ctx, error):
        print(error, type(error))
        await ctx.send(embed=errors.handle_balance(error))

    @bot.command()
    async def tip(ctx, receiver: discord.Member, amount: Decimal, *, token: to_lower):
        """Send tokens to another user.

        e.g. $tip @user 5 FTM
        """
        if token not in tokens:
            await ctx.send(embed=errors.handle_invalid_token())
            return

        balance = get_user_balance(conn, w3, ctx.author, token)
        if amount > balance:
            await ctx.send(embed=errors.handle_insufficient_balance(amount,
                token, balance))
            return

        txn_hash = tip_user(conn, w3, ctx.author, receiver, amount, token)
        await ctx.send(embed=embeds.tip_succesful(ctx.author, receiver, amount,
            token, txn_hash))

    @tip.error
    async def tip_error(ctx, error):
        print(error, type(error))
        await ctx.send(embed=errors.handle_tipping(error))


    @bot.listen
    async def on_message(message):
        if "help" in message.content.lower():
            await message.channel.send("<Help message here>")
            await bot.process_commands(message)

    @bot.event
    async def on_ready():
        print(f"Bot {bot.user} is ready!")

    bot.run(discord_token)
