import sqlite3

conn = sqlite3.connect("test.db")

cur = conn.cursor()

conn.execute("CREATE TABLE IF NOT EXISTS library (title TEXT, type TEXT, directory TEXT, location TEXT)")

data = cur.execute("SELECT *  FROM library")

for row in data:
    print(row)

cur.close()
conn.close()