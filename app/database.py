import sqlite3

DB_PATH = "api_test_lab.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT NOT NULL
            )
            """
        )


def create_user(username, password):
    with get_connection() as connection:
        connection.execute(
            """
                INSERT INTO users(username, password)
                VALUES (?, ?)
            """,
            (username, password),
        )

def get_user_by_username(username):
    with get_connection() as connection:
        cusor = connection.execute(
            """
                SELECT username, password from users WHERE username = ?
            """,
            (username,),
        )
        row = cusor.fetchone()
    if row is None:
        return None
    return {
        "username":row[0],
        "password":row[1]
    }

def clear_user():
    with get_connection() as connection:
        connection.execute("DELETE FROM users")