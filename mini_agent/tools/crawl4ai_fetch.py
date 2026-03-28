"""Web Fetch tool for Mini-Agent using Crawl4AI (fallback for Jina Reader)."""

import json
from typing import Any, Dict

from .base import Tool, ToolResult

# Lazy import to avoid loading crawl4ai at startup
_crawl4ai = None


def _get_crawl4ai():
    global _crawl4ai
    if _crawl4ai is None:
        from crawl4ai import AsyncWebCrawler
        _crawl4ai = AsyncWebCrawler()
    return _crawl4ai


class Crawl4AITool(Tool):
    """Fetch and extract content from web pages using Crawl4AI."""

    @property
    def name(self) -> str:
        return "crawl4ai_fetch"

    @property
    def description(self) -> str:
        return """Fallback web fetch tool using Crawl4AI. Use this when web_fetch fails or when you need to handle complex JavaScript-heavy pages. Slower but more powerful than Jina Reader."""

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to fetch"
                }
            },
            "required": ["url"]
        }

    async def execute(self, url: str) -> ToolResult:
        try:
            import asyncio
            crawler = _get_crawl4ai()
            
            # Run in a new event loop since crawl4ai may already have an event loop
            result = await crawler.arun(url=url)
            
            if result.success and result.markdown:
                content = result.markdown
                return ToolResult(success=True, content=content)
            else:
                error_msg = result.error if result.error else "Unknown error"
                return ToolResult(success=False, content="", error=f"Crawl4AI failed: {error_msg}")
                
        except ImportError:
            return ToolResult(success=False, content="", error="crawl4ai not installed")
        except Exception as e:
            return ToolResult(success=False, content="", error=f"Error: {str(e)}")
