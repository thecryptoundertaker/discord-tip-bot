from utils.fantom import connect_to_fantom

# Globals
# XXX these should be moved to a separate config file that also looks for envvars

PROVIDER_ADDRESS="wss://wsapi.fantom.network/"
PROVIDER_TYPE="wss"

def main():
    fantom = connect_to_fantom(PROVIDER_ADDRESS)
    print(f"* Connected to Fantom!")
    print(f"* Node Address: {PROVIDER_ADDRESS}")
    print(f"* Provider Type: {PROVIDER_TYPE}")
    print(f"* Current Block: {fantom.eth.block_number}")

if __name__ == "__main__":
    main()
