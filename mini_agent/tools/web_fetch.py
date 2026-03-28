"""Web Fetch tool for Mini-Agent using Jina Reader."""

import json
from typing import Any, Dict

import httpx

from .base import Tool, ToolResult


class WebFetchTool(Tool):
    """Fetch and extract content from web pages using Jina Reader."""

    @property
    def name(self) -> str:
        return "web_fetch"

    @property
    def description(self) -> str:
        return """Fetch and extract readable content from a URL. Use this to get detailed information from web pages, articles, or documents. Returns the page content in clean text/markdown format."""

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to fetch"
                },
                "max_chars": {
                    "type": "integer",
                    "description": "Maximum characters to return (default: 10000)",
                    "default": 10000
                }
            },
            "required": ["url"]
        }

    async def execute(self, url: str, max_chars: int = 10000) -> ToolResult:
        try:
            # Use Jina Reader API
            fetch_url = f"https://r.jina.ai/{url}"
            
            async with httpx.AsyncClient(timeout=30.0, proxy="http://127.0.0.1:7890") as client:
                response = await client.get(fetch_url)
                response.raise_for_status()
                
                content = response.text
                
                # Truncate if too long
                if len(content) > max_chars:
                    content = content[:max_chars] + f"\n\n...[truncated, total {len(content)} chars]"
                
                return ToolResult(success=True, content=content)
                
        except httpx.HTTPError as e:
            return ToolResult(success=False, content="", error=f"HTTP error: {str(e)}")
        except Exception as e:
            return ToolResult(success=False, content="", error=f"Error: {str(e)}")
