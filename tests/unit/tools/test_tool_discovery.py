"""
Unit tests for tool_discovery.py to improve test coverage
"""
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import tempfile
import importlib.util
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.tool_discovery import discover_tools_in_directory, discover_all_tools, load_tool_instances
from tools.tool_framework import Tool


# Create a simple test tool class for testing
class TestTool(Tool):
    def __init__(self):
        super().__init__(
            tool_id="test-tool",
            name="Test Tool",
            description="A tool for testing",
            category="testing"
        )
    
    def get_params_definition(self):
        return {}
    
    def execute(self, **params):
        return {"result": "test"}


class TestToolDiscovery:
    """Test cases for tool discovery functions"""
    
    def test_discover_tools_in_directory(self):
        """Test discovering tools in a directory"""
        # Create a temporary directory structure for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a Python file with a tool class
            tool_file_path = os.path.join(temp_dir, "test_tool.py")
            with open(tool_file_path, 'w') as f:
                f.write("""
from tools.tool_framework import Tool

class MockTool(Tool):
    def __init__(self):
        super().__init__(
            tool_id="mock-tool",
            name="Mock Tool", 
            description="A mock tool for testing",
            category="testing"
        )
    
    def get_params_definition(self):
        return {}
    
    def execute(self, **params):
        return {"result": "mock"}
""")
            
            # Now test the discovery function
            tool_classes = discover_tools_in_directory(temp_dir)
            
            # Verify that the MockTool class was found
            assert len(tool_classes) == 1
            assert tool_classes[0].__name__ == "MockTool"
    
    def test_discover_tools_in_directory_with_invalid_file(self):
        """Test discovering tools when directory has non-Python files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create both Python and non-Python files
            python_file_path = os.path.join(temp_dir, "valid_tool.py")
            with open(python_file_path, 'w') as f:
                f.write("""
from tools.tool_framework import Tool

class ValidTool(Tool):
    def __init__(self):
        super().__init__(
            tool_id="valid-tool",
            name="Valid Tool",
            description="A valid tool",
            category="testing"
        )
    
    def get_params_definition(self):
        return {}
    
    def execute(self, **params):
        return {"result": "valid"}
""")
            
            # Create a non-Python file
            non_python_path = os.path.join(temp_dir, "not_a_tool.txt")
            with open(non_python_path, 'w') as f:
                f.write("This is not a Python file")
            
            # Create a file starting with __ (should be ignored)
            ignore_file_path = os.path.join(temp_dir, "__init__.py")
            with open(ignore_file_path, 'w') as f:
                f.write("")
            
            tool_classes = discover_tools_in_directory(temp_dir)
            
            # Only the valid Python tool should be found
            assert len(tool_classes) == 1
            assert tool_classes[0].__name__ == "ValidTool"
    
    def test_discover_tools_in_directory_with_import_error(self):
        """Test discovering tools when there are import errors"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a Python file with syntax errors
            bad_file_path = os.path.join(temp_dir, "bad_tool.py")
            with open(bad_file_path, 'w') as f:
                f.write("""
# This has a syntax error - missing colon
if True
    print("bad syntax")
""")
            
            # Test that the function handles import errors gracefully
            with patch('builtins.print') as mock_print:
                tool_classes = discover_tools_in_directory(temp_dir)
                
                # Should return empty list due to import errors
                assert len(tool_classes) == 0
                # Print should have been called for the import error
                assert mock_print.called
    
    def test_discover_all_tools(self):
        """Test discovering all tools from subdirectories"""
        with tempfile.TemporaryDirectory() as base_temp_dir:
            # Create a subdirectory with a tool
            sub_dir = os.path.join(base_temp_dir, "test_subdir")
            os.makedirs(sub_dir)
            
            tool_file_path = os.path.join(sub_dir, "subdir_tool.py")
            with open(tool_file_path, 'w') as f:
                f.write("""
from tools.tool_framework import Tool

class SubdirTool(Tool):
    def __init__(self):
        super().__init__(
            tool_id="subdir-tool",
            name="Subdir Tool",
            description="A tool in subdirectory",
            category="testing"
        )
    
    def get_params_definition(self):
        return {}
    
    def execute(self, **params):
        return {"result": "subdir"}
""")
            
            # Create a __pycache__ directory (should be ignored)
            cache_dir = os.path.join(base_temp_dir, "__pycache__")
            os.makedirs(cache_dir)
            
            all_tools = discover_all_tools(base_temp_dir)
            
            # Verify that the subdir tool was found under its directory name
            assert "test_subdir" in all_tools
            assert len(all_tools["test_subdir"]) == 1
            assert all_tools["test_subdir"][0].__name__ == "SubdirTool"
            
            # Verify that __pycache__ was ignored
            assert "__pycache__" not in all_tools
    
    def test_load_tool_instances(self):
        """Test loading instances of all discovered tools"""
        # Patch the discover_all_tools function to return our test tool
        with patch('tools.tool_discovery.discover_all_tools') as mock_discover:
            mock_discover.return_value = {
                "test_dir": [TestTool]  # Return our test tool class
            }
            
            tools = load_tool_instances()
            
            # Verify that one tool instance was created
            assert len(tools) == 1
            assert isinstance(tools[0], TestTool)
            assert tools[0].tool_id == "test-tool"
    
    def test_load_tool_instances_with_instantiation_error(self):
        """Test loading tool instances when instantiation fails"""
        # Create a mock tool class that raises an exception on instantiation
        class FailingTool(Tool):
            def __init__(self):
                raise ValueError("Cannot instantiate")
            
            def get_params_definition(self):
                return {}
            
            def execute(self, **params):
                return {"result": "fail"}
        
        with patch('tools.tool_discovery.discover_all_tools') as mock_discover:
            mock_discover.return_value = {
                "failing_dir": [FailingTool]
            }
            
            with patch('builtins.print') as mock_print:
                tools = load_tool_instances()
                
                # Should return an empty list due to instantiation error
                assert len(tools) == 0
                # Print should have been called for the instantiation error
                assert mock_print.called