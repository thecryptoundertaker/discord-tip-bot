import discord

###
# tokens
###
def list_tokens(tokens):
    embed = discord.Embed(title="Tokens supported", color=0x117de1)
    embed.description = '\n'.join(
                        [f"**{tokens[token]['name']}** ({token.upper()})"
                        for token in tokens.keys()])
    return embed

###
# deposit
###

def deposit_address(token, address):
    token = token.upper()
    embed = discord.Embed(title=f"Deposit {token}", color=0x00e500)
    embed.description = f'''This is your unique address that is associated with \
            your discord user. Deposit {token} to this address only.'''
    embed.add_field(name="Your deposit address", value=f"`{address}`")
    return embed

###
# withdrawal
###

def dst_address_prompt(token):
    token = token.upper()
    embed = discord.Embed(color=0x9a9b9c)
    embed.description = f"Enter your **{token}** destination address."
    embed.set_footer(text="Reply with cancel to cancel.")
    return embed

def withdrawal_cancelled():
    embed = discord.Embed(color=0x9a9b9c)
    embed.description = "Withdrawal cancelled."
    return embed

def withdrawal_amount_prompt(balance, token):
    token = token.upper()
    embed = discord.Embed(color=0x9a9b9c)
    embed.description = f'''How much **{token}** do you want to withdraw?
            You currently have {balance} **{token}**
            Reply with `all` to withdraw all'''
    embed.set_footer(text="Reply with cancel to cancel.")
    return embed

def withdrawal_ok_prompt(amount, token, address):
    token = token.upper()
    embed = discord.Embed(title=f"Confirm {token} withdrawal", color=0xf28804)
    embed.description = '''Please make sure everything is correct. This cannot \
            be reversed.'''
    embed.add_field(name="Destination address", value=f"`{address}`",
            inline=False)
    embed.add_field(name="Withdrawal amount", value=f"**{amount} {token}**",
            inline=False)
    embed.set_footer(text="Reply with yes to confirm or no to cancel")

    return embed

def withdrawal_successful(amount, token, address, txn_hash):
    token = token.upper()
    embed = discord.Embed(title=f"{token} sent", color=0x00e500)
    embed.description = "Your withdrawal was processed succesfully!"
    embed.add_field(name="Destination address", value=f"`{address}`",
            inline=False)
    embed.add_field(name="Withdrawal amount", value=f"**{amount} {token}**",
            inline=False)
    embed.add_field(name="Transaction ID",
            value=f"[{txn_hash}](https://ftmscan.com/tx/{txn_hash})",
            inline=False)
    return embed

###
# balance
###

def show_balance(ctx, balance, token):
    token = token.upper()
    embed = discord.Embed(title="Balance", color=0x117de1)
    embed.set_author(name=f"{ctx.author.display_name}'s Wallet",
            icon_url=ctx.author.avatar_url)
    embed.description = f"**{balance}** {token}"
    return embed

###
# tip
###

def tip_succesful(sender, receiver, amount, token, txn_hash):
    token = token.upper()
    embed = discord.Embed(title="Generous!", color=0xFFD700)
    embed.description = f'''{sender.mention} sent {receiver.mention} {amount} \
            {token}'''
    embed.add_field(name="Transaction ID",
            value=f"[{txn_hash}](https://ftmscan.com/tx/{txn_hash})")

    return embed
