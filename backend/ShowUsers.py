# Run this to print all users to console.

import sqlite3

from prettytable import PrettyTable

connection = sqlite3.Connection("databases/users.db")
cursor = connection.cursor()
cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()
users_table = PrettyTable(["UUID", "Owner", "Token"])
for row in rows:
    users_table.add_row([row[0], row[1], row[2]])
print(users_table)
