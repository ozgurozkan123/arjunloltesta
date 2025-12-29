FROM python:3.11-slim

# Install system dependencies and Go toolchain
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    git \
    golang \
    build-essential \
    jq \
  && rm -rf /var/lib/apt/lists/*

# Make sure the Go bin directory is in PATH
ENV PATH="/root/go/bin:${PATH}"

# Install ProjectDiscovery httpx (Go CLI)
RUN go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py ./

ENV HOST=0.0.0.0
ENV PORT=8000
# Expose MCP port
EXPOSE 8000

CMD ["python", "server.py"]
