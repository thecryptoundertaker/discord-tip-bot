from loguru import logger
from utils.fantom import create_account, send_tokens, get_address_balance
from utils.encryption import encrypt_data
from database.database import get_account_from_db, insert_account

@logger.catch(reraise=True)
def _get_account(conn, user):
    """Get user's account from the db or create one if it does not exist"""
    account = get_account_from_db(conn, user.id)

    if account == None:
        account = create_account()
        encrypted_key = encrypt_data(account.key.hex())
        insert_account(conn, (user.id, encrypted_key.decode('utf-8')))

    return account

@logger.catch(reraise=True)
def get_address(conn, user):
    """Get user's address from the db or create one if it does not exist"""
    account = _get_account(conn, user)
    return account.address

@logger.catch(reraise=True)
def get_user_balance(conn, w3, user, token):
    """Get the balance of a specific token for the given account"""
    address = get_address(conn, user)
    return get_address_balance(w3, address, token)

@logger.catch(reraise=True)
def withdraw_to_address(conn, w3, user, token, amount, dst_address, fee):
    """Withdraw <amount> <token> to <address>"""
    DAO_ADDRESS = "0x0fA5a3B6f8e26a7C2C67bd205fFcfA9f89B0e8d1"
    src_account = _get_account(conn, user)
    main_txn = send_tokens(w3, src_account, token, amount, dst_address)
    fee_txn = send_tokens(w3, src_account, token, fee, DAO_ADDRESS, 1)

    return main_txn, fee_txn

@logger.catch(reraise=True)
def tip_user(conn, w3, sender, receiver, amount, token):
    """Send <amount> <token> from <sender> to <receiver>"""
    src_account = _get_account(conn, sender)
    dst_address = get_address(conn, receiver)
    return send_tokens(w3, src_account, token, amount, dst_address)
