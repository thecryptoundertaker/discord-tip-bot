from web3 import Web3

# Globals
# XXX these should be moved to a separate config file that also looks for envvars

PROVIDER_ADDRESS="wss://wsapi.fantom.network/"
PROVIDER_TYPE="wss"

# functions
def connect_to_fantom_node(provider_type="wss", provider_address=PROVIDER_ADDRESS, timeout=60):
    try:
        if provider_type == "wss" or "ws":
            w3 = Web3(Web3.WebsocketProvider(provider_address, websocket_timeout=timeout))
        else:
            raise
        if w3.isConnected():
            return w3
        else:
            raise
    except:
        return exit

# main
w3 = connect_to_fantom_node()
print(f"* Connected to Fantom!")
print(f"* Node Address: {PROVIDER_ADDRESS}")
print(f"* Provider Type: {PROVIDER_TYPE}")
print(f"* Current Block: {w3.eth.block_number}")
