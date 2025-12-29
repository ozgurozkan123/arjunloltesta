# httpx-mcp (FastMCP / Render-ready)

## What changed
- Replaced the Node/stdio implementation with a lightweight FastMCP SSE server (`server.py`).
- Binds to `0.0.0.0` and uses the `PORT` environment variable (Render sets this) with path `/mcp`.
- Returns the `httpx` command string to run where the binary is available (no CLI execution inside the container).
- Added minimal `requirements.txt` and `Dockerfile` scoped to the `httpx-mcp` folder for Render deployments.

## Run locally
```bash
cd httpx-mcp
pip install -r requirements.txt
python server.py  # listens on http://0.0.0.0:8000/mcp (SSE transport)
```

## Deploy to Render (Web Service)
- **Root Directory:** `httpx-mcp`
- **Dockerfile Path:** `httpx-mcp/Dockerfile`
- **Port:** leave default; the server reads `$PORT` automatically.
- **Health check:** use `/` or `/mcp`; FastMCP returns 404 on `/` which Render accepts as long as the port is bound.

The MCP endpoint will be available at `https://<your-render-service>.onrender.com/mcp`.
