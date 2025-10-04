"""
Unit tests for document_parser_tool.py to improve test coverage
"""
import sys
import os
from unittest.mock import Mock, patch
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.document_parser_tool.document_parser_tool import DocumentParsingTool


class TestDocumentParsingTool:
    """Test cases for DocumentParsingTool class"""
    
    def test_init(self):
        """Test DocumentParsingTool initialization"""
        tool = DocumentParsingTool()
        
        assert tool.tool_id == "document-parser"
        assert tool.name == "Document Parsing Tool"
        assert tool.description == "Parses content from various document formats"
        assert tool.category == "processing"
        assert tool.config is not None
    
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
        assert "enum" in params_def["format"]
    
    def test_get_params_definition_with_custom_formats(self):
        """Test parameter definition with custom supported formats from config"""
        tool = DocumentParsingTool()
        # Manually set a custom config value to test the format
        tool.config.set("supported_formats", ["pdf", "docx", "txt"])
        
        params_def = tool.get_params_definition()
        assert params_def["format"]["enum"] == ["pdf", "docx", "txt"]
        assert "pdf, docx, txt" in params_def["format"]["description"]
    
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
    
    @patch('builtins.print')
    def test_execute_with_minimal_params(self, mock_print):
        """Test execution with minimal parameters (only required ones)"""
        tool = DocumentParsingTool()
        result = tool.execute(file_path="/minimal/path")
        
        # Verify print was called
        mock_print.assert_called_once_with("Parsing document: '/minimal/path' (format: txt)")
        
        # Verify result structure
        assert result["file_path"] == "/minimal/path"
        assert result["format"] == "txt"
        assert "parsed_content" in result