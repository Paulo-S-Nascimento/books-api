from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import urllib

books = [
    {"id": 1, "titulo": "Harry Potter", "autor": "J.K. Rowling"},
    {"id": 2, "titulo": "O príncipe", "autor": "Maquiavel"}
]
next_id = 3

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/books':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(books).encode())
        elif self.path.startswith('/books/'):
            try:
                book_id = int(self.path.split('/')[-1])
                book = next((b for b in books if b["id"] == book_id), None)
                if book:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(book).encode())
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'Book not found')
            except:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'Invalid ID')
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/books':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            global next_id
            new_book = {
                "id": next_id,
                "titulo": data.get("titulo"),
                "autor": data.get("autor")
            }
            next_id += 1
            books.append(new_book)

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(new_book).encode())
        else:
            self.send_response(404)
            self.end_headers()

def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    print('Server running on port 8000...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
