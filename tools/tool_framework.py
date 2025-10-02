"""
Tool Framework for Multi-Agent Research System
Defines the base classes and interfaces for tools that agents can use
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import json


@dataclass
class ToolDefinition:
    """Definition of a tool that agents can use"""
    tool_id: str
    name: str
    description: str
    category: str  # information-retrieval, data-analysis, validation, domain-specific, processing
    parameters: Dict[str, Any]
    output_schema: Dict[str, Any]
    required_params: List[str] = None

    def __post_init__(self):
        if self.required_params is None:
            self.required_params = []
            for param_name, param_info in self.parameters.items():
                if param_info.get("required", False):
                    self.required_params.append(param_name)


class Tool(ABC):
    """Base class for all tools that agents can use"""
    
    def __init__(self, tool_id: str, name: str, description: str, category: str):
        self.tool_id = tool_id
        self.name = name
        self.description = description
        self.category = category
    
    @abstractmethod
    def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute the tool with given parameters"""
        pass
    
    def validate_parameters(self, params: Dict[str, Any]) -> bool:
        """Validate that required parameters are provided"""
        # This is a basic validation; in a real implementation, you'd do more thorough checks
        for param_name in self.get_required_params():
            if param_name not in params:
                return False
        return True
    
    def get_required_params(self) -> List[str]:
        """Return list of required parameters"""
        return [param for param, info in self.get_params_definition().items() 
                if info.get("required", False)]
    
    def get_params_definition(self) -> Dict[str, Any]:
        """Return definition of parameters this tool requires"""
        return {}
    
    def get_definition(self) -> ToolDefinition:
        """Return the tool definition"""
        return ToolDefinition(
            tool_id=self.tool_id,
            name=self.name,
            description=self.description,
            category=self.category,
            parameters=self.get_params_definition(),
            output_schema=self.get_output_schema()
        )
    
    def get_output_schema(self) -> Dict[str, Any]:
        """Return the expected output schema of this tool"""
        return {"result": {"type": "any", "description": "Tool execution result"}}


class ToolRegistry:
    """Registry to manage all available tools"""
    
    def __init__(self):
        self._tools: Dict[str, Tool] = {}
    
    def register_tool(self, tool: Tool):
        """Register a tool in the registry"""
        self._tools[tool.tool_id] = tool
        print(f"Tool registered: {tool.name} (ID: {tool.tool_id})")
    
    def get_tool(self, tool_id: str) -> Optional[Tool]:
        """Get a tool by its ID"""
        return self._tools.get(tool_id)
    
    def get_all_tools(self) -> Dict[str, Tool]:
        """Get all registered tools"""
        return self._tools.copy()
    
    def get_tools_by_category(self, category: str) -> List[Tool]:
        """Get all tools in a specific category"""
        return [tool for tool in self._tools.values() if tool.category == category]
    
    def get_tool_definition(self, tool_id: str) -> Optional[ToolDefinition]:
        """Get the definition of a tool by its ID"""
        tool = self.get_tool(tool_id)
        return tool.get_definition() if tool else None
    
    def execute_tool(self, tool_id: str, **params) -> Optional[Dict[str, Any]]:
        """Execute a tool with given parameters"""
        tool = self.get_tool(tool_id)
        if not tool:
            print(f"Tool with ID '{tool_id}' not found in registry")
            return None
        
        if not tool.validate_parameters(params):
            print(f"Invalid parameters for tool '{tool_id}'")
            return None
        
        try:
            return tool.execute(**params)
        except Exception as e:
            print(f"Error executing tool '{tool_id}': {str(e)}")
            return {"error": str(e)}