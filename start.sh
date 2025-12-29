#!/bin/bash

set -e

echo "[*] Starting all services..."

# Loop through all directories in the current folder
for dir in */ ; do
    # Remove trailing slash
    dir=${dir%/}

    # Skip if not a directory
    [ -d "$dir" ] || continue

    # Check if build.sh exists in the directory
    if [ -f "$dir/build.sh" ]; then
        echo "[+] Found build.sh in $dir, executing..."
        chmod +x "$dir/build.sh"
        (cd "$dir" && ./build.sh)
    else
        echo "[-] No build.sh found in $dir, skipping..."
    fi
done

# Normalize mcp-config shape for FastMCP
jq '{mcpServers: with_entries(.value += {dockerContainer: ""})}' mcp-config.json > mcp-config.tmp && mv mcp-config.tmp mcp-config.json

echo "[*] All build scripts executed. Starting FastMCP in HTTP mode so MCP clients can POST to /mcp."

export PORT="${PORT:-10000}"
export HOST="${HOST:-0.0.0.0}"
export MCP_PATH="${MCP_PATH:-/mcp}"

# Run FastMCP with HTTP transport (POST support) instead of SSE
fastmcp serve --config mcp-config.json --transport http --host "$HOST" --port "$PORT" --path "$MCP_PATH"
