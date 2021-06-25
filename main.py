from utils.fantom import connect_to_fantom
from config import config
from tipbot import tipbot

# Globals
# XXX these should be moved to a separate config file that also looks for envvars

# PROVIDER_ADDRESS="wss://wsapi.fantom.network/"
# PROVIDER_TYPE="wss"

def main():
    fantom = connect_to_fantom(config["PROVIDER_ADDRESS"])
    print(f"* Connected to Fantom!")
    print(f"* Node Address: {config['PROVIDER_ADDRESS']}")
    print(f"* Provider Type: {config['PROVIDER_TYPE']}")
    print(f"* Current Block: {fantom.eth.block_number}")
    bot = tipbot.TipBot(config)
    bot.exec()

if __name__ == "__main__":
    main()
