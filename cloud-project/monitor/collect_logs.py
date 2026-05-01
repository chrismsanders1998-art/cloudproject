import sqlite3
import subprocess

conn = sqlite3.connect("traffic.db")
cur = conn.cursor()

logs = subprocess.check_output(["docker", "logs", "target-app"], text=True)
for line in logs.splitlines():
    parts = [p.strip() for p in line.split("|")]
    if len(parts) != 5:
        continue
    timestamp, source_ip, method, path, status_code = parts
    cur.execute("""
        INSERT INTO requests (timestamp, source_ip, method, path, status_code)
        VALUES (?, ?, ?, ?, ?)
    """, (timestamp, source_ip, method, path, int(status_code)))
conn.commit()
conn.close()

print("Logs collected into database.")
