import sqlite3

conn = sqlite3.connect("traffic.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT ,
    timestamp TEXT ,
    source_ip TEXT ,
    method TEXT ,
    path TEXT ,
    status_code INTEGER
)
""")

conn.commit()
conn.close()

print("DB INITIALIZED")
