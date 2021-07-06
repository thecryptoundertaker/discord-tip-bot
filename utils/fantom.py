from web3 import Web3
from eth_account import Account
from secrets import randbits
import discord
from database.database import get_account_from_db, insert_account, create_connection
from config import config
from tokens.tokens import tokens, get_token_abi

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

def _get_account(user: discord.Member):
    """Get user's account from the db or create one if it does not exist"""
    conn = create_connection(config["DATABASE_NAME"])
    account = get_account_from_db(conn, user.id)

    #if user not in db
    if account == None:
        account = create_account()
        insert_account(conn, (user.id, account.key.hex()))

    return account

def _send_tokens(src_account, token, amount, dst_address):
    """Send <amount> <token> from <src_account> to <dst_address>"""
    try:
        w3 = connect_to_fantom(config["PROVIDER_ADDRESS"])
        token_abi = get_token_abi(tokens[token])
        token_contract = w3.eth.contract(address=tokens[token]["contract_address"], abi=token_abi)
        nonce = w3.eth.getTransactionCount(src_account.address)
        amount = w3.toWei(amount, "ether")
        contract_func = token_contract.functions.transfer(dst_address, amount)
        txn = contract_func.buildTransaction({
                            "chainId": 250,
                            "gas": 80000,
                            "gasPrice": w3.toWei(60, "gwei"),
                            "nonce": nonce
                        })
        signed_txn = Account.sign_transaction(txn, src_account.key)
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return txn_hash.hex()
    except:
        raise

def get_balance_for_address(address, token):
    try:
        w3 = connect_to_fantom(config["PROVIDER_ADDRESS"])
        if token.upper() == "FTM":
            balance = w3.eth.getBalance(address)
            return w3.fromWei(balance, "ether")
        token_abi = get_token_abi(tokens[token])
        token_contract = w3.eth.contract(address=tokens[token]["contract_address"], abi=token_abi)
        balance = token_contract.functions.balanceOf(address).call()
        return w3.fromWei(balance, "ether")
    except:
        raise

def get_address(user: discord.Member):
    """Get user's address from the db or create one if it does not exist"""
    account = _get_account(user)
    return account.address



def get_balance(user: discord.Member, token: str):
    """Get the balance of a specific token from a specific user"""
    conn = create_connection(config["DATABASE_NAME"])
    address = get_address(user)
    return get_balance_for_address(address, token)

def withdraw_to_address(user: discord.Member, token: str, amount: float, dst_address: str):
    """Withdraw <amount> <token> to <address>"""
    conn = create_connection(config["DATABASE_NAME"])
    src_account = _get_account(user)
    return  _send_tokens(src_account, token, amount, dst_address)

