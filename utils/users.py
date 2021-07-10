from utils.fantom import create_account, send_tokens, get_address_balance
from database.database import get_account_from_db, insert_account

# XXX should this be moved to database or discord or a new users module?
def _get_account(conn, user):
    """Get user's account from the db or create one if it does not exist"""
    account = get_account_from_db(conn, user.id)

    if account == None:
        account = create_account()
        insert_account(conn, (user.id, account.key.hex()))

    return account

def get_address(conn, user):
    """Get user's address from the db or create one if it does not exist"""
    account = _get_account(conn, user)
    return account.address

def get_user_balance(conn, w3, user, token):
    """Get the balance of a specific token for the given account"""
    address = get_address(conn, user)
    return get_address_balance(w3, address, token)

def withdraw_to_address(conn, w3, user, token, amount, dst_address):
    """Withdraw <amount> <token> to <address>"""
    src_account = _get_account(conn, user)
    return  send_tokens(w3, src_account, token, amount, dst_address)

def tip_user(conn, w3, sender, receiver, amount, token):
    """Send <amount> <token> from <sender> to <receiver>"""
    src_account = _get_account(conn, sender)
    dst_address = get_address(conn, receiver)
    return send_tokens(w3, src_account, token, amount, dst_address)
