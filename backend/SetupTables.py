import sqlite3
import uuid

from libs.Tokens import generate_base64

# Define connection and cursor.
users_connection = sqlite3.Connection("databases/users.db")
users_cursor = users_connection.cursor()

# Drop all tables.
users_cursor.execute("DROP TABLE IF EXISTS users")

# Create users table.
users_cursor.execute(
    "CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY, owner TEXT NOT NULL, token TEXT NOT NULL)"
)

# Add administrator users
users = ["Demonstrations", "105hua", "MorbidKitty"]

for user in users:
    user_uuid = uuid.uuid4()
    user_token = generate_base64(32)
    users_cursor.execute(
        "INSERT INTO users VALUES (?, ?, ?)", (str(user_uuid), user, user_token)
    )

users_connection.commit()

cache_connection = sqlite3.Connection("databases/cache.db")
cache_cursor = cache_connection.cursor()
cache_cursor.execute("DROP TABLE IF EXISTS cache")
cache_cursor.execute(
    "CREATE TABLE IF NOT EXISTS cache(job_id TEXT PRIMARY KEY, ban_data TEXT NOT NULL, timestamp INTEGER NOT NULL, player_uuid TEXT NOT NULL)"
)
cache_connection.commit()
