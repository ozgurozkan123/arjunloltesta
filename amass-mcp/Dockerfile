FROM node:20-slim

# Install amass and dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    amass \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy package manifests first for layer caching
COPY package.json package-lock.json* tsconfig.json next.config.ts ./

# Install deps
RUN npm install

# Copy source
COPY app ./app
COPY public ./public 2>/dev/null || true

# Build Next.js
RUN npm run build

ENV HOST=0.0.0.0
ENV PORT=3000
EXPOSE 3000

CMD ["npm", "run", "start"]
