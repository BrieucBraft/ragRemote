FROM python:3.9-slim

WORKDIR /app

# Install necessary dependencies for Ollama
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Copy your application code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# The port Cloud Run will use
ENV PORT 8080

# Create a startup script to run Ollama and your application
RUN echo '#!/bin/bash\n\
ollama serve & \
sleep 5 && \
ollama pull gemma3:1b & \
sleep 10 && \
uvicorn main:app --host 0.0.0.0 --port $PORT\n' > /app/start.sh

RUN chmod +x /app/start.sh

# Use the startup script as the entrypoint
CMD ["/app/start.sh"]