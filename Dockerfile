# Use a lightweight base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    wget \
    lsb-release \
    apt-transport-https && \
    rm -rf /var/lib/apt/lists/*

# Install Google Cloud SDK (Optional: Only if needed)
RUN curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee /etc/apt/sources.list.d/google-cloud-sdk.list > /dev/null && \
    apt-get update && apt-get install -y google-cloud-cli && \
    rm -rf /var/lib/apt/lists/*

# Set the default Google Cloud project
ENV GOOGLE_CLOUD_PROJECT=ragbraft
RUN gcloud config set project $GOOGLE_CLOUD_PROJECT

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Install Ollama manually (Stable method)
RUN wget https://ollama.com/download/Ollama-linux.tar.gz -O /tmp/Ollama-linux.tar.gz && \
    tar -xzf /tmp/Ollama-linux.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/ollama && \
    rm -f /tmp/Ollama-linux.tar.gz

# Ensure Ollama uses the correct home directory
ENV OLLAMA_HOME=/root/.ollama

# Download models from Cloud Storage (Ensure the bucket & files exist)
RUN mkdir -p /root/.ollama/models && \
    gsutil cp gs://ollama-models-ragbraft/gemma3 /root/.ollama/models/gemma3 && \
    gsutil cp gs://ollama-models-ragbraft/nomic-embed-text /root/.ollama/models/nomic-embed-text && \
    chown -R root:root /root/.ollama

# Expose the correct port for Cloud Run
ENV PORT 8080

# Start Ollama and the FastAPI app
CMD ["sh", "-c", "ollama serve & sleep 5 && uvicorn main:app --host 0.0.0.0 --port $PORT"]
