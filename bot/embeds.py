import discord

def list_tokens(tokens):
    embed = discord.Embed(title="Tokens supported", color=0x117de1)
    embed.description = '\n'.join(
                        [f"**{tokens[token]['name']}** ({token.upper()})"
                        for token in tokens.keys()])
    return embed

def deposit_address(token, address):
    token = token.upper()
    embed = discord.Embed(title=f"Deposit {token}", color=0x00e500)
    embed.description = f'''This is your unique address that is associated with \
            your discord user. Deposit {token} to this address only.'''
    embed.add_field(name="Your deposit address", value=f"`{address}`")
    return embed
