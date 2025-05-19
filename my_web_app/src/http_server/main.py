# main.py
#!/usr/bin/python
# -*- coding: utf-8 -*-
# type: ignore
from http.server import HTTPServer, BaseHTTPRequestHandler
from jinja2_env import render_template
from datetime import datetime
import urllib.parse
import mimetypes
import pathlib
import json


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/message":
            self.handle_message_submission()
        else:
            self.send_error_page()

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == "/favicon.ico":
            self.send_static("static/images/favicon.ico")
        elif pr_url.path.startswith("/static/"):
            self.send_static(pr_url.path.lstrip("/"))
        elif pr_url.path == "/":
            self.send_html_file("index.html")
        elif pr_url.path == "/message":
            self.send_html_file("message.html")
        elif pr_url.path == "/read":
            self.read_messages()
        else:
            self.send_error_page()

    def handle_message_submission(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length).decode("utf-8")
        parsed_data = urllib.parse.parse_qs(data)
        data_dict = {
            "username": parsed_data.get("username", [""])[0],
            "message": parsed_data.get("message", [""])[0],
        }
        timestamp = datetime.now().isoformat()
        self.save_to_json(timestamp, data_dict)
        self.send_response(302)
        self.send_header("Location", "/read")
        self.end_headers()

    def save_to_json(self, timestamp, data):
        storage_path = pathlib.Path("storage/data.json")
        storage_path.parent.mkdir(exist_ok=True)
        messages = {}
        if storage_path.exists():
            try:
                with open(storage_path, "r") as file:
                    messages = json.load(file)
            except json.JSONDecodeError:
                self.send_error_page()

        messages[timestamp] = data
        with open(storage_path, "w") as file:
            json.dump(messages, file, indent=4, ensure_ascii=False)

    def read_messages(self):
        storage_path = pathlib.Path("storage/data.json")
        messages = {}
        if storage_path.exists():
            try:
                with open(storage_path, "r") as file:
                    messages = json.load(file)
            except json.JSONDecodeError:
                self.send_error_page()

        content = render_template("read.html", {"messages": messages})
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def send_html_file(self, filename, status=200):
        content = render_template(filename)
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def send_static(self, path):
        static_path = pathlib.Path(path)
        if static_path.exists():
            self.send_response(200)
            mime_type, _ = mimetypes.guess_type(static_path)
            mime_type = mime_type or "application/octet-stream"
            if mime_type.startswith("text/"):
                mime_type += ""
            self.send_header("Content-type", mime_type)
            self.end_headers()
            with open(static_path, "rb") as file:
                self.wfile.write(file.read())
        else:
            self.send_error_page()

    def send_error_page(self):
        content = render_template("error.html")
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))


def run():
    server_address = ("", 3000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Server started on http://localhost:3000")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down the server.")
        httpd.server_close()

    """
    cd my_web_app/src/http_server
    python main.py
    """


if __name__ == "__main__":
    run()
