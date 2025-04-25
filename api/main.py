from http.server import HTTPServer
from api import SimpleAPIHandler

def run(server_class=HTTPServer, handler_class=SimpleAPIHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Servidor ejecutándose en http://localhost:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
