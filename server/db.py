from os import path
from sqlite3 import Connection, Cursor, connect


class Database:

    def __init__(self, db_path: str):
        self.__conn = self.__connect(db_path)

    # Returns a connection to the DB at the given path
    # Creates the DB if it does not exist
    def __connect(self, db_path: str) -> Connection:
        if not path.exists(db_path):
            open(db_path, "w+").close()
        return self.__init_db(db_path)

    # Returns a connection to the DB
    # Creates the tables if they do not exist
    def __init_db(self, db_path: str) -> Connection:
        conn: Connection = connect(db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS "users" (
                    "id"        INTEGER NOT NULL UNIQUE,
                    "username"  TEXT UNIQUE,
                    PRIMARY KEY("id")
            );""")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS "games" (
                    "user_id"   INTEGER,
                    "game_id"   INTEGER,
                    "wishlist"  INTEGER
            );""")
        return conn
