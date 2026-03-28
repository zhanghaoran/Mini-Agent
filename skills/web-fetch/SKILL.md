---
name: web-fetch
description: Fetch and extract readable content from web pages using Jina Reader API. Use when you need to get detailed content from a specific URL.
---

# Web Fetch Tool

Fetch and extract readable content from web pages using Jina Reader API.

## Quick Start

### Fetch a URL
```bash
python3 ~/.openclaw/workspace/bin/web_fetch.py <URL> [max_chars]

# Examples:
python3 ~/.openclaw/workspace/bin/web_fetch.py "https://example.com"
python3 ~/.openclaw/workspace/bin/web_fetch.py "https://github.com" 2000
python3 ~/.openclaw/workspace/bin/web_fetch.py "example.com" 500
```

## Parameters

- **URL** (required): The URL to fetch. Can include or omit `https://`
- **max_chars** (optional): Maximum characters to return. Default: 10000

## Return Format

The tool returns markdown-formatted content with:
- Title
- URL Source
- Published Time (if available)
- Markdown Content

## Error Handling

- 503 errors: Jina Reader service temporarily unavailable. Try again later.
- Connection errors: Check proxy settings (currently using 127.0.0.1:7890)

## Use Cases

1. **Get detailed page content** - When search results aren't enough
2. **Read documentation** - Fetch technical docs
3. **Extract article content** - Get full article text
4. **Research** - Gather detailed information from specific sources

## Notes

- Uses Jina Reader API (https://r.jina.ai/)
- Automatically adds https:// if no protocol specified
- Proxy: http://127.0.0.1:7890 (sing-box)
- Supports any publicly accessible URL
