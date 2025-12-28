FROM node:20-slim

# Install Amass and essentials
RUN apt-get update && apt-get install -y --no-install-recommends \
    amass \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy entire project (we only use amass-mcp subdir)
COPY . .

# Work inside the amass-mcp Next.js app
WORKDIR /app/amass-mcp

# Install dependencies
RUN npm install

# Build Next.js app
RUN npm run build

ENV HOST=0.0.0.0
ENV PORT=3000
EXPOSE 3000

CMD ["npm", "run", "start"]
