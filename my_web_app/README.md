# Simple HTTP Server build on Python3

A basic HTTP server built with Python 3.10, using Jinja2 for templates. It serves a home page, a message submission form, a message display page, and handles static files. Form data is saved in `storage/data.json`.

## Docker Setup for "my_web_app project"

### Prerequisites
- Docker installed (I’m using an archived version for macOS Catalina: v. 20.10.21, build baeda1f).
- Project files in `src/http_server/` (`main.py`, `jinja2_env.py`, `templates/`, `static/`).

### Create requirements.txt
Generate dependencies:
- cd src/http_server
- pip freeze > requirements.txt

### Build the Docker Image
- cd my_web_app
- docker build -t simple-http-server .

### Run with Docker Compose
- docker-compose up -d

- Opens at http://localhost:3000.

- Stop: docker-compose down.

### Remove volume:
- docker volume rm http_server_data
