# type: ignore
from jinja2_env import render_template
from jinja2 import Environment, FileSystemLoader
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from datetime import datetime
import urllib.parse
import mimetypes
import pathlib
import json


env = Environment(loader=FileSystemLoader("templates"))


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/":
            self.send_html_file("index.html")
        elif pr_url.path == "/message":
            self.send_html_file("message.html")
        elif pr_url.path == "/read":
            self.read_messages()
        else:
            self.send_html_file("error.html", 404)

    def do_POST(self):
        if self.path == "/message":
            self.handle_message_submission()

    def handle_message_submission(self):
        data = self.rfile.read(int(self.headers["Content-Length"]))
        data_parse = urllib.parse.unquote_plus(data.decode())
        data_dict = {
            key: value for key, value in [el.split("=") for el in data_parse.split("&")]
        }
        data_dict["timestamp"] = datetime.now().isoformat()
        self.save_to_json(data_dict)
        self.send_response(302)
        self.send_header("Location", "/read")
        self.end_headers()

    def save_to_json(self, data):
        storage_path = pathlib.Path("storage/data.json")
        if storage_path.exists():
            with open(storage_path, "r") as file:
                try:
                    messages = json.load(file)
                except json.JSONDecodeError:
                    messages = []
        else:
            messages = []

        messages.append(data)

        with open(storage_path, "w") as file:
            json.dump(messages, file, indent=4)

    def read_messages(self):
        storage_path = pathlib.Path("storage/data.json")
        if storage_path.exists():
            with open(storage_path, "r") as file:
                try:
                    messages = json.load(file)
                except json.JSONDecodeError:
                    messages = []
        else:
            messages = []

        content = render_template("read.html", {"messages": messages})
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode())

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        filepath = pathlib.Path("templates") / filename
        try:
            with open(filepath, "rb") as fd:
                self.wfile.write(fd.read())
        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            error_message = (
                "<html><body><h1>Error 404: File Not Found</h1></body></html>"
            )
            self.wfile.write(error_message.encode())

    def send_static(self):
        static_file_path = pathlib.Path("static") / self.path.strip("/")
        if static_file_path.exists():
            self.send_response(200)
            mt = mimetypes.guess_type(static_file_path)[0] or "application/octet-stream"
            self.send_header("Content-type", mt)
            self.end_headers()
            with open(static_file_path, "rb") as file:
                self.wfile.write(file.read())
        else:
            self.send_html_file("error.html", 404)


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ("", 3000)
    httpd = server_class(server_address, handler_class)
    print("Server started on http://localhost:3000")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server.")
        httpd.shutdown()
        httpd.server_close()


if __name__ == "__main__":
    server_thread = Thread(target=run)
    server_thread.start()
