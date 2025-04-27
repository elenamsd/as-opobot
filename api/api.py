from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from db import get_collection_data
from logic import buscar_convocatorias, cargar_diccionario_sinonimos

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

        elif parsed_path.path.startswith("/buscar/"):
            query_params = parse_qs(parsed_path.query)
            palabras = query_params.get("q", [""])[0]

            if not palabras:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Missing query parameter 'q'")
                return

            try:
                # data = get_collection_data(opposition)
                # En vez de hacer get_collection_data, cargas desde un JSON fijo
                import os
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                DATA_FILE = os.path.join(BASE_DIR, "data_fake.json")
                DICT_FILE = os.path.join(BASE_DIR, "diccionario_sinonimos.json")
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                diccionario_sinonimos = cargar_diccionario_sinonimos(DICT_FILE)
                resultados = buscar_convocatorias(palabras, data, diccionario_sinonimos)

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(resultados, default=str).encode())
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(f"Error: {str(e)}".encode())

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")
