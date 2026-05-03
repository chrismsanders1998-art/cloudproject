Containerized Web Attack Detection and Mitigation

Overview

This project shows how to simulate, monitor, detect, and mitigate basic application-layer attacks against a containerized web application. The target is a simple Flask web app running in Docker on an Ubuntu virtual machine. A second system acts as the attacker and sends suspicious HTTP requests. Python scripts are then used to collect logs, store request data in SQLite, detect suspicious behavior, and block the attacker IP.

───

Tools Used

• 2 Ubuntu VMs (one being attacked and one doing the attacking)
• Docker (for contatinerization)
• Flask (for running a web application)
• Python 3 (for scripting)
• SQLite (for database)
• curl

───

Components:

Target Application

The web application runs inside Docker and logs:

• timestamp
• source IP
• HTTP method
• request path
• response code

Monitoring

collect_logs.py reads the application logs and stores request data in traffic.db.

Detection

The detection logic looks for:

• repeated failed login attempts
• suspicious path requests
• repeated suspicious activity from the same IP

Mitigation

When an IP is flagged, it is added to blocked_ips.txt. The Flask application checks this file and denies future requests from blocked IPs.

───

The following attack types were tested:

• repeated failed logins
• requests to /admin
• requests to suspicious files such as /config.php
• path traversal-style requests

───

Steps

1. Start the app

docker build -t target-webapp .
docker run -d --name target-app -p 5000:5000 -v /home/user/cloud-project/app/blocked_ips.txt:/app/blocked_ips.txt target-webapp

2. Initialize the database

python3 init_db.py

3. Generate attack traffic from seperate system on the same network

curl -X POST -d "username=test&password=bad" http://TARGET_IP:5000/login
curl http://TARGET_IP:5000/admin
curl http://TARGET_IP:5000/config.php

4. Collect logs

python3 collect_logs.py

5. Detect and mitigate

python3 detection_mitigation.py

───

Unblocking

Blocked IPs are stored in:

blocked_ips.txt

To unblock, remove the IP address from the file and restart the container if needed.

───

Summary

This project demonstrates the full process of:

• attacking a containerized web app
• collecting and storing logs
• detecting suspicious behavior
• blocking the attacker

───

Christopher Sanders