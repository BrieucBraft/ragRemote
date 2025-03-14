# Use python slim as the base image
FROM python:3.9-slim

# Set the working directory
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

# Install the Google Cloud SDK
RUN curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee /etc/apt/sources.list.d/google-cloud-sdk.list && \
    apt-get update && apt-get install -y google-cloud-sdk

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Verify gcloud installation
RUN gcloud --version

# Set the default project
ENV GOOGLE_CLOUD_PROJECT=ragbraft
RUN gcloud config set project $GOOGLE_CLOUD_PROJECT

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure Ollama uses the correct home directory
ENV OLLAMA_HOME=/root/.ollama

# Download models from Cloud Storage
RUN mkdir -p /root/.ollama/models && \
    gsutil cp gs://ollama-models-ragbraft/gemma3 /root/.ollama/models/gemma3 && \
    gsutil cp gs://ollama-models-ragbraft/nomic-embed-text /root/.ollama/models/nomic-embed-text && \
    chown -R root:root /root/.ollama

# Expose the correct port for Cloud Run
ENV PORT 8080

# Start Ollama and the FastAPI app
CMD ["sh", "-c", "ollama serve & sleep 5 && uvicorn main:app --host 0.0.0.0 --port $PORT"]