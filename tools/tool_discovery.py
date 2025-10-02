"""
Tool Discovery Service for the Multi-Agent Research System
This module enables dynamic discovery and loading of tools from tool directories
"""
import os
import sys
import importlib
import inspect
from typing import List, Type, Dict, Any
from tools.tool_framework import Tool


def discover_tools_in_directory(tool_dir_path: str) -> List[Type[Tool]]:
    """
    Discover and import all Tool classes from a given directory.
    
    Args:
        tool_dir_path: Path to the tool directory
        
    Returns:
        List of Tool classes found in the directory
    """
    tool_classes = []
    
    # Add the tool directory to Python path temporarily
    if tool_dir_path not in sys.path:
        sys.path.insert(0, tool_dir_path)
    
    # Find all Python files in the directory
    for file_name in os.listdir(tool_dir_path):
        if file_name.endswith('.py') and not file_name.startswith('__'):
            module_name = file_name[:-3]  # Remove .py extension
            
            try:
                # Import the module
                spec = importlib.util.spec_from_file_location(module_name, 
                    os.path.join(tool_dir_path, file_name))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find Tool classes in the module
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, Tool) and obj != Tool:
                        tool_classes.append(obj)
                        
            except ImportError as e:
                print(f"Could not import module {module_name}: {e}")
    
    # Remove the tool directory from Python path
    if tool_dir_path in sys.path:
        sys.path.remove(tool_dir_path)
    
    return tool_classes


def discover_all_tools(tools_base_path: str = "tools") -> Dict[str, Type[Tool]]:
    """
    Discover all tools from subdirectories within the tools base path.
    
    Args:
        tools_base_path: Base path where tool directories are located
        
    Returns:
        Dictionary mapping tool directory names to their Tool classes
    """
    all_tools = {}
    
    for dir_name in os.listdir(tools_base_path):
        dir_path = os.path.join(tools_base_path, dir_name)
        
        # Check if it's a directory and not a special directory like __pycache__
        if os.path.isdir(dir_path) and not dir_name.startswith('__'):
            tool_classes = discover_tools_in_directory(dir_path)
            all_tools[dir_name] = tool_classes
    
    return all_tools


def load_tool_instances() -> List[Tool]:
    """
    Load instances of all discovered tools.
    
    Returns:
        List of Tool instances
    """
    tools = []
    discovered_tools = discover_all_tools()
    
    for dir_name, tool_classes in discovered_tools.items():
        for tool_class in tool_classes:
            try:
                tool_instance = tool_class()
                tools.append(tool_instance)
            except Exception as e:
                print(f"Could not instantiate tool {tool_class.__name__}: {e}")
    
    return tools