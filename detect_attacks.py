import sqlite3
from collections import defaultdict

conn = sqlite3.connect("traffic.db")
cur = conn.cursor()

alerts = []

# Rule 1: repeated failed logins
cur.execute("""
SELECT source_ip, COUNT(*)
FROM requests
WHERE path = '/login' AND status_code = 401
GROUP BY source_ip
HAVING COUNT(*) >= 3
""")

failed_logins = cur.fetchall()
for ip, count in failed_logins:
    alerts.append(f"ALERT: {ip} had {count} failed login attempts")

# Rule 2: admin page access attempts
cur.execute("""
SELECT source_ip, COUNT(*)
FROM requests
WHERE path = '/admin'
GROUP BY source_ip
""")

admin_hits = cur.fetchall()
for ip, count in admin_hits:
    alerts.append(f"ALERT: {ip} accessed /admin {count} time(s)")

conn.close()

if alerts:
    print("Suspicious activity detected:")
    for alert in alerts:
        print(alert)
else:
    print("No suspicious activity detected.")
