import os
from fastmcp import FastMCP
from typing import List, Optional

mcp = FastMCP("httpx-mcp")

@mcp.tool()
def httpx(
    target: List[str],
    ports: Optional[List[int]] = None,
    probes: Optional[List[str]] = None,
) -> str:
    """
    Build an httpx command for scanning targets.

    Args:
        target: A list of domains or URLs to scan.
        ports: Optional list of port numbers to probe.
        probes: Optional list of probe flags (e.g., status-code, title, web-server).
    Returns:
        A shell command string the user can run where httpx is installed.
    """
    args = ["-u", ",".join(target), "-silent"]

    if ports:
        args += ["-p", ",".join(str(p) for p in ports)]
    if probes:
        for probe in probes:
            # ensure probe already includes leading dash or not
            flag = probe if probe.startswith("-") else f"-{probe}"
            args.append(flag)

    command = "httpx " + " ".join(args)
    return command

if __name__ == "__main__":
    mcp.run(
        transport="sse",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        path="/mcp",
    )
