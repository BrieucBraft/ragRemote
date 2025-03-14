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

# Pull the required models during the build process
RUN ollama serve && sleep 10 && ollama pull gemma3 && ollama pull nomic-embed-text


# Create a startup script to ensure Ollama is running before launching FastAPI
RUN echo '#!/bin/bash\n\
# Start Ollama server in background\n\
ollama serve &\n\
# Run FastAPI with Uvicorn\n\
uvicorn main:app --host 0.0.0.0 --port $PORT --workers 17\n' > /app/start.sh

# Make the script executable
RUN chmod +x /app/start.sh

# Use the script as the entrypoint
CMD ["/app/start.sh"]
