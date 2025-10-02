"""
Web Search Tool for the Multi-Agent Research System
"""
from tools.tool_framework import Tool
from tools.config.tool_config import ToolConfig, DEFAULT_CONFIGS
from typing import Dict, Any


class WebSearchTool(Tool):
    """Tool for performing web searches - example implementation"""
    
    def __init__(self):
        super().__init__(
            tool_id="web-search",
            name="Web Search Tool",
            description="Performs web searches to find relevant information",
            category="information-retrieval"
        )
        self.config = ToolConfig("web_search_tool")
        # Use default config if no specific config is set
        for key, value in DEFAULT_CONFIGS["web_search_tool"].items():
            if self.config.get(key) is None:
                self.config.set(key, value)
    
    def get_params_definition(self):
        return {
            "query": {
                "type": "string",
                "required": True,
                "description": "Search query string"
            },
            "num_results": {
                "type": "integer", 
                "required": False,
                "default": self.config.get("default_num_results", 5),
                "description": f"Number of results to return (default: {self.config.get('default_num_results', 5)})"
            }
        }
    
    def execute(self, **params) -> Dict[str, Any]:
        # This is a mock implementation - in a real system, you'd connect to a search API
        query = params.get("query", "")
        num_results = params.get("num_results", 5)
        
        # Mock response
        print(f"Performing web search for: '{query}' (limit: {num_results} results)")
        
        mock_results = []
        for i in range(min(num_results, 3)):  # Limit to 3 for demo
            mock_results.append({
                "title": f"Mock Result {i+1} for {query}",
                "url": f"https://example.com/result{i+1}",
                "snippet": f"This is a mock snippet for the search result {i+1} related to {query}..."
            })
        
        return {
            "query": query,
            "results": mock_results,
            "num_results_returned": len(mock_results)
        }