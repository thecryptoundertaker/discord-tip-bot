from loguru import logger
import discord

###
# help
###

@logger.catch
def help():
    embed = discord.Embed(title="Help", color=0x117de1)
    embed.description = '''Plutus will take your money through the underworld \
and deliver it to any Discord user you want. See `$tokens` for a list of all \
supported tokens.'''
    embed.add_field(name="How to use Plutus",
                    value='''It's as simple as\n`$tip @user <amount> <token>`
For example:\n`$tip @hades 1 tomb`\n''', inline=False)
    embed.add_field(name="Commands",
                    value='''Here is a list of all the commands available:
```$balance\n$deposit\n$tip\n$tokens\n$withdraw```\n''', inline=False)
    embed.set_thumbnail(url=("https://cdn.discordapp.com/attachments/864163706970570762/871147388708999308/image0.png"))
    embed.set_footer(text='''For help with a specific command run `$help \
<command>`''')

    return embed

@logger.catch
def help_balance():
    embed = discord.Embed(title="Balance help", color=0x117de1)
    embed.description = "Check your token's balance."
    embed.add_field(name="Usage", value="`$balance <token>`", inline=False)
    embed.add_field(name="Example", value="`$balance ftm`", inline=False)
    embed.set_footer(text='See `$tokens` for a list of supported tokens')

    return embed

@logger.catch
def help_deposit():
    embed = discord.Embed(title="Deposit help", color=0x117de1)
    embed.description = '''Deposit tokens to your Discord user. Deposit \
**ONLY** supported tokens. See `$tokens` for the complete list.'''
    embed.add_field(name="Usage", value="`$deposit [device]`")
    embed.set_footer(text="See '$tokens' for a list of supported tokens")
    embed.set_footer(text='''Pro tip: Use `$deposit mobile` for easy \
copy-pasting on mobile''')
    
    return embed

@logger.catch
def help_tip():
    embed = discord.Embed(title="Tip help", color=0x117de1)
    embed.description = "Send tokens to another Discord user."
    embed.add_field(name="Usage", value="`$tip @user <amount> <token>`",
                    inline=False)
    embed.add_field(name="Example", value="`$tip @COMA 1 ftm`", inline=False)
    embed.set_footer(text='See `$tokens` for a list of supported tokens')

    return embed

@logger.catch
def help_withdraw():
    embed = discord.Embed(title="Withdraw help", color=0x117de1)
    embed.description = "Withdraw tokens to an address."
    embed.add_field(name="Usage", value="`$withdraw <token>`", inline=False)
    embed.add_field(name="Example", value="`$withdraw ftm`", inline=False)
    embed.set_footer(text='See `$tokens` for a list of supported tokens')

    return embed

@logger.catch
def help_tokens():
    embed = discord.Embed(title="Tokens help", color=0x117de1)
    embed.description = "Check the list of supported tokens."
    embed.add_field(name="Usage", value="`$tokens`", inline=False)

    return embed

###
# tokens
###

@logger.catch
def list_tokens(tokens):
    embed = discord.Embed(title="Tokens supported", color=0x117de1)
    embed.description = '\n'.join(
                        [f"**{tokens[token]['name']}** ({token.upper()})"
                        for token in tokens.keys()])
    return embed

###
# deposit
###

@logger.catch
def deposit_address(address):
    embed = discord.Embed(title=f"Deposit", color=0x00e500)
    embed.description = f'''This is your unique address that is associated \
with your discord user. Deposit your tokens to this address only.'''
    embed.add_field(name="Your deposit address",
            value=f"`{address}`")
    embed.set_footer(text='''Pro tip: Use "$deposit mobile" for easy \
copy-pasting on mobile''')
    return embed

@logger.catch
def deposit_address_mobile(address):
    embed = discord.Embed(title=f"Deposit", color=0x00e500)
    embed.description = f'''This is your unique address that is associated \
with your discord user. Deposit your tokens to this address only. Here \
is your address for easy copy pasting :arrow_down: :arrow_down: :arrow_down:'''
    return embed


###
# withdrawal
###

@logger.catch
def dst_address_prompt(token):
    token = token.upper()
    embed = discord.Embed(color=0x9a9b9c)
    embed.description = f"Enter your **{token}** destination address."
    embed.set_footer(text="Reply with cancel to cancel.")
    return embed

@logger.catch
def withdrawal_cancelled():
    embed = discord.Embed(color=0x9a9b9c)
    embed.description = "Withdrawal cancelled."
    return embed

@logger.catch
def withdrawal_amount_prompt(balance, token):
    token = token.upper()
    embed = discord.Embed(color=0x9a9b9c)
    embed.description = f'''How much **{token}** do you want to withdraw?
You currently have {float(balance):g} **{token}**
Reply with `all` to withdraw all'''
    embed.set_footer(text="Reply with cancel to cancel.")
    return embed

@logger.catch
def withdrawal_ok_prompt(amount, token, address, fee):
    token = token.upper()
    embed = discord.Embed(title=f"Confirm {token} withdrawal", color=0xf28804)
    embed.description = '''Please make sure everything is correct. This cannot \
be reversed.'''
    embed.add_field(name="Destination address", value=f"`{address}`",
            inline=False)
    embed.add_field(name="Withdrawal amount",
            value=f"**{float(amount):g} {token}**", inline=True)
    embed.add_field(name="Withdrawal fee", value=f"**{fee} {token}**",
            inline=True)
    embed.set_footer(text="Reply with yes to confirm or no to cancel")

    return embed

@logger.catch
def withdrawal_successful(amount, fee, token, address, main_txn, fee_txn):
    token = token.upper()
    embed = discord.Embed(title=f"{token} sent", color=0x00e500)
    embed.description = "Your withdrawal was processed succesfully!"
    embed.add_field(name="Destination address", value=f"`{address}`",
            inline=False)
    embed.add_field(name="Withdrawal amount",
            value=f"**{float(amount):g} {token}**", inline=True)
    embed.add_field(name="Withdrawal fee", value=f"**{fee} {token}**",
            inline=True)
    embed.add_field(name="Withdrawal Transaction ID",
            value=f"[{main_txn}](https://ftmscan.com/tx/{main_txn})",
            inline=False)
    if fee_txn:
        embed.add_field(name="Fee Transaction ID",
                value=f"[{fee_txn}](https://ftmscan.com/tx/{fee_txn})",
                inline=False)
    return embed

###
# balance
###

@logger.catch
def show_balance(ctx, balance, token):
    token = token.upper()
    embed = discord.Embed(title="Balance", color=0x117de1)
    embed.set_author(name=f"{ctx.author.display_name}'s Wallet",
            icon_url=ctx.author.avatar_url)
    embed.description = f"**{float(balance):g}** {token}"
    return embed

###
# tip
###

@logger.catch
def tip_succesful(sender, receiver, amount, token, txn_hash):
    token = token.upper()
    embed = discord.Embed(title="Generous!", color=0xFFD700)
    embed.description = f'''{sender.mention} sent {receiver.mention} \
{float(amount):g} {token}'''
    embed.add_field(name="Transaction ID",
            value=f"[{txn_hash}](https://ftmscan.com/tx/{txn_hash})")
    embed.set_footer(text='''Note: Sometimes it may take a bit for this tx to \
be reflected on the blockchain.''')

    return embed
