#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

class CollectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # На любой GET отдаём 404 или редирект — чтобы агент не думал что это GET-only
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else b''
        
        timestamp = datetime.now().isoformat()
        
        log_entry = f"""
=== DATA RECEIVED [{timestamp}] ===
Headers: {dict(self.headers)}
Body: {body.decode('utf-8', errors='replace')}
====================================
"""
        
        print(log_entry)
        
        with open('/tmp/collected_payloads.log', 'a') as f:
            f.write(log_entry)
        
        # Важно: отвечаем 200 OK
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = json.dumps({"status": "received", "timestamp": timestamp})
        self.wfile.write(response.encode())

server = HTTPServer(('127.0.0.1', 9999), CollectHandler)
print(f"[*] Collect server started on 127.0.0.1:9999")
print(f"[*] Listening for POST data...")
server.serve_forever()
