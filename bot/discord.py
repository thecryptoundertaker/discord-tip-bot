from loguru import logger
from web3 import Web3
from typing import Optional
import discord
from discord.ext import commands
from utils.users import (get_address, get_user_balance, withdraw_to_address,
        tip_user)
from tokens.tokens import tokens
from utils.utils import round_down, to_lower, get_min_gas
from bot import errors, embeds
from bot.help import help_commands
from decimal import Decimal
from config import config

@logger.catch
def run_discord_bot(discord_token, conn, w3):
    command_prefix = "$"
    description = "Plutus, the Discord tipping bot."
    bot = commands.Bot(command_prefix=command_prefix,
                    description=description,
                    help_command=None)

    ###
    # Help commands
    ###

    help_commands(bot)

    ###
    # Tip bot commands
    ###

    @bot.command(name="tokens")
    async def _tokens(ctx):
        logger.debug("Executing $tokens command.")
        await ctx.send(embed=embeds.list_tokens(tokens))

    @bot.command()
    @commands.dm_only()
    async def deposit(ctx, device: Optional[str]):
        logger.debug("Executing $deposit command.")
        address = get_address(conn, ctx.author)
        if device == "mobile":
            await ctx.send(embed=embeds.deposit_address_mobile(address))
            await ctx.send(f"{address}")
        else:
            await ctx.send(embed=embeds.deposit_address(address))

    @bot.command()
    @commands.dm_only()
    async def withdraw(ctx, *, token: to_lower):
        logger.debug("Executing $withdraw command.")
        if token not in tokens:
            return await ctx.send(embed=errors.handle_invalid_token())

        balance = get_user_balance(conn, w3, ctx.author, token)
        if balance == 0:
            return await ctx.send(embed=errors.handle_no_funds(token))

        ftm_balance = get_user_balance(conn, w3, ctx.author, "ftm")
        min_gas = get_min_gas(w3)
        if ftm_balance < min_gas * 2: # enough gas for 2 transactions
            return await ctx.send(embed=errors.handle_not_enough_gas(min_gas*2))

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
            await ctx.send(embed=embeds.withdrawal_amount_prompt(balance, token))
            amount = await bot.wait_for("message", check=is_valid)
            if amount.content.lower() == "cancel":
                return await ctx.send(embed=embeds.withdrawal_cancelled())
            if amount.content.lower() == "all":
                _amount = Decimal(balance)
            else:
                try:
                    _amount = Decimal(amount.content)
                except:
                    return await ctx.send(embed=errors.handle_invalid_amount())

            if token == "ftm":
                _amount -= min_gas * 2 # To cover for gas fees
            fee = round_down(_amount * Decimal(config["FEE"]), 6)
            _amount -= fee
            if _amount < Decimal("1e-6"):
                return await ctx.send(embed=errors.handle_withdrawal_too_small())
            total = _amount + fee
            if token == "ftm":
                total += min_gas * 2
            if 0 < total <= balance:
                await ctx.send(embed=embeds.withdrawal_ok_prompt(_amount, token,
                            address, fee))
                confirmation = await bot.wait_for("message", check=is_valid)
                if confirmation.content.lower() in ["yes", "y", "confirm"]:
                    main_txn, fee_txn = withdraw_to_address(conn, w3,
                            ctx.author, token, _amount, address, fee)
                    if main_txn == None:
                        return await ctx.send(embed=errors.handle_unknown_error())
                    await ctx.send(embed=embeds.withdrawal_successful(_amount,
                        fee, token, address, main_txn, fee_txn))
                else:
                    await ctx.send(embed=embeds.withdrawal_cancelled())
            else:
                await ctx.send(embed=errors.handle_insufficient_balance(_amount,
                    token, balance))

    @bot.command()
    async def balance(ctx, *, token: to_lower):
        logger.debug("Executing $balance command.")
        if token not in tokens:
            return await ctx.send(embed=errors.handle_invalid_token())
        balance = get_user_balance(conn, w3, ctx.author, token)
        await ctx.send(embed=embeds.show_balance(ctx, balance, token))

    @bot.command()
    async def tip(ctx, receiver: discord.Member, amount: Decimal, *, token: to_lower):
        logger.debug("Executing $tip command.")
        if amount < Decimal("1e-6"):
            return await ctx.send(embed=errors.handle_tip_too_small())
        if token not in tokens:
            return await ctx.send(embed=errors.handle_invalid_token())

        balance = get_user_balance(conn, w3, ctx.author, token)
        if amount > balance:
            return await ctx.send(embed=errors.handle_insufficient_balance(
                amount, token, balance))
        min_gas = get_min_gas(w3)

        if token == "ftm":
            if amount + min_gas > balance:
                return await ctx.send(embed=errors.handle_not_enough_gas(min_gas))
        else:
            ftm_balance = get_user_balance(conn, w3, ctx.author, "ftm")
            if ftm_balance < min_gas:
                return await ctx.send(embed=errors.handle_not_enough_gas(min_gas))

        txn_hash = tip_user(conn, w3, ctx.author, receiver, amount, token)
        if not txn_hash:
            return await ctx.send(embed=errors.handle_unknown_error())
        await ctx.send(embed=embeds.tip_succesful(ctx.author, receiver, amount,
            token, txn_hash))

    ###
    # Command Errors
    ###

    @deposit.error
    async def deposit_error(ctx, error):
        logger.error("{}: {}", type(error).__name__, error)
        await ctx.send(embed=errors.handle_deposit(error))

    @withdraw.error
    async def withdraw_error(ctx, error):
        logger.error("{}: {}", type(error).__name__, error)
        await ctx.send(embed=errors.handle_withdrawal(error))

    @balance.error
    async def balance_error(ctx, error):
        logger.error("{}: {}", type(error).__name__, error)
        await ctx.send(embed=errors.handle_balance(error))

    @tip.error
    async def tip_error(ctx, error):
        logger.error("{}: {}", type(error).__name__, error)
        await ctx.send(embed=errors.handle_tipping(error))

    ###
    # Run Bot
    ###

    @bot.listen
    async def on_message(message):
        await bot.process_commands(message)

    @bot.event
    async def on_ready():
        logger.info("Bot {} is ready!", bot.user)

    bot.run(discord_token)
