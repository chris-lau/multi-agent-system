"""
Demo script to showcase the tool framework
"""
from tools.tool_framework import ToolRegistry
from tools.tool_execution_service import ToolExecutionService
from tools.example_tools import WebSearchTool, DocumentParsingTool, StatisticalAnalysisTool


def main():
    print("Multi-Agent Research System - Tool Framework Demo")
    print("=" * 50)
    
    # Create tool registry and register tools
    registry = ToolRegistry()
    
    # Register example tools
    registry.register_tool(WebSearchTool())
    registry.register_tool(DocumentParsingTool())
    registry.register_tool(StatisticalAnalysisTool())
    
    # Create tool execution service
    tool_service = ToolExecutionService(registry)
    
    print("\nAvailable tools:")
    available_tools = tool_service.get_available_tools()
    for tool_id, tool_info in available_tools.items():
        print(f"- {tool_id}: {tool_info['name']} ({tool_info['category']})")
    
    print("\n" + "="*50)
    print("Testing individual tool execution:")
    
    # Test web search tool
    print("\n1. Testing Web Search Tool:")
    web_result = tool_service.execute_tool("web-search", query="AI in healthcare", num_results=3)
    print(f"Result: {web_result}")
    
    # Test document parsing tool
    print("\n2. Testing Document Parsing Tool:")
    doc_result = tool_service.execute_tool("document-parser", file_path="/path/to/doc.pdf", format="pdf")
    print(f"Result: {doc_result}")
    
    # Test statistical analysis tool
    print("\n3. Testing Statistical Analysis Tool:")
    stat_result = tool_service.execute_tool("statistical-analysis", data=[1, 2, 3, 4, 5], analysis_type="descriptive")
    print(f"Result: {stat_result}")
    
    print("\n" + "="*50)
    print("Testing parallel tool execution:")
    
    # Test parallel execution
    tool_requests = [
        {"tool_id": "web-search", "params": {"query": "renewable energy", "num_results": 2}},
        {"tool_id": "statistical-analysis", "params": {"data": [10, 20, 30], "analysis_type": "descriptive"}},
        {"tool_id": "document-parser", "params": {"file_path": "/path/to/research.pdf"}}
    ]
    
    parallel_results = tool_service.execute_tools_parallel(tool_requests)
    
    print("\nParallel execution results:")
    for i, result in enumerate(parallel_results):
        print(f"Request {i+1}: {result['request']}")
        print(f"Result: {result['result']}")
        print()
    
    print("\n" + "="*50)
    print("Execution history:")
    history = tool_service.get_execution_history()
    for i, record in enumerate(history[-5:], 1):  # Show last 5 executions
        print(f"{i}. Tool: {record['tool_id']}, Duration: {record['duration']:.2f}s")
    
    # Cleanup
    tool_service.shutdown()
    print("\nDemo completed!")


if __name__ == "__main__":
    main()