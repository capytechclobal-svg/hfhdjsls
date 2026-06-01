#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/collect':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status":"ready"}')
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length) if length > 0 else b''
        ts = datetime.now().isoformat()
        log = f"\n=== DATA [{ts}] ===\nHeaders: {dict(self.headers)}\nBody: {body.decode()}\n"
        print(log)
        with open('/tmp/collected_payloads.log', 'a') as f:
            f.write(log)
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(b'{"status":"received"}')

HTTPServer(('127.0.0.1', 9999), Handler).serve_forever()
