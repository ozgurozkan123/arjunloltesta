"""
MCP for Security - Security Tools MCP Server
A comprehensive MCP server providing access to popular security tools
for penetration testing and vulnerability assessment.
"""

import os
import subprocess
import json
from typing import Optional
from fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("security-tools-mcp")

def run_command(command: list, timeout: int = 300) -> str:
    """Execute a command and return its output."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        output = result.stdout
        if result.stderr:
            output += "\n" + result.stderr
        return output if output else "Command completed with no output"
    except subprocess.TimeoutExpired:
        return f"Command timed out after {timeout} seconds"
    except FileNotFoundError:
        return f"Tool not found: {command[0]}. Make sure it's installed."
    except Exception as e:
        return f"Error executing command: {str(e)}"


@mcp.tool()
def do_nmap(target: str, nmap_args: Optional[str] = None) -> str:
    """
    Run nmap network scanner to detect open ports and services.
    
    Args:
        target: Target IP address or hostname to scan
        nmap_args: Additional nmap arguments (e.g., "-sV -sC -p 1-1000")
    """
    cmd = ["nmap"]
    if nmap_args:
        cmd.extend(nmap_args.split())
    cmd.append(target)
    return run_command(cmd)


@mcp.tool()
def do_masscan(target: str, ports: str = "1-65535", rate: int = 1000) -> str:
    """
    Run masscan for fast port scanning.
    
    Args:
        target: Target IP address or CIDR range (e.g., "192.168.1.0/24")
        ports: Port range to scan (default: "1-65535")
        rate: Packet rate per second (default: 1000)
    """
    cmd = ["masscan", target, "-p", ports, "--rate", str(rate)]
    return run_command(cmd)


@mcp.tool()
def do_sqlmap(url: str, sqlmap_args: Optional[str] = None) -> str:
    """
    Run sqlmap for SQL injection detection and exploitation.
    
    Args:
        url: Target URL with parameter (e.g., "http://example.com/page?id=1")
        sqlmap_args: Additional sqlmap arguments (e.g., "--dbs --batch --level=3")
    """
    cmd = ["sqlmap", "-u", url, "--batch"]
    if sqlmap_args:
        cmd.extend(sqlmap_args.split())
    return run_command(cmd, timeout=600)


@mcp.tool()
def do_ffuf(url: str, wordlist: str = "/usr/share/wordlists/dirb/common.txt", ffuf_args: Optional[str] = None) -> str:
    """
    Run ffuf for web fuzzing and directory/file discovery.
    
    Args:
        url: Target URL with FUZZ keyword (e.g., "http://example.com/FUZZ")
        wordlist: Path to wordlist file
        ffuf_args: Additional ffuf arguments (e.g., "-mc 200,301 -t 50")
    """
    cmd = ["ffuf", "-u", url, "-w", wordlist]
    if ffuf_args:
        cmd.extend(ffuf_args.split())
    return run_command(cmd, timeout=600)


@mcp.tool()
def do_nuclei(url: str, tags: Optional[str] = None, severity: Optional[str] = None) -> str:
    """
    Run nuclei vulnerability scanner with templates.
    
    Args:
        url: Target URL to scan
        tags: Comma-separated tags to filter templates (e.g., "cve,rce,sqli")
        severity: Filter by severity (e.g., "critical,high,medium")
    """
    cmd = ["nuclei", "-u", url, "-silent"]
    if tags:
        cmd.extend(["-tags", tags])
    if severity:
        cmd.extend(["-severity", severity])
    return run_command(cmd, timeout=600)


@mcp.tool()
def get_nuclei_tags() -> str:
    """
    Get available Nuclei template tags from the official repository.
    """
    import urllib.request
    try:
        url = "https://raw.githubusercontent.com/projectdiscovery/nuclei-templates/main/TEMPLATES-STATS.json"
        with urllib.request.urlopen(url, timeout=30) as response:
            data = json.loads(response.read().decode())
            tags = [tag["name"] for tag in data.get("tags", [])]
            return json.dumps(tags[:100], indent=2)  # Return top 100 tags
    except Exception as e:
        return f"Error fetching tags: {str(e)}"


@mcp.tool()
def do_httpx(targets: str, httpx_args: Optional[str] = None) -> str:
    """
    Run httpx for HTTP probing and technology detection.
    
    Args:
        targets: Target URL(s) or domain(s), comma-separated
        httpx_args: Additional httpx arguments (e.g., "-status-code -title -tech-detect")
    """
    cmd = ["httpx"]
    if httpx_args:
        cmd.extend(httpx_args.split())
    # Pass targets via stdin simulation with echo
    target_list = targets.replace(",", "\n")
    try:
        result = subprocess.run(
            cmd,
            input=target_list,
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.stdout + result.stderr if result.stdout or result.stderr else "No results"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def do_katana(url: str, depth: int = 2, katana_args: Optional[str] = None) -> str:
    """
    Run katana web crawler for endpoint discovery.
    
    Args:
        url: Target URL to crawl
        depth: Crawling depth (default: 2)
        katana_args: Additional katana arguments (e.g., "-jc -ef png,jpg")
    """
    cmd = ["katana", "-u", url, "-d", str(depth), "-silent"]
    if katana_args:
        cmd.extend(katana_args.split())
    return run_command(cmd, timeout=300)


@mcp.tool()
def do_subfinder(domain: str, subfinder_args: Optional[str] = None) -> str:
    """
    Run subfinder for subdomain enumeration.
    
    Args:
        domain: Target domain (e.g., "example.com")
        subfinder_args: Additional subfinder arguments (e.g., "-recursive -all")
    """
    cmd = ["subfinder", "-d", domain, "-silent"]
    if subfinder_args:
        cmd.extend(subfinder_args.split())
    return run_command(cmd, timeout=300)


@mcp.tool()
def do_amass(domain: str, amass_args: Optional[str] = None) -> str:
    """
    Run amass for in-depth subdomain enumeration and attack surface mapping.
    
    Args:
        domain: Target domain (e.g., "example.com")
        amass_args: Additional amass arguments (e.g., "-passive -timeout 10")
    """
    cmd = ["amass", "enum", "-d", domain]
    if amass_args:
        cmd.extend(amass_args.split())
    return run_command(cmd, timeout=600)


@mcp.tool()
def do_sslscan(target: str) -> str:
    """
    Run sslscan for SSL/TLS configuration analysis.
    
    Args:
        target: Target hostname:port (e.g., "example.com:443")
    """
    cmd = ["sslscan", target]
    return run_command(cmd)


@mcp.tool()
def do_waybackurls(domain: str) -> str:
    """
    Fetch historical URLs from the Wayback Machine.
    
    Args:
        domain: Target domain to search (e.g., "example.com")
    """
    cmd = ["waybackurls", domain]
    return run_command(cmd, timeout=120)


@mcp.tool()
def do_arjun(url: str, arjun_args: Optional[str] = None) -> str:
    """
    Run arjun for HTTP parameter discovery.
    
    Args:
        url: Target URL to scan
        arjun_args: Additional arjun arguments (e.g., "-m POST --stable")
    """
    cmd = ["arjun", "-u", url]
    if arjun_args:
        cmd.extend(arjun_args.split())
    return run_command(cmd, timeout=300)


@mcp.tool()
def do_wpscan(url: str, wpscan_args: Optional[str] = None) -> str:
    """
    Run wpscan for WordPress vulnerability scanning.
    
    Args:
        url: Target WordPress URL
        wpscan_args: Additional wpscan arguments (e.g., "--enumerate vp,vt,u")
    """
    cmd = ["wpscan", "--url", url, "--no-banner"]
    if wpscan_args:
        cmd.extend(wpscan_args.split())
    return run_command(cmd, timeout=600)


@mcp.tool()
def do_crtsh(domain: str) -> str:
    """
    Query crt.sh for SSL certificate transparency logs to find subdomains.
    
    Args:
        domain: Target domain (e.g., "example.com")
    """
    import urllib.request
    import urllib.parse
    try:
        url = f"https://crt.sh/?q=%.{urllib.parse.quote(domain)}&output=json"
        with urllib.request.urlopen(url, timeout=60) as response:
            data = json.loads(response.read().decode())
            domains = list(set([entry.get("name_value", "").replace("*.", "") for entry in data]))
            return "\n".join(sorted(domains))
    except Exception as e:
        return f"Error querying crt.sh: {str(e)}"


@mcp.tool()
def do_gobuster(url: str, mode: str = "dir", wordlist: str = "/usr/share/wordlists/dirb/common.txt", gobuster_args: Optional[str] = None) -> str:
    """
    Run gobuster for directory/DNS/vhost brute-forcing.
    
    Args:
        url: Target URL
        mode: Scan mode - dir, dns, vhost (default: "dir")
        wordlist: Path to wordlist
        gobuster_args: Additional gobuster arguments
    """
    cmd = ["gobuster", mode, "-u", url, "-w", wordlist]
    if gobuster_args:
        cmd.extend(gobuster_args.split())
    return run_command(cmd, timeout=600)


@mcp.tool()
def check_http_headers(url: str) -> str:
    """
    Check HTTP security headers for a given URL.
    
    Args:
        url: Target URL to check
    """
    import urllib.request
    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0 (Security Header Check)')
        with urllib.request.urlopen(req, timeout=30) as response:
            headers = dict(response.headers)
            
            security_headers = [
                "Strict-Transport-Security",
                "Content-Security-Policy",
                "X-Frame-Options",
                "X-Content-Type-Options",
                "X-XSS-Protection",
                "Referrer-Policy",
                "Permissions-Policy",
                "Cross-Origin-Opener-Policy",
                "Cross-Origin-Resource-Policy"
            ]
            
            result = ["=== HTTP Security Headers Analysis ===\n"]
            for header in security_headers:
                value = headers.get(header)
                if value:
                    result.append(f"✓ {header}: {value}")
                else:
                    result.append(f"✗ {header}: MISSING")
            
            return "\n".join(result)
    except Exception as e:
        return f"Error checking headers: {str(e)}"


@mcp.tool()
def list_available_tools() -> str:
    """
    List all available security tools in this MCP server.
    """
    tools = [
        ("do_nmap", "Network port scanning and service detection"),
        ("do_masscan", "Fast port scanning for large networks"),
        ("do_sqlmap", "SQL injection detection and exploitation"),
        ("do_ffuf", "Web fuzzing and directory discovery"),
        ("do_nuclei", "Vulnerability scanning with templates"),
        ("get_nuclei_tags", "Get available Nuclei template tags"),
        ("do_httpx", "HTTP probing and tech detection"),
        ("do_katana", "Web crawling and endpoint discovery"),
        ("do_subfinder", "Subdomain enumeration"),
        ("do_amass", "Attack surface mapping"),
        ("do_sslscan", "SSL/TLS configuration analysis"),
        ("do_waybackurls", "Historical URL discovery"),
        ("do_arjun", "HTTP parameter discovery"),
        ("do_wpscan", "WordPress vulnerability scanning"),
        ("do_crtsh", "Certificate transparency lookup"),
        ("do_gobuster", "Directory/DNS brute-forcing"),
        ("check_http_headers", "HTTP security headers analysis"),
    ]
    
    result = ["=== Available Security Tools ===\n"]
    for name, description in tools:
        result.append(f"• {name}: {description}")
    
    return "\n".join(result)


# Run the server
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=port,
        path="/mcp"
    )
