#!/usr/bin/env python3
"""
Web Fetch Tool - Uses Jina Reader API
Usage: python web_fetch.py <url> [max_chars]
"""

import sys
import requests

PROXY = "http://127.0.0.1:7890"

def fetch(url: str, max_chars: int = 10000) -> str:
    # Add https:// if no protocol specified
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"
    
    # Use Jina Reader API
    fetch_url = f"https://r.jina.ai/{url}"
    
    try:
        response = requests.get(fetch_url, proxies={"http": PROXY, "https": PROXY}, timeout=30)
        response.raise_for_status()
        
        content = response.text
        if len(content) > max_chars:
            content = content[:max_chars] + f"\n\n...[truncated, total {len(content)} chars]"
        
        return content
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python web_fetch.py <url> [max_chars]")
        sys.exit(1)
    
    url = sys.argv[1]
    max_chars = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
    
    print(fetch(url, max_chars))
