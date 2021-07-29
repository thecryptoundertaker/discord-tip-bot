import sqlite3
from loguru import logger
from eth_account import Account

@logger.catch(reraise=True)
def get_db_connection(db_file):
    """
    Create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object
    """

    logger.debug("Connecting to {} db", db_file)
    return sqlite3.connect(db_file)

@logger.catch(reraise=True)
def init_db(conn):
    cur = conn.cursor()
    logger.debug("Creating table 'accounts' if it doesn't exist.")
    cur.execute('''CREATE TABLE IF NOT EXISTS accounts (
                user_id INTEGER PRIMARY KEY,
                key TEXT NOT NULL UNIQUE
                )''')
    conn.commit()
    return cur

@logger.catch(reraise=True)
def get_db(db_file):
    logger.debug("Getting the {} database connection", db_file)
    conn = get_db_connection(db_file)
    curr = init_db(conn)
    return conn

@logger.catch(reraise=True)
def insert_account(conn, new_entry):
    """
    Insert a new (user_id, key) to the accounts table
    :param conn: Connection object
    :param new_entry: Tuple with (user_id (int), key (hex str))
    """
    logger.info("Inserting {} to db.", new_entry)
    query = '''INSERT INTO accounts (user_id,key) VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(query, new_entry)
    conn.commit()

@logger.catch(reraise=True)
def get_account_from_db(conn, user_id):
    """
    Get a user's account from the accounts table
    :param conn: Connection object
    :param user_id: Discord user id
    :return: Account object
    """

    logger.debug("Getting account from {}.", user_id)
    cur = conn.cursor()
    cur.execute("SELECT key FROM accounts WHERE user_id=?", (user_id,))
    key = cur.fetchone()
    if not key:
        return None
    account = Account.from_key(key[0])

    return account
