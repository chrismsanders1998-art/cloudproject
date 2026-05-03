import sqlite3

BLOCKLIST_FILE = "/home/user/cloud-project/app/blocked_ips.txt"

conn = sqlite3.connect("traffic.db")
cur = conn.cursor()

suspicious_ips = set()
alerts = []

# Rule 1: repeated failed login attempts
cur.execute("""
SELECT source_ip, COUNT(*)
FROM requests
WHERE path = '/login' AND status_code = 401
GROUP BY source_ip
HAVING COUNT(*) >= 3
""")
for ip, count in cur.fetchall():
    suspicious_ips.add(ip)
    alerts.append(f"ALERT: {ip} had {count} failed login attempts")

# Rule 2: suspicious/restricted/path-traversal style requests
cur.execute("""
SELECT source_ip, path, COUNT(*)
FROM requests
WHERE path IN ('/admin', '/etc/passwd', '/../../etc/passwd', '/backup.zip', '/config.php')
GROUP BY source_ip, path
HAVING COUNT(*) >= 1
""")
for ip, path, count in cur.fetchall():
    suspicious_ips.add(ip)
    alerts.append(f"ALERT: {ip} requested suspicious path {path} {count} time(s)")

# Rule 3: repeated suspicious path activity
cur.execute("""
SELECT source_ip, COUNT(*)
FROM requests
WHERE path IN ('/admin', '/etc/passwd', '/../../etc/passwd', '/backup.zip', '/config.php')
GROUP BY source_ip
HAVING COUNT(*) >= 2
""")
for ip, count in cur.fetchall():
    suspicious_ips.add(ip)
    alerts.append(f"ALERT: {ip} made {count} suspicious path requests")

conn.close()

if alerts:
    print("Suspicious activity detected:")
    for alert in alerts:
        print(alert)
else:
    print("No suspicious activity detected.")

if suspicious_ips:
    print("\\nMitigation actions:")
    existing = set()
    try:
        with open(BLOCKLIST_FILE, "r") as f:
            existing = {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        pass

    updated = existing | suspicious_ips

    with open(BLOCKLIST_FILE, "w") as f:
        for ip in sorted(updated):
            f.write(ip + "\n")

    for ip in suspicious_ips:
        print(f"Blocked in app-level blocklist: {ip}")
else:
    print("\\nNo IPs to block.")
