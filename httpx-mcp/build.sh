#!/bin/bash

set -e

# Install JS deps and build the MCP JS bundle (used by stdio version, harmless here)
npm install >/dev/null 
npm run build >/dev/null 

# Install ProjectDiscovery httpx (Go binary)
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

# Prefer the Go-installed binary explicitly to avoid picking up the Python httpx script
GO_HTTPX_BIN="$(go env GOPATH)/bin/httpx"
if [ -x "$GO_HTTPX_BIN" ]; then
    HTTPX_PATH="$GO_HTTPX_BIN"
else
    # Fallback to PATH lookup
    HTTPX_PATH="$(which httpx)"
fi

SERVICE_PATH=$(pwd)
INDEX_PATH="$SERVICE_PATH/build/index.js"
COMMAND_NAME=$(basename "$SERVICE_PATH")
CONFIG_FILE="$SERVICE_PATH/../mcp-config.json"

[ -f "$CONFIG_FILE" ] || echo "{}" > "$CONFIG_FILE"

jq --arg cmd "$COMMAND_NAME" \
   --arg node_path "$INDEX_PATH" \
   --arg bin_path "$HTTPX_PATH" \
   '.[$cmd] = { "command": "node", "args": [$node_path, $bin_path] }' \
   "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"
