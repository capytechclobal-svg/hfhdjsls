from flask import Flask, request, jsonify, send_from_directory
import json
import os
from datetime import datetime

app = Flask(__name__)

# Log file
LOG_FILE = "/opt/chatgpt-bounty/collected_data.log"

def log_request(data):
    """Log incoming data with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {json.dumps(data, indent=2)}\n"
    log_entry += "="*80 + "\n"
    
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    
    # Also print to console
    print(log_entry)

@app.route("/")
def index():
    return "OK", 200

@app.route("/static/page.html")
def serve_page():
    return send_from_directory("static", "page.html")

@app.route("/collect", methods=["POST"])
def collect_data():
    """Endpoint for ChatGPT to POST data to"""
    data = {
        "method": request.method,
        "headers": dict(request.headers),
        "body": request.get_data(as_text=True),
        "form": dict(request.form),
        "args": dict(request.args),
        "ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent", "")
    }
    
    log_request(data)
    
    return jsonify({"status": "received", "message": "Data collected successfully"}), 200

@app.route("/collect", methods=["GET"])
def collect_data_get():
    """Also accept GET requests with query params"""
    data = {
        "method": "GET",
        "headers": dict(request.headers),
        "args": dict(request.args),
        "ip": request.remote_addr,
        "user_agent": request.headers.get("User-Agent", "")
    }
    
    log_request(data)
    
    return jsonify({"status": "received", "message": "Data collected successfully"}), 200

@app.route("/view-logs")
def view_logs():
    """View collected data (password protected simple view)"""
    if request.remote_addr != "127.0.0.1":
        return "Access denied", 403
    
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            return f"<pre>{f.read()}</pre>"
    return "No logs yet"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
