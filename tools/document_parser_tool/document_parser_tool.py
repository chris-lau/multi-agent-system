"""
Document Parsing Tool for the Multi-Agent Research System
"""
from tools.tool_framework import Tool
from tools.config.tool_config import ToolConfig, DEFAULT_CONFIGS
from typing import Dict, Any


class DocumentParsingTool(Tool):
    """Tool for parsing documents - example implementation"""
    
    def __init__(self):
        super().__init__(
            tool_id="document-parser",
            name="Document Parsing Tool",
            description="Parses content from various document formats",
            category="processing"
        )
        self.config = ToolConfig("document_parser_tool")
        # Use default config if no specific config is set
        for key, value in DEFAULT_CONFIGS["document_parser_tool"].items():
            if self.config.get(key) is None:
                self.config.set(key, value)
    
    def get_params_definition(self):
        supported_formats = self.config.get("supported_formats", ["txt"])
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
                "enum": supported_formats,
                "description": f"Document format ({', '.join(supported_formats)})"
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