FROM node:20-slim

# Install Amass binary and dependencies
RUN set -eux; \
  apt-get update; \
  apt-get install -y --no-install-recommends ca-certificates wget unzip; \
  wget -O /tmp/amass.zip https://github.com/owasp-amass/amass/releases/latest/download/amass_Linux_amd64.zip; \
  unzip /tmp/amass.zip -d /tmp/amass; \
  find /tmp/amass -name amass -type f -exec mv {} /usr/local/bin/amass \; ; \
  chmod +x /usr/local/bin/amass; \
  rm -rf /tmp/amass* /var/lib/apt/lists/*

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
