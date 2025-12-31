FROM golang:1.22-bookworm AS amass-builder

# Install amass using go install
RUN go install github.com/owasp-amass/amass/v4/...@latest

FROM node:20-slim

# Install required runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy amass binary from builder stage
COPY --from=amass-builder /go/bin/amass /usr/local/bin/amass
RUN chmod +x /usr/local/bin/amass

WORKDIR /app

# Copy package manifests first for layer caching
COPY package.json package-lock.json* tsconfig.json next.config.ts ./

# Install deps
RUN npm install

# Copy source
COPY app ./app
COPY public ./public

# Build Next.js
RUN npm run build

ENV HOST=0.0.0.0
ENV PORT=3000
EXPOSE 3000

CMD ["npm", "run", "start"]
