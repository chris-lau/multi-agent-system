"""
Unit tests for example_tools.py to improve test coverage
"""
import sys
import os
from unittest.mock import Mock, patch
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.example_tools import WebSearchTool, DocumentParsingTool, StatisticalAnalysisTool


class TestWebSearchTool:
    """Test cases for WebSearchTool class"""
    
    def test_init(self):
        """Test WebSearchTool initialization"""
        tool = WebSearchTool()
        
        assert tool.tool_id == "web-search"
        assert tool.name == "Web Search Tool"
        assert tool.description == "Performs web searches to find relevant information"
        assert tool.category == "information-retrieval"
    
    def test_get_params_definition(self):
        """Test parameter definition for WebSearchTool"""
        tool = WebSearchTool()
        params_def = tool.get_params_definition()
        
        assert "query" in params_def
        assert params_def["query"]["type"] == "string"
        assert params_def["query"]["required"] == True
        assert "num_results" in params_def
        assert params_def["num_results"]["type"] == "integer"
        assert params_def["num_results"]["required"] == False
        assert params_def["num_results"]["default"] == 5
    
    @patch('builtins.print')
    def test_execute(self, mock_print):
        """Test execution of WebSearchTool"""
        tool = WebSearchTool()
        result = tool.execute(query="test query", num_results=2)
        
        # Verify print was called
        mock_print.assert_called_once_with("Performing web search for: 'test query' (limit: 2 results)")
        
        # Verify result structure
        assert "query" in result
        assert result["query"] == "test query"
        assert "results" in result
        assert "num_results_returned" in result
        assert result["num_results_returned"] == 2  # We limited to 2 results
        assert len(result["results"]) == 2
        
        # Check each result has required fields
        for res in result["results"]:
            assert "title" in res
            assert "url" in res
            assert "snippet" in res
    
    @patch('builtins.print')
    def test_execute_with_default_params(self, mock_print):
        """Test execution of WebSearchTool with default parameters"""
        tool = WebSearchTool()
        result = tool.execute(query="test query")
        
        # Verify print was called
        mock_print.assert_called_once_with("Performing web search for: 'test query' (limit: 5 results)")
        
        # Verify result structure
        assert result["query"] == "test query"
        assert result["num_results_returned"] <= 3  # Limited to 3 in mock implementation


class TestDocumentParsingTool:
    """Test cases for DocumentParsingTool class"""
    
    def test_init(self):
        """Test DocumentParsingTool initialization"""
        tool = DocumentParsingTool()
        
        assert tool.tool_id == "document-parser"
        assert tool.name == "Document Parsing Tool"
        assert tool.description == "Parses content from various document formats"
        assert tool.category == "processing"
    
    def test_get_params_definition(self):
        """Test parameter definition for DocumentParsingTool"""
        tool = DocumentParsingTool()
        params_def = tool.get_params_definition()
        
        assert "file_path" in params_def
        assert params_def["file_path"]["type"] == "string"
        assert params_def["file_path"]["required"] == True
        assert "format" in params_def
        assert params_def["format"]["type"] == "string"
        assert params_def["format"]["required"] == False
        assert params_def["format"]["default"] == "txt"
    
    @patch('builtins.print')
    def test_execute(self, mock_print):
        """Test execution of DocumentParsingTool"""
        tool = DocumentParsingTool()
        result = tool.execute(file_path="/path/to/doc.pdf", format="pdf")
        
        # Verify print was called
        mock_print.assert_called_once_with("Parsing document: '/path/to/doc.pdf' (format: pdf)")
        
        # Verify result structure
        assert result["file_path"] == "/path/to/doc.pdf"
        assert result["format"] == "pdf"
        assert "parsed_content" in result
        assert "metadata" in result
        assert result["metadata"]["word_count"] == 150
        assert result["metadata"]["page_count"] == 1
        assert result["metadata"]["title"] == "Mock Title from /path/to/doc.pdf"
    
    @patch('builtins.print')
    def test_execute_with_default_format(self, mock_print):
        """Test execution of DocumentParsingTool with default format"""
        tool = DocumentParsingTool()
        result = tool.execute(file_path="/path/to/doc.txt")
        
        # Verify print was called with default format
        mock_print.assert_called_once_with("Parsing document: '/path/to/doc.txt' (format: txt)")
        
        # Verify result structure
        assert result["format"] == "txt"


class TestStatisticalAnalysisTool:
    """Test cases for StatisticalAnalysisTool class"""
    
    def test_init(self):
        """Test StatisticalAnalysisTool initialization"""
        tool = StatisticalAnalysisTool()
        
        assert tool.tool_id == "statistical-analysis"
        assert tool.name == "Statistical Analysis Tool"
        assert tool.description == "Performs statistical analysis on provided data"
        assert tool.category == "data-analysis"
    
    def test_get_params_definition(self):
        """Test parameter definition for StatisticalAnalysisTool"""
        tool = StatisticalAnalysisTool()
        params_def = tool.get_params_definition()
        
        assert "data" in params_def
        assert params_def["data"]["type"] == "array"
        assert params_def["data"]["required"] == True
        assert "analysis_type" in params_def
        assert params_def["analysis_type"]["type"] == "string"
        assert params_def["analysis_type"]["required"] == False
        assert params_def["analysis_type"]["default"] == "descriptive"
    
    @patch('builtins.print')
    def test_execute(self, mock_print):
        """Test execution of StatisticalAnalysisTool with data"""
        tool = StatisticalAnalysisTool()
        data = [1, 2, 3, 4, 5]
        result = tool.execute(data=data, analysis_type="descriptive")
        
        # Verify print was called
        mock_print.assert_called_once_with(f"Performing descriptive analysis on data with {len(data)} values")
        
        # Verify result structure
        assert result["analysis_type"] == "descriptive"
        assert result["input_data"] == data
        assert "statistics" in result
        
        stats = result["statistics"]
        assert stats["count"] == 5
        assert stats["mean"] == 3.0  # (1+2+3+4+5)/5
        assert stats["min"] == 1
        assert stats["max"] == 5
        assert stats["range"] == 4  # 5-1
    
    @patch('builtins.print')
    def test_execute_empty_data(self, mock_print):
        """Test execution of StatisticalAnalysisTool with empty data"""
        tool = StatisticalAnalysisTool()
        data = []
        result = tool.execute(data=data)
        
        # Verify print was called
        mock_print.assert_called_once_with("Performing descriptive analysis on data with 0 values")
        
        # Verify result structure
        stats = result["statistics"]
        assert stats["count"] == 0
        assert stats["mean"] == 0
        assert stats["min"] == 0
        assert stats["max"] == 0
        assert stats["range"] == 0