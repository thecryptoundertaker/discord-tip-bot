from web3 import Web3
from eth_account import Account
from secrets import randbits
import discord
from database.database import get_account_from_db, insert_account, create_connection
from config import config

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
            # XXX add these to log file
            print(f"* Connected to Fantom!")
            print(f"* Node Address: {provider_address}")
            print(f"* Provider Type: {provider_type}")
            print(f"* Current Block: {w3.eth.block_number}")
            return w3
        else:
            return None
    except:
        raise Exception

###
# Wallet Utils
###

def create_account():
    try:
        return Account.create(randbits(4096))
    except:
        raise

def get_account_from_key(private_key):
    try:
        return Account.from_key(private_key)
    except:
        raise

def get_balance_for_address(web3, address):
    try:
        return web3.eth.get_balance(address)
    except:
        raise

def get_address(user: discord.Member):
    """Get user's address from the db or create one if it does not exist"""
    conn = create_connection(config["DATABASE_NAME"])
    if isinstance(user, discord.Member):
        id_ = user.id
    else:
        id_ = user
    account = get_account_from_db(conn, id_)

    #if user not in db
    if account == None:
        account = _create_account()
        insert_account(conn, (id_, account.key.hex()))

    return account.address
