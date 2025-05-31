from http.server import BaseHTTPRequestHandler, HTTPServer
import json

books = [
    {"id": 1, "titulo": "Harry Potter", "autor": "J.K. Rowling"},
    {"id": 2, "titulo": "O Príncipe", "autor": "Maquiavel"}
]
next_id = 3

class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/':
            self._send_response(200, {"message": "API de livros está no ar!"})

        elif self.path == '/books':
            self._send_response(200, books)

        elif self.path.startswith('/books/'):
            try:
                book_id = int(self.path.split('/')[-1])
                book = next((b for b in books if b["id"] == book_id), None)
                if book:
                    self._send_response(200, book)
                else:
                    self._send_response(404, {"error": "Livro não encontrado"})
            except ValueError:
                self._send_response(400, {"error": "ID inválido"})
        else:
            self._send_response(404, {"error": "Rota não encontrada"})

    def do_POST(self):
        if self.path == '/books':
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


    def _send_response(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps(data).encode()
        self.wfile.write(response)

def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('🚀 Servidor rodando na porta 8000...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
