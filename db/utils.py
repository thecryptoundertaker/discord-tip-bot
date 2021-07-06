import sqlite3
import logging

logger = logging.getLogger(__name__)

def get_db(database_file='tipbot.db'):
    try:
        logging.info("Attempting to open sqlite database")
        conn = sqlite3.connect(database_file)
        return conn
    except:
        raise

def get_db_cursor(db):
    try:
        return db.cursor()
    except:
        raise

def create_users_table(db):
    try:
        logging.info("Creating users table")
        cur = db.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users
            (ID INT PRIMARY KEY NOT NULL)
            """)
        return cur
    except:
        raise

def drop_table(db, table):
    breakpoint()
    try:
        logging.info("Dropping table %s" % table)
        cur = db.cursor()
        cur.execute("DROP TABLE IF EXISTS users")
        return cur.fetchone()
    except:
        raise

def list_all_tables(db):
    try:
        tables = db.execute("""
        SELECT name FROM sqlite_master
        WHERE type ='table' AND name NOT LIKE 'sqlite_%';
        """)
        return tables.fetchall()
    except:
        raise
