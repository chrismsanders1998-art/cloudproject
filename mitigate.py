import sqlite3

conn = sqlite3.connect("traffic.db")
cur = conn.cursor()

suspicious_ips = set()
cur.execute("""
SELECT source_ip
FROM requests
WHERE path = '/login' AND status_code = 401
GROUP BY source_ip
HAVING COUNT(*) >= 3
""")

for row in cur.fetchall():
    suspicious_ips.add(row[0])

cur.execute("""
SELECT source_ip
FROM requests
WHERE path = '/admin'
GROUP BY source_ip
""")

for row in cur.fetchall():
    suspicious_ips.add(row[0])

conn.close()

if suspicious_ips:
    print("Mitigation action:")
for ip in suspicious_ips:
        print(f"Would block IP: {ip}")
else:
    print("No IPs to mitigate.")
