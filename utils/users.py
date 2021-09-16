from loguru import logger
from utils.fantom import create_account, send_tokens, get_address_balance
from utils.encryption import encrypt_data
from database.database import get_account_from_db, insert_account
from config import config

@logger.catch
def _get_account(conn, user):
    """Get user's account from the db or create one if it does not exist"""
    account = get_account_from_db(conn, user.id)

    if account == None:
        account = create_account()
        encrypted_key = encrypt_data(account.key.hex())
        insert_account(conn, (user.id, encrypted_key.decode('utf-8')))

    return account

@logger.catch
def get_address(conn, user):
    """Get user's address from the db or create one if it does not exist"""
    account = _get_account(conn, user)
    return account.address

@logger.catch
def get_user_balance(conn, w3, user, token):
    """Get the balance of a specific token for the given account"""
    address = get_address(conn, user)
    return get_address_balance(w3, address, token)

@logger.catch
def withdraw_to_address(conn, w3, user, token, amount, dst_address, fee):
    """Withdraw <amount> <token> to <address>"""
    DAO_ADDRESS = config["DAO_ADDRESS"]
    src_account = _get_account(conn, user)
    main_txn = send_tokens(w3, src_account, token, amount, dst_address)
    if main_txn == None:
        return None, None
    fee_txn = send_tokens(w3, src_account, token, fee, DAO_ADDRESS, 1)

    return main_txn, fee_txn

@logger.catch
def tip_user(conn, w3, sender, receiver, amount, token):
    """Send <amount> <token> from <sender> to <receiver>"""
    src_account = _get_account(conn, sender)
    dst_address = get_address(conn, receiver)
    txn_hash = send_tokens(w3, src_account, token, amount, dst_address)
    if not txn_hash:
        return None
    return txn_hash
