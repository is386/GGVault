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
        conn: Connection = connect(db_path, check_same_thread=False)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS "users" (
                    "id"        INTEGER NOT NULL UNIQUE,
                    "username"  TEXT UNIQUE,
                    "password"  TEXT,
                    PRIMARY KEY("id")
            );""")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS "games" (
                    "user_id"   INTEGER,
                    "game_id"   INTEGER,
                    "wishlist"  INTEGER
            );""")
        return conn

    # Closes the connection to the database
    def close(self):
        self.__conn.close()

    # Returns True if the username is available, false otherwise
    def user_exists(self, user: str) -> bool:
        c: Cursor = self.__conn.cursor()
        c = self.__conn.execute(
            "SELECT username FROM users WHERE username=?", (user,))
        rows: list = c.fetchall()
        return len(rows) == 1

    # Returns the given user's hashed password
    def get_pass(self, user: str) -> bytes:
        c: Cursor = self.__conn.cursor()
        c = self.__conn.execute(
            "SELECT password FROM users WHERE username=?", (user,))
        rows: list = c.fetchall()
        return rows[0][0]

    # Inserts the given username and password into the DB
    def insert_user(self, user: str, pw: bytes):
        self.__conn.execute("""
            INSERT INTO
                users(username, password)
            VALUES
                (?, ?)
            """, (user, pw))
        self.__conn.commit()

    # Inserts the given game id into the DB
    def insert_game(self, user_id: int, game_id: int, wishlist: bool):
        self.__conn.execute("""
            INSERT INTO
                games(user_id, game_id, wishlist)
            VALUES
                (?, ?, ?)
            """, (user_id, game_id, int(wishlist)))
        self.__conn.commit()

    # Deletes the given game id from the DB
    def delete_game(self, user_id: int, game_id: int):
        self.__conn.execute("""
            DELETE FROM
                games
            WHERE
                user_id=? AND game_id=?;
            """, (user_id, game_id))
        self.__conn.commit()

    # Moves the given game id to/from wishlist
    def move_game(self, user_id: int, game_id: int, wishlist: bool):
        self.__conn.execute("""
            UPDATE
                games
            SET
                wishlist=?
            WHERE
                user_id=? AND game_id=?;
            """, (int(wishlist), user_id, game_id))
        self.__conn.commit()

    # Returns a list of the games the user has in their lists
    def get_games(self, user_id: int) -> list:
        c: Cursor = self.__conn.cursor()
        c = self.__conn.execute(
            "SELECT * FROM games WHERE user_id=?", (user_id,))
        return c.fetchall()