import sqlite3

con = sqlite3.connect("user_data.db")
cursor = con.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())

cursor.execute("Select * from users;")
print(cursor.fetchall())
