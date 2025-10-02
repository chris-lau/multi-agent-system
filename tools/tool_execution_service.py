"""
Tool Execution Service for Multi-Agent Research System
Handles execution of tools requested by agents
"""
from typing import Dict, Any, Optional
from tools.tool_framework import ToolRegistry, Tool
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue


class ToolExecutionService:
    """Service to execute tools requested by agents"""
    
    def __init__(self, registry: ToolRegistry):
        self.registry = registry
        self.execution_history = []
        self.max_workers = 5  # Maximum concurrent tool executions
        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self.lock = threading.Lock()
    
    def execute_tool(self, tool_id: str, **params) -> Optional[Dict[str, Any]]:
        """Execute a single tool with given parameters"""
        start_time = time.time()
        
        result = self.registry.execute_tool(tool_id, **params)
        
        execution_record = {
            "tool_id": tool_id,
            "params": params,
            "result": result,
            "timestamp": time.time(),
            "duration": time.time() - start_time
        }
        
        with self.lock:
            self.execution_history.append(execution_record)
        
        return result
    
    def execute_tools_parallel(self, tool_requests: list) -> list:
        """Execute multiple tools in parallel"""
        results = []
        
        # Submit all tool requests to executor
        future_to_request = {}
        for request in tool_requests:
            tool_id = request.get("tool_id")
            params = request.get("params", {})
            future = self.executor.submit(self.execute_tool, tool_id, **params)
            future_to_request[future] = request
        
        # Collect results
        for future in as_completed(future_to_request):
            request = future_to_request[future]
            try:
                result = future.result()
                results.append({
                    "request": request,
                    "result": result
                })
            except Exception as e:
                results.append({
                    "request": request,
                    "error": str(e)
                })
        
        # Sort results to match original request order
        sorted_results = []
        for request in tool_requests:
            for result in results:
                if result["request"] == request:
                    sorted_results.append(result)
                    break
        
        return sorted_results
    
    def get_execution_history(self) -> list:
        """Get the history of tool executions"""
        return self.execution_history.copy()
    
    def get_tool_definition(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """Get the definition of a tool"""
        return self.registry.get_tool_definition(tool_id)
    
    def get_available_tools(self) -> Dict[str, Dict[str, Any]]:
        """Get all available tools with their definitions"""
        tools = {}
        for tool_id, tool in self.registry.get_all_tools().items():
            tools[tool_id] = {
                "name": tool.name,
                "description": tool.description,
                "category": tool.category,
                "definition": tool.get_params_definition()
            }
        return tools
    
    def add_tool(self, tool: Tool):
        """Add a new tool to the registry"""
        self.registry.register_tool(tool)
    
    def shutdown(self):
        """Shutdown the execution service"""
        self.executor.shutdown(wait=True)