import discord

###
# help
###

def help():
    embed = discord.Embed(title="Help", color=0x117de1)
    embed.description = '''Charon is a bot that allows you to tip other \
Discord users in many different tokens. See `$tokens` for a list of all \
supported tokens.'''
    embed.add_field(name="How to use Charon",
                    value='''It's as simple as\n`$tip @user <amount> <token>`
For example:\n`$tip @hades 1 tomb`\n''', inline=False)
    embed.add_field(name="Commands",
                    value='''Here is a list of all the commands available:
```$balance\n$deposit\n$tip\n$tokens\n$withdraw```\n''', inline=False)
    # embed.set_thumbnail(url="https://c4.wallpaperflare.com/wallpaper/645/910/380/fantasy-art-charon-wallpaper-preview.jpg")
    embed.set_thumbnail(url="https://www.emp-online.es/dw/image/v2/BBQV_PRD/on/demandware.static/-/Sites-master-emp/default/dwd6c21498/images/3/8/6/3/386335a.jpg?sfrm=png")
    embed.set_footer(text='''For help with a specific command run `$help \
<command>`''')

    return embed

def help_balance():
    embed = discord.Embed(title="Balance help", color=0x117de1)
    embed.description = "Check your token's balance."
    embed.add_field(name="Usage", value="`$balance <token>`", inline=False)
    embed.add_field(name="Example", value="`$balance ftm`", inline=False)
    embed.set_footer(text='See `$tokens` for a list of supported tokens')

    return embed

def help_deposit():
    embed = discord.Embed(title="Deposit help", color=0x117de1)
    embed.description = '''Deposit tokens to your Discord user. Deposit \
**ONLY** supported tokens. See `$tokens` for the complete list.'''
    embed.add_field(name="Usage", value="`$deposit [device]`")
    embed.set_footer(text="See '$tokens' for a list of supported tokens")
    embed.set_footer(text='''Pro tip: Use `$deposit mobile` for easy \
copy-pasting on mobile''')
    
    return embed

def help_tip():
    embed = discord.Embed(title="Tip help", color=0x117de1)
    embed.description = "Send tokens to another Discord user."
    embed.add_field(name="Usage", value="`$tip @user <amount> <token>`",
                    inline=False)
    embed.add_field(name="Example", value="`$tip @COMA 1 ftm`", inline=False)
    embed.set_footer(text='See `$tokens` for a list of supported tokens')

    return embed

def help_withdraw():
    embed = discord.Embed(title="Withdraw help", color=0x117de1)
    embed.description = "Withdraw tokens to an address."
    embed.add_field(name="Usage", value="`$withdraw <token>`", inline=False)
    embed.add_field(name="Example", value="`$withdraw ftm`", inline=False)
    embed.set_footer(text='See `$tokens` for a list of supported tokens')

    return embed

def help_tokens():
    embed = discord.Embed(title="Tokens help", color=0x117de1)
    embed.description = "Check the list of supported tokens."
    embed.add_field(name="Usage", value="`$tokens`", inline=False)

    return embed

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

def deposit_address(address):
    embed = discord.Embed(title=f"Deposit", color=0x00e500)
    embed.description = f'''This is your unique address that is associated with \
            your discord user. Deposit your tokens to this address only.'''
    embed.add_field(name="Your deposit address",
            value=f"`{address}`")
    embed.set_footer(text='''Pro tip: Use "$deposit mobile" for easy \
copy-pasting on mobile''')
    return embed

def deposit_address_mobile(address):
    embed = discord.Embed(title=f"Deposit", color=0x00e500)
    embed.description = f'''This is your unique address that is associated with \
your discord user. Deposit your tokens to this address only. Here \
is your address for easy copy pasting :arrow_down: :arrow_down: \
:arrow_down:'''
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

def withdrawal_ok_prompt(amount, token, address, fee):
    token = token.upper()
    embed = discord.Embed(title=f"Confirm {token} withdrawal", color=0xf28804)
    embed.description = '''Please make sure everything is correct. This cannot \
be reversed.'''
    embed.add_field(name="Destination address", value=f"`{address}`",
            inline=False)
    embed.add_field(name="Withdrawal amount", value=f"**{amount} {token}**",
            inline=False)
    embed.add_field(name="Withdrawal fee", value=f"**{amount} {token}**",
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
    if balance and balance.as_tuple().exponent < -9:
        balance = round(balance, 9)
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