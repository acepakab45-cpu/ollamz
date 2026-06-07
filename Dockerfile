FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# System dependencies (ADD zstd HERE)
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    ca-certificates \
    zstd \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app

COPY . /app

# Install Python dependencies
RUN pip3 install --no-cache-dir flask requests gunicorn

EXPOSE 5000

# Start Ollama + Flask
CMD bash -c "ollama serve & sleep 5 && gunicorn app:app --bind 0.0.0.0:5000"
