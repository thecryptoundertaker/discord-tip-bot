from loguru import logger
from web3 import Web3
from eth_account import Account
from secrets import randbits
from tokens.tokens import tokens, get_token_abi
from utils.utils import to_decimal, from_decimal
from decimal import Decimal
from config import config

###
# Node utils
###

@logger.catch
def connect_to_fantom(provider_address, provider_type="wss", timeout=60):
    if provider_type == "wss" or "ws":
        w3 = Web3(Web3.WebsocketProvider(provider_address,
                    websocket_timeout=timeout))
    else:
        raise Exception
    if w3.isConnected():
        logger.info("Connected to Fantom!")
        logger.info("Node Address: {}", provider_address)
        logger.info("Provider Type: {}", provider_type)
        logger.info("Current Block: {}", w3.eth.block_number)
        return w3
    else:
        return None

###
# Wallet Utils
###

@logger.catch
def create_account():
    return Account.create(randbits(4096))

@logger.catch
def _sign_transaction(txn, account):
    return Account.sign_transaction(txn, account.key)

@logger.catch
def _send_raw_transaction(w3, signed_txn):
    txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return txn_hash

@logger.catch
def send_tokens(w3, src_account, token, amount, dst_address, pending_txs=0):
    """Send <amount> <token> from <src_account> to <dst_address>"""
    if amount == 0:
        return
    nonce = w3.eth.getTransactionCount(src_account.address) + pending_txs
    amount = to_decimal(amount, tokens[token]['decimals'])
    txn_details = {
            "chainId": 250,
            "gas": int(config["GAS_LIMIT"]),
            "gasPrice": w3.toWei(Decimal(config["GAS_PRICE"]), "gwei"),
            "nonce": nonce
            }
    if token.lower() == "ftm":
        txn_details.update({"to": dst_address, "value": amount})
        signed_txn = _sign_transaction(txn_details, src_account)
    else:
        token_abi = get_token_abi(tokens[token])
        token_contract = w3.eth.contract(
                                address=tokens[token]["contract_address"],
                                abi=token_abi)
        contract_func = token_contract.functions.transfer(dst_address, amount)
        txn = contract_func.buildTransaction(txn_details)
        signed_txn = _sign_transaction(txn, src_account)
    txn_hash = _send_raw_transaction(w3, signed_txn)
    if not txn_hash:
        return None
    return txn_hash.hex()

@logger.catch
def get_address_balance(w3, address, token):
    if token.upper() == "FTM":
        balance = w3.eth.getBalance(address)
        return from_decimal(balance, tokens[token]["decimals"])
    token_abi = get_token_abi(tokens[token])
    token_contract = w3.eth.contract(
                                address=tokens[token]["contract_address"],
                                abi=token_abi)
    balance = token_contract.functions.balanceOf(address).call()
    return from_decimal(balance, tokens[token]["decimals"])
