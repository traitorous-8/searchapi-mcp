# searchapi-mcp

MCP server exposing SearchApi.io real-time SERP data (Google, Shopping, Jobs, YouTube, and 100+ engines) as tools for AI agents.

## Tools

| Tool | Engine | Parameters | Description |
| --- | --- | --- | --- |
| `search` | Any | `engine`, `query`, `num`, `location`, `gl`, `hl` | Search using any supported SearchApi.io engine |
| `google_search` | `google` | `query`, `num`, `location`, `gl`, `hl` | Google Web Search |
| `google_shopping` | `google_shopping` | `query`, `num`, `gl`, `hl` | Google Shopping Search |
| `google_jobs` | `google_jobs` | `query`, `location`, `hl` | Google Jobs Search |
| `youtube_search` | `youtube` | `query`, `hl`, `gl` | YouTube Search |

## Setup

1. Install the dependencies:

```bash
pip install mcp httpx
```

2. Set the `SEARCHAPI_API_KEY` environment variable with your API key from [SearchApi.io](https://www.searchapi.io/):

```bash
export SEARCHAPI_API_KEY="your-searchapi-api-key"
```

## How to Run

To start the MCP server directly:

```bash
python server.py
```

## Claude Desktop Configuration

To configure SearchApi MCP in Claude Desktop, add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "searchapi": {
      "command": "python",
      "args": [
        "/path/to/searchapi-mcp/server.py"
      ],
      "env": {
        "SEARCHAPI_API_KEY": "your-searchapi-api-key"
      }
    }
  }
}
```
