"""
Unit tests for demo_tools.py to improve test coverage
"""
import sys
import os
from unittest.mock import patch, Mock, MagicMock
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_demo_tools_main_function():
    """Test the main function of demo_tools.py by mocking all external dependencies"""
    # Since the main function runs the entire demo, we'll mock all external dependencies
    with patch('demo_tools.ToolRegistry') as mock_registry_class, \
         patch('demo_tools.ToolExecutionService') as mock_service_class, \
         patch('demo_tools.WebSearchTool') as mock_web_tool_class, \
         patch('demo_tools.DocumentParsingTool') as mock_doc_tool_class, \
         patch('demo_tools.StatisticalAnalysisTool') as mock_stat_tool_class, \
         patch('builtins.print') as mock_print:
        
        # Create mock instances
        mock_registry_instance = Mock()
        mock_registry_class.return_value = mock_registry_instance
        
        mock_service_instance = Mock()
        mock_service_instance.get_available_tools.return_value = {
            "web-search": {"name": "Web Search Tool", "category": "search"},
            "document-parser": {"name": "Document Parser Tool", "category": "parser"},
            "statistical-analysis": {"name": "Statistical Analysis Tool", "category": "analysis"}
        }
        # Mock the execute_tool method to return a simple result
        mock_service_instance.execute_tool.return_value = "mock result"
        # Mock the execute_tools_parallel method to return mock results
        mock_service_instance.execute_tools_parallel.return_value = [
            {"request": {"tool_id": "web-search", "params": {}}, "result": "mock result 1"},
            {"request": {"tool_id": "statistical-analysis", "params": {}}, "result": "mock result 2"},
            {"request": {"tool_id": "document-parser", "params": {}}, "result": "mock result 3"}
        ]
        # Mock the get_execution_history method to return mock history
        mock_service_instance.get_execution_history.return_value = [
            {"tool_id": "web-search", "duration": 0.5},
            {"tool_id": "document-parser", "duration": 1.2},
            {"tool_id": "statistical-analysis", "duration": 0.8}
        ]
        mock_service_class.return_value = mock_service_instance
        
        # Create mock tool instances
        mock_web_tool_instance = Mock()
        mock_doc_tool_instance = Mock()
        mock_stat_tool_instance = Mock()
        mock_web_tool_class.return_value = mock_web_tool_instance
        mock_doc_tool_class.return_value = mock_doc_tool_instance
        mock_stat_tool_class.return_value = mock_stat_tool_instance

        # Import and run the main function from demo_tools
        from demo_tools import main
        main()
        
        # Verify that print was called (the main function has print statements)
        assert mock_print.called
        # Verify registry was created
        mock_registry_class.assert_called()
        # Verify tools were registered
        mock_registry_instance.register_tool.assert_any_call(mock_web_tool_instance)
        mock_registry_instance.register_tool.assert_any_call(mock_doc_tool_instance)
        mock_registry_instance.register_tool.assert_any_call(mock_stat_tool_instance)
        # Verify service was created with the registry
        mock_service_class.assert_called_once_with(mock_registry_instance)
        # Verify the service shutdown was called
        mock_service_instance.shutdown.assert_called()