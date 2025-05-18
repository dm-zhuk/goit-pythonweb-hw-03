# Dockerfile for the HTTP server
FROM python:3.10-slim

# Set the working directory to app
WORKDIR /app

# Copy everything from my project folder
COPY ./src/http_server/ .

# Install dependencies from requirements.txt
RUN pip install -r requirements.txt

# That's what main.py uses
EXPOSE 3000

# Create storage folder for data.json if not exists
RUN mkdir -p storage

# Start the server with main.py
CMD ["python", "main.py"]