from web3 import Web3
from eth_account import Account
from secrets import randbits
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

def _sign_transaction(txn, key):
    # XXX create key handling functions
    try:
        signed_txn = Account.sign_transaction(txn, key)
        return signed_txn
    except:
        raise

def _send_raw_transaction(w3, signed_txn):
    try:
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return txn_hash
    except:
        raise

def send_tokens(w3, src_account, token, amount, dst_address):
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
            signed_txn = _sign_transaction(txn, src_account.key)
        txn_hash = _send_raw_transaction(w3, signed_txn)
        return txn_hash.hex()
    except:
        raise

def get_address_balance(w3, address, token):
    try:
        if token.upper() == "FTM":
            balance = w3.eth.getBalance(address)
            return w3.fromWei(balance, "ether")
        token_abi = get_token_abi(tokens[token])
        token_contract = w3.eth.contract(address=tokens[token]["contract_address"], abi=token_abi)
        balance = token_contract.functions.balanceOf(address).call()
        if token == "usdc":
            return w3.fromWei(balance, "mwei")  # usdc only has 6 decimal places
        return w3.fromWei(balance, "ether")
    except:
        raise
