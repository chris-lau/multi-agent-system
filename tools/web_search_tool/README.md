# Web Search Tool

The Web Search Tool enables agents to perform web searches to find relevant information on various topics.

## Overview
This tool provides web search capabilities to agents in the Multi-Agent Research System. It allows agents to search the web for information relevant to their research tasks.

## Parameters
- `query` (string, required): The search query string
- `num_results` (integer, optional, default: 5): Number of results to return

## Output
The tool returns a structured response with:
- `query`: The original search query
- `results`: Array of search results, each containing title, URL, and snippet
- `num_results_returned`: The number of results actually returned

## Usage Example
```json
{
  "query": "AI in healthcare",
  "num_results": 3
}
```

## Note
This is currently a mock implementation. In a real system, this would connect to a search API like Tavily or DuckDuckGo.