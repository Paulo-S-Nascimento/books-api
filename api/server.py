from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import time
from prometheus_client import start_http_server, Counter, Histogram, generate_latest

# Prometheus 
REQUEST_COUNT = Counter('app_requests_total', 'Total de requisições', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Tempo de resposta', ['endpoint'])
ERROR_COUNT = Counter('app_error_count', 'Total de erros', ['endpoint'])


books = [
    {"id": 1, "titulo": "Harry Potter", "autor": "J.K. Rowling"},
    {"id": 2, "titulo": "O Príncipe", "autor": "Maquiavel"}
]
next_id = 3

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        start_time = time.time()
        try:
            if self.path == '/':
                REQUEST_COUNT.labels(method='GET', endpoint='/').inc()
                self._send_response(200, {"message": "API de livros está no ar!"})

            elif self.path == '/health':
                REQUEST_COUNT.labels(method='GET', endpoint='/health').inc()
                self._send_response(200, {"status": "ok"})

            elif self.path == '/books':
                REQUEST_COUNT.labels(method='GET', endpoint='/books').inc()
                self._send_response(200, books)

            elif self.path.startswith('/books/'):
                REQUEST_COUNT.labels(method='GET', endpoint='/books/{id}').inc()
                try:
                    book_id = int(self.path.split('/')[-1])
                    book = next((b for b in books if b["id"] == book_id), None)
                    if book:
                        self._send_response(200, book)
                    else:
                        self._send_response(404, {"error": "Livro não encontrado"})
                except ValueError:
                    self._send_response(400, {"error": "ID inválido"})

            elif self.path == '/metrics':
                self.send_response(200)
                self.send_header('Content-Type', 'text/plain')
                self.end_headers()
                self.wfile.write(generate_latest())

            else:
                self._send_response(404, {"error": "Rota não encontrada"})
        except Exception:
            ERROR_COUNT.labels(endpoint=self.path).inc()
            self._send_response(500, {"error": "Erro interno do servidor"})
        finally:
            duration = time.time() - start_time
            REQUEST_LATENCY.labels(endpoint=self.path).observe(duration)

    def do_POST(self):
        start_time = time.time()
        try:
            if self.path == '/books':
                REQUEST_COUNT.labels(method='POST', endpoint='/books').inc()
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data)
                    titulo = data.get("titulo")
                    autor = data.get("autor")

                    if not titulo or not autor:
                        self._send_response(400, {"error": "Campos 'titulo' e 'autor' são obrigatórios"})
                        return

                    global next_id
                    new_book = {
                        "id": next_id,
                        "titulo": titulo,
                        "autor": autor
                    }
                    next_id += 1
                    books.append(new_book)

                    self._send_response(201, new_book)

                except json.JSONDecodeError:
                    self._send_response(400, {"error": "JSON inválido"})
            else:
                self._send_response(404, {"error": "Rota não encontrada"})
        except Exception:
            ERROR_COUNT.labels(endpoint=self.path).inc()
            self._send_response(500, {"error": "Erro interno do servidor"})
        finally:
            duration = time.time() - start_time
            REQUEST_LATENCY.labels(endpoint=self.path).observe(duration)

    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps(data).encode()
        self.wfile.write(response)

# Run server
def run():
    start_http_server(8001)  # Prometheus metrics server
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Servidor rodando na porta 8000...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
