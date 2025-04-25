from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse
import json
from db import get_collection_data

class SimpleAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        print(f"Received request for path: {parsed_path.path}")
        if parsed_path.path.startswith("/data/"):
            collection_name = parsed_path.path.split("/data/")[1]
            try:
                data = get_collection_data(collection_name)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(data, default=str).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error: {str(e)}".encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
