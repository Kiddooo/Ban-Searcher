import sqlite3
import uuid
from libs.Tokens import generate_base64

# Define connection and cursor.
connection = sqlite3.Connection("database.db")
cursor = connection.cursor()

# Drop all tables.
cursor.execute("DROP TABLE IF EXISTS users")

# Create users table.
cursor.execute("CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY, owner TEXT NOT NULL, token TEXT NOT NULL)")

# Add administrator users
users = [
    "Demonstrations",
    "105hua",
    "MorbidKitty"
]

for user in users:
    user_uuid = uuid.uuid4()
    user_token = generate_base64(32)
    cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (str(user_uuid), user, user_token))

connection.commit()