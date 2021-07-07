from web3 import Web3
from eth_account import Account
from secrets import randbits
import discord
from database.database import get_account_from_db, insert_account
from tokens.tokens import tokens, get_token_abi

import logging
logger = logging.getLogger(__name__)

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


# XXX should this be moved to database or discord or a new users module?
def _get_account(conn, user):
    """Get user's account from the db or create one if it does not exist"""
    account = get_account_from_db(conn, user.id)

    #if user not in db
    if account == None:
        account = create_account()
        insert_account(conn, (user.id, account.key.hex()))

    return account

def _send_tokens(w3, src_account, token, amount, dst_address):
    """Send <amount> <token> from <src_account> to <dst_address>"""
    try:
        nonce = w3.eth.getTransactionCount(src_account.address)
        amount = w3.toWei(amount, "ether")
        if token.lower() == "ftm":
            signed_txn = Account.sign_transaction({
                            "chainId": 250,
                            "gas": 80000,
                            "gasPrice": w3.toWei(60, "gwei"),
                            "nonce": nonce,
                            "to": dst_address,
                            "value": amount
                        }, src_account.key)

        else:
            token_abi = get_token_abi(tokens[token])
            token_contract = w3.eth.contract(address=tokens[token]["contract_address"], abi=token_abi)
            contract_func = token_contract.functions.transfer(dst_address, amount)
            txn = contract_func.buildTransaction({
                                "chainId": 250,
                                "gas": 80000,
                                "gasPrice": w3.toWei(60, "gwei"),
                                "nonce": nonce
                            })
            # XXX wrap signing transaction in a function, create key handling functions
            signed_txn = Account.sign_transaction(txn, src_account.key)
        # XXX wrap send_raw_transaction to trap exceptions
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return txn_hash.hex()
    except:
        raise

def get_balance_for_address(w3, address, token):
    try:
        if token.upper() == "FTM":
            balance = w3.eth.getBalance(address)
            return w3.fromWei(balance, "ether")
        token_abi = get_token_abi(tokens[token])
        token_contract = w3.eth.contract(address=tokens[token]["contract_address"], abi=token_abi)
        balance = token_contract.functions.balanceOf(address).call()
        return w3.fromWei(balance, "ether")
    except:
        raise

def get_address(conn, user):
    """Get user's address from the db or create one if it does not exist"""
    account = _get_account(conn, user)
    return account.address

def get_user_balance(conn, w3, user, token):
    """Get the balance of a specific token for the given account"""
    address = get_address(conn, user)
    return get_balance_for_address(w3, address, token)

def withdraw_to_address(conn, w3, user, token, amount, dst_address):
    """Withdraw <amount> <token> to <address>"""
    src_account = _get_account(conn, user)
    return  _send_tokens(w3, src_account, token, amount, dst_address)

def tip_user(conn, w3, sender, receiver, amount, token):
    """Send <amount> <token> from <sender> to <receiver>"""
    src_account = _get_account(conn, sender)
    dst_address = get_address(conn, receiver)
    return _send_tokens(w3, src_account, token, amount, dst_address)
