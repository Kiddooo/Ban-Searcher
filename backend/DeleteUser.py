import argparse
import sqlite3
import sys
import uuid

from libs.Tokens import generate_base64

parser = argparse.ArgumentParser()
parser.add_argument("--uuid")
args = parser.parse_args()


def is_valid_uuid(input_uuid):
    try:
        uuid.UUID(input_uuid, version=4)
        return True
    except ValueError:
        return False


if is_valid_uuid(args.uuid) is False:
    print("The provided username is not valid.")
    sys.exit(0)

connection = sqlite3.Connection("database.db")
cursor = connection.cursor()

cursor.execute("DELETE FROM users WHERE id = ?", (args.uuid,))
connection.commit()
print("User has been deleted.")
