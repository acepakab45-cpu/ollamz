FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app

COPY . /app

# Install Python deps
RUN pip3 install --no-cache-dir flask requests

EXPOSE 5000

# IMPORTANT: start ollama first, then flask
CMD bash -c "\
ollama serve & \
sleep 5 && \
gunicorn app:app --bind 0.0.0.0:5000"