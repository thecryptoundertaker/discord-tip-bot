import sqlite3
import logging

logger = logging.getLogger(__name__)

from eth_account import Account

def create_connection(db_file):
    """
    Create a database connection to the SQLite database specified by db_file
    :param db_file: database file
    :return: Connection object
    """

    try:
        return sqlite3.connect(db_file)
    except:
        raise

def init_db(db_file):
    #TODO: Find a way to securely store private keys
    conn = create_connection(db_file)
    cur = conn.cursor()
    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS accounts (
                    user_id INTEGER PRIMARY KEY,
                    key TEXT NOT NULL UNIQUE
                    )''')
        conn.commit()
    except:
        raise

    return conn

def insert_account(conn, new_entry):
    """
    Insert a new (user_id, key) to the accounts table
    :param conn: Connection object
    :param new_entry: Tuple with (user_id (int), key (hex str))
    """
    print(f"Inserting {new_entry} to db...")
    query = '''INSERT INTO accounts (user_id,key) VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(query, new_entry)
    conn.commit()

def get_account_from_db(conn, user_id):
    """
    Get a user's account from the accounts table
    :param conn: Connection object
    :param user_id: Discord user id
    :return: Account object
    """

    cur = conn.cursor()
    cur.execute("SELECT key FROM accounts WHERE user_id=?", (user_id,))
    key = cur.fetchone()
    if not key:
        return None
    account = Account.from_key(key[0])

    return account
