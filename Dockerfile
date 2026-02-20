FROM python:3.11-slim

# Install system dependencies and security tools
USER root
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    git \
    nmap \
    masscan \
    sslscan \
    gobuster \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Install Go for Go-based tools
RUN wget -q https://go.dev/dl/go1.22.0.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go1.22.0.linux-amd64.tar.gz \
    && rm go1.22.0.linux-amd64.tar.gz

ENV PATH="/usr/local/go/bin:/root/go/bin:${PATH}"
ENV GOPATH="/root/go"

# Install Go-based security tools
RUN go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest \
    && go install github.com/projectdiscovery/httpx/cmd/httpx@latest \
    && go install github.com/projectdiscovery/katana/cmd/katana@latest \
    && go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest \
    && go install github.com/ffuf/ffuf/v2@latest \
    && go install github.com/tomnomnom/waybackurls@latest

# Install sqlmap
RUN git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git /opt/sqlmap \
    && ln -s /opt/sqlmap/sqlmap.py /usr/local/bin/sqlmap \
    && chmod +x /opt/sqlmap/sqlmap.py

# Install arjun
RUN pip install arjun

# Create wordlists directory
RUN mkdir -p /usr/share/wordlists/dirb \
    && wget -q -O /usr/share/wordlists/dirb/common.txt \
    https://raw.githubusercontent.com/v0re/dirb/master/wordlists/common.txt

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables for proper binding
ENV HOST=0.0.0.0
ENV PYTHONUNBUFFERED=1

# Expose port (Render sets PORT automatically)
EXPOSE 8000

# Run the server
CMD ["python", "server.py"]
