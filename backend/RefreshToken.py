import argparse
import re
import sys
import sqlite3
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
if len(rows) < 1:
    print("No such username in database.")
    sys.exit(0)

new_token_generated = False
old_token = rows[0][2]
user_id = rows[0][0]
owner = rows[0][1]

while new_token_generated is False:
    new_token = generate_base64(32)
    cursor.execute("SELECT * FROM users WHERE token = ?", (new_token,))
    token_rows = cursor.fetchall()
    if len(token_rows) == 0:
        new_token_generated = True

cursor.execute("UPDATE users SET token = ? WHERE id = ?", (new_token, user_id))
connection.commit()
print(f"{owner}'s token has been updated.")
print(f"New Token: {new_token}")
