import argparse
import re
import sys
import sqlite3
import uuid
from libs.Tokens import generate_base64

parser = argparse.ArgumentParser()
parser.add_argument("--username")
args = parser.parse_args()

username_regex = re.compile(r"^[a-zA-Z0-9_]{3,16}$")

if args.username is None or args.username == "":
    print("You need to provide a username.")
    sys.exit(0)

if username_regex.match(args.username) is None:
    print("The provided username is not valid.")
    sys.exit(0)

connection = sqlite3.Connection("database.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM users WHERE owner = ?", (args.username,))
rows = cursor.fetchall()
if len(rows) >= 1:
    print("This username already exists in the database.")
    sys.exit(0)

id_exists = True
while id_exists == True:
    user_id = uuid.uuid4()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    rows = cursor.fetchall()
    if len(rows) == 0:
        id_exists = False

token_exists = True
while token_exists == True:
    user_token = generate_base64(32)
    cursor.execute("SELECT * FROM users WHERE token = ?", (user_token,))
    rows = cursor.fetchall()
    if len(rows) == 0:
        token_exists = False

cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (user_id, args.username, user_token))
connection.commit()

print(f"{args.username} has been added as a user.")
print(f"ID: {user_id}")
print(f"Token: {user_token}")