"""Brave Search tool for Mini-Agent."""

import json
from typing import Any, Dict

import httpx

from .base import Tool, ToolResult


class BraveSearchTool(Tool):
    """Brave Search LLM Context API tool."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    @property
    def name(self) -> str:
        return "brave_search"

    @property
    def description(self) -> str:
        return """Search the web using Brave Search LLM Context API. Returns comprehensive results with sources and snippets. Use this for research, fact-checking, and gathering current information."""

    @property
    def parameters(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                },
                "count": {
                    "type": "integer",
                    "description": "Number of results to return (default: 10)",
                    "default": 10
                }
            },
            "required": ["query"]
        }

    async def execute(self, query: str, count: int = 10) -> ToolResult:
        try:
            url = "https://api.search.brave.com/res/v1/llm/context"
            headers = {
                "X-Subscription-Token": self.api_key
            }
            params = {
                "q": query,
                "count": count
            }

            async with httpx.AsyncClient(timeout=30.0, proxy="http://127.0.0.1:7890") as client:
                response = await client.get(url, headers=headers, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                # Format results nicely
                results = self._format_results(data)
                return ToolResult(success=True, content=results)
                
        except httpx.HTTPError as e:
            return ToolResult(success=False, content="", error=f"HTTP error: {str(e)}")
        except Exception as e:
            return ToolResult(success=False, content="", error=f"Error: {str(e)}")

    def _format_results(self, data: dict) -> str:
        """Format Brave Search results into readable text."""
        try:
            results_text = f"🔍 Search Results for query\n\n"
            
            # Get grounding results
            generic = data.get("grounding", {}).get("generic", [])
            
            for i, item in enumerate(generic, 1):
                title = item.get("title", "Untitled")
                url = item.get("url", "")
                snippets = item.get("snippets", [])
                
                results_text += f"### {i}. {title}\n"
                results_text += f"🔗 {url}\n\n"
                
                for snippet in snippets[:2]:  # Max 2 snippets per result
                    results_text += f"> {snippet}\n"
                results_text += "\n"
            
            if not generic:
                results_text += "No results found.\n"
                
            return results_text
            
        except Exception as e:
            # Return raw JSON if parsing fails
            return json.dumps(data, indent=2, ensure_ascii=False)
