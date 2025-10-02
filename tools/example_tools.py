"""
Example tools for the Multi-Agent Research System
"""
from tools.tool_framework import Tool
from typing import Dict, Any
import requests
import urllib.parse


class WebSearchTool(Tool):
    """Tool for performing web searches - example implementation"""
    
    def __init__(self):
        super().__init__(
            tool_id="web-search",
            name="Web Search Tool",
            description="Performs web searches to find relevant information",
            category="information-retrieval"
        )
    
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
                "default": 5,
                "description": "Number of results to return (default: 5)"
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


class DocumentParsingTool(Tool):
    """Tool for parsing documents - example implementation"""
    
    def __init__(self):
        super().__init__(
            tool_id="document-parser",
            name="Document Parsing Tool",
            description="Parses content from various document formats",
            category="processing"
        )
    
    def get_params_definition(self):
        return {
            "file_path": {
                "type": "string",
                "required": True,
                "description": "Path to the document file"
            },
            "format": {
                "type": "string",
                "required": False,
                "default": "txt",
                "description": "Document format (txt, pdf, docx, etc.)"
            }
        }
    
    def execute(self, **params) -> Dict[str, Any]:
        file_path = params.get("file_path", "")
        format_type = params.get("format", "txt")
        
        print(f"Parsing document: '{file_path}' (format: {format_type})")
        
        # Mock response
        return {
            "file_path": file_path,
            "format": format_type,
            "parsed_content": f"This is mock parsed content from {file_path}",
            "metadata": {
                "word_count": 150,
                "page_count": 1,
                "title": f"Mock Title from {file_path}"
            }
        }


class StatisticalAnalysisTool(Tool):
    """Tool for performing statistical analysis - example implementation"""
    
    def __init__(self):
        super().__init__(
            tool_id="statistical-analysis",
            name="Statistical Analysis Tool",
            description="Performs statistical analysis on provided data",
            category="data-analysis"
        )
    
    def get_params_definition(self):
        return {
            "data": {
                "type": "array",
                "required": True,
                "description": "Array of numerical values to analyze"
            },
            "analysis_type": {
                "type": "string",
                "required": False,
                "default": "descriptive",
                "description": "Type of analysis to perform (descriptive, correlation, etc.)"
            }
        }
    
    def execute(self, **params) -> Dict[str, Any]:
        data = params.get("data", [])
        analysis_type = params.get("analysis_type", "descriptive")
        
        print(f"Performing {analysis_type} analysis on data with {len(data)} values")
        
        # Mock statistical analysis
        if data:
            mean_val = sum(data) / len(data)
            min_val = min(data)
            max_val = max(data)
        else:
            mean_val, min_val, max_val = 0, 0, 0
        
        return {
            "analysis_type": analysis_type,
            "input_data": data,
            "statistics": {
                "count": len(data),
                "mean": mean_val,
                "min": min_val,
                "max": max_val,
                "range": max_val - min_val if data else 0
            }
        }