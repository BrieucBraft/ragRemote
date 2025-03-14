FROM python:3.9-slim

WORKDIR /app

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    wget \
    lsb-release \
    apt-transport-https \
    git

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the correct port for Cloud Run
ENV PORT 8080

# Create a directory for models
RUN mkdir -p /root/.ollama/models

# Pull models during build using a background server with proper cleanup
RUN nohup bash -c "ollama serve &" && \
    sleep 10 && \
    ollama pull gemma3 && \
    ollama pull nomic-embed-text && \
    pkill -f "ollama serve" && \
    sleep 2

# Create a startup script to ensure Ollama is running before launching FastAPI
RUN echo '#!/bin/bash\n\
# Start Ollama server in background\n\
ollama serve &\n\
# Wait for Ollama server to be ready\n\
MAX_RETRIES=30\n\
COUNT=0\n\
echo "Waiting for Ollama server to start..."\n\
while ! curl -s http://localhost:11434/api/tags >/dev/null && [ $COUNT -lt $MAX_RETRIES ]; do\n\
  sleep 1\n\
  COUNT=$((COUNT+1))\n\
  echo "Attempt $COUNT/$MAX_RETRIES - Waiting for Ollama server..."\n\
done\n\
if [ $COUNT -eq $MAX_RETRIES ]; then\n\
  echo "Ollama server failed to start within the timeout period"\n\
  exit 1\n\
fi\n\
echo "Ollama server is ready!"\n\
# Run FastAPI with Uvicorn\n\
uvicorn main:app --host 0.0.0.0 --port $PORT --workers 17\n' > /app/start.sh

# Make the script executable
RUN chmod +x /app/start.sh

# Use the script as the entrypoint
CMD ["/app/start.sh"]