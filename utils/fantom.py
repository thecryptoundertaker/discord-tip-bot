from web3 import Web3
from eth_account import Account
from secrets import randbits

###
# Node utils
###

def connect_to_fantom(provider_address, provider_type="wss", timeout=60):
    try:
        if provider_type == "wss" or "ws":
            w3 = Web3(Web3.WebsocketProvider(provider_address, websocket_timeout=timeout))
        else:
            raise Exception
        if w3.isConnected():
            return w3
        else:
            return None
    except:
        raise Exception

###
# Wallet Utils
###

def create_wallet():
    try:
        return Account.create(randbits(4096))
    except:
        raise

