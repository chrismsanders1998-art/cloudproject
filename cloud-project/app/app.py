from flask import Flask, request
from datetime import datetime
import os

app = Flask(__name__)

BLOCKLIST_FILE = "/app/blocked_ips.txt"

def get_blocked_ips():
    if not os.path.exists(BLOCKLIST_FILE):
        return set()
    with open(BLOCKLIST_FILE, "r") as f:
        return {line.strip() for line in f if line.strip()}

@app.before_request
def block_bad_ips():
    blocked_ips = get_blocked_ips()
    if request.remote_addr in blocked_ips:
        print(f"{datetime.now()} | {request.remote_addr} | {request.method} | {request.path} | 403 BLOCKED", flush=True)
        return "Forbidden", 403

def log_request(status_code):
    print(f"{datetime.now()} | {request.remote_addr} | {request.method} | {request.path} | {status_code}", flush=True)

@app.route('/')
def home():
    log_request(200)
    return "Home page"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        if username == 'admin' and password == 'password123':
            log_request(200)
            return "Login successful", 200
        log_request(401)
        return "Login failed", 401
    log_request(200)
    return '''
        <form method="post">
            <input name="username" placeholder="username">
            <input name="password" placeholder="password" type="password">
            <button type="submit">Login</button>
        </form>
    '''

@app.route('/admin')
def admin():
    log_request(403)
    return "Forbidden", 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
