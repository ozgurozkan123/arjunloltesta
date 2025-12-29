import os
import subprocess
from fastmcp import FastMCP
from typing import List, Optional

mcp = FastMCP("httpx-mcp")

HTTPX_BIN = os.getenv("HTTPX_BIN", "httpx")

@mcp.tool()
def httpx(
    target: List[str],
    ports: Optional[List[int]] = None,
    probes: Optional[List[str]] = None,
) -> str:
    """
    Run ProjectDiscovery httpx against target(s) and return the raw output.

    Args:
        target: List of domains/URLs to scan.
        ports: Optional list of ports to probe.
        probes: Optional list of probe flags (e.g., status-code, title, web-server).
    Returns:
        Command output (stdout or stderr) from httpx.
    """
    args = ["-u", ",".join(target), "-silent"]

    if ports:
        args += ["-p", ",".join(str(p) for p in ports)]
    if probes:
        for probe in probes:
            flag = probe if probe.startswith("-") else f"-{probe}"
            args.append(flag)

    cmd = [HTTPX_BIN] + args

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            timeout=300,
        )
        output = result.stdout.strip()
        if result.returncode != 0:
            output = (output + "\n" + result.stderr.strip()).strip()
            return f"httpx exited with code {result.returncode}:\n{output}"
        return output or "(no output)"
    except FileNotFoundError:
        return "httpx binary not found. Ensure the ProjectDiscovery httpx CLI is installed in the container."
    except subprocess.TimeoutExpired:
        return "httpx timed out. Try reducing targets or probes."

if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        path="/mcp",
    )
