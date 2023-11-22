# Assume psycopg2 installed on pip
# Assume VSDB01 is Hostname, DB port number 5432, db name VSDB , user user1,
# Assume http configured for 8080
# Database configuration

import http.server
import socketserver
import json
import psycopg2
from http import HTTPStatus
from urllib.parse import urlparse, parse_qs
from http.server import SimpleHTTPRequestHandler


DB_HOST = 'VSDB01'
DB_PORT = '5432'
DB_NAME = 'VSDB'
DB_USER = 'user1'
DB_PASSWORD = 'YYYYYYY'

# Create the 'visitors' table if not exists
with psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD) as conn:
    with conn.cursor() as cur:
        cur.execute('CREATE TABLE IF NOT EXISTS visitors (ip_address VARCHAR(15) PRIMARY KEY);')

class VisitorHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path == '/':
            self.show_stats()
        elif path == '/version':
            self.show_version()
        else:
            super().do_GET()

    def show_stats(self):
        ip_address = self.client_address[0]
        with psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD) as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute('INSERT INTO visitors (ip_address) VALUES (%s);', (ip_address,))
                except psycopg2.IntegrityError:
                    # If the IP address already exists, do nothing
                    pass
                cur.execute('SELECT COUNT(*) FROM visitors;')
                total_visitors = cur.fetchone()[0]

        response = f'Total Unique Visitors: {total_visitors}'.encode('utf-8')
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response)
    def show_version(self):
        version_info = {'version': '1.0'}
        response = json.dumps(version_info).encode('utf-8')
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response)

with socketserver.TCPServer(("", 8080), VisitorHandler) as httpd:
    print("Server running on port 8080...")
    httpd.serve_forever()
