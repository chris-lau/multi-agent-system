# Multi-Agent Research & Analysis System

## Project Overview

The Multi-Agent Research & Analysis System is an AI-powered research platform that uses multiple specialized agents to answer complex questions across different domains. By leveraging the A2A (Agent-to-Agent) protocol for standardized communication and integrating with various research tools through autonomous discovery and selection, the system provides comprehensive, validated research results with modular, independently deployable components.

The system implements a multi-agent architecture where:
- An orchestration agent coordinates research tasks and aggregates results
- Specialized research agents handle domain-specific queries (technical, economic, social)
- A fact-checking agent validates information from other agents
- All communication follows the A2A protocol for interoperability
- Agents can autonomously discover and select appropriate tools for their research tasks

## Project Structure

- `README.md` - Documentation on how to use the system
- `QWEN.md` - This file with project overview
- `product-definition.md` - Outlines the product overview, problem statement, solution, target users, key features, and success metrics
- `research-system-spec.md` - Provides the technical specification for the system architecture and A2A protocol implementation
- `development-phases.md` - Contains a detailed roadmap with 7 development phases and trackable tasks
- `main.py` - Entry point with argument parsing to run the system
- `a2a_protocol.py` - Implements the A2A protocol for agent communication
- `llm_interface.py` - Interfaces with Google's Gemini LLM
- `demo_tools.py` - Demo script showcasing the tool framework
- `test_tool_integration.py` - Test script specifically for tool integration
- `agents/` - Directory containing individual agent implementations:
  - `orchestrator_agent/` - Orchestrator agent directory:
    - `orchestrator_agent.py` - Coordinates the research process
    - `README.md` - Documentation for the orchestrator agent
  - `tech_research_agent/` - Tech research agent directory:
    - `tech_research_agent.py` - Performs technical research using Gemini LLM
    - `README.md` - Documentation for the tech research agent
  - `economic_research_agent/` - Economic research agent directory:
    - `economic_research_agent.py` - Performs economic research using Gemini LLM
    - `README.md` - Documentation for the economic research agent
  - `factcheck_agent/` - Fact-check agent directory:
    - `factcheck_agent.py` - Validates research results using Gemini LLM
    - `README.md` - Documentation for the fact-check agent
- `tools/` - Directory containing the tool framework:
  - `tool_framework.py` - Base classes and interfaces for tools
  - `tool_execution_service.py` - Service for executing tools with parallel execution capabilities
  - `example_tools.py` - Example tools implementation (WebSearchTool, DocumentParsingTool, StatisticalAnalysisTool)
  - `__init__.py` - Package initialization for tools module

## A2A Protocol Implementation

The system implements the A2A (Agent-to-Agent) protocol for standardized communication between agents. Key aspects include:

- **Message Structure**: JSON-based messages with standardized fields (type, id, timestamp, sender, receiver, payload, metadata)
- **Required Endpoints**: Each agent must implement POST `/a2a/message`, GET `/a2a/capabilities`, and GET `/a2a/status`
- **Capabilities Format**: JSON-LD format describing agent capabilities and supported message types
- **Agent Roles**: Orchestration, technology research, economic research, social/cultural research, and fact-checking
- **Enhanced for Tool Support**: Additional message types for tool discovery and usage:
  - `request:discover-tools` - Request available tools
  - `response:available-tools` - Return list of available tools
  - `request:use-tool` - Request to execute a specific tool
  - `response:tool-result` - Return results from tool execution

## Building and Running

### Prerequisites
- Python 3.7+
- Google Generative AI library: `pip install google-generativeai`

### Installation
1. Install required dependencies:
   ```bash
   pip install google-generativeai
   ```

### Usage
Run the system with optional arguments:

```bash
python main.py [--api-key API_KEY] [--query "Your research query here"]
```

Options:
- `--api-key`: Google Gemini API key (optional, can also be set as environment variable)
- `--query`: Research query to process (default: "Analyze the impact of AI on healthcare")

### Examples:
1. Run with default settings:
   ```bash
   python main.py
   ```

2. Run with a custom query:
   ```bash
   python main.py --query "What are the latest advancements in renewable energy?"
   ```

3. Run with API key and custom query:
   ```bash
   python main.py --api-key "your_api_key_here" --query "Analyze quantum computing applications in cryptography"
   ```

## LLM Integration

The system uses Google's Gemini LLM for research tasks. To use real LLM capabilities:
1. Get an API key from Google AI Studio
2. Either:
   - Pass it with the `--api-key` argument, or
   - Set the environment variable `GOOGLE_API_KEY`

If no API key is provided, the system will use mock responses for demonstration purposes.

## How It Works

1. The Orchestrator Agent receives a research query
2. It distributes specialized research tasks to the Tech Research Agent and Economic Research Agent
3. Agents discover and select relevant tools autonomously
4. Each research agent uses the Gemini LLM to perform domain-specific analysis
5. Results are sent back to the Orchestrator Agent
6. The Orchestrator sends results to the Fact-Checking Agent for validation
7. The Fact-Checking Agent uses the Gemini LLM to validate the information
8. The Orchestrator generates a final comprehensive report

## Tool Framework

The system includes a comprehensive tool framework that enables agents to:
- Discover available tools with their capabilities
- Select appropriate tools based on research needs
- Execute tools and process results
- Incorporate tool results into research outcomes

The tool framework consists of:
- Base `Tool` class that agents can extend
- `ToolRegistry` to manage available tools
- `ToolExecutionService` for executing tools synchronously or in parallel
- A2A protocol extensions for tool discovery and usage
- Example tools like WebSearchTool, DocumentParsingTool, and StatisticalAnalysisTool

## Development Conventions

- Each agent is contained in its own directory with dedicated README documentation
- All agents implement the A2A protocol for standardized communication
- LLM integration is handled through the `llm_interface.py` module
- Tool framework allows for modular enhancement of agent capabilities
- Type hints are used throughout the codebase for better maintainability
- Error handling is implemented at each level of the system

## Development Roadmap

The project follows a phased development approach:

**Phase 1: MVP** - Core 4 agents with basic A2A protocol implementation (COMPLETED)
**Phase 1: Enhanced MVP** - Tool framework and autonomous tool discovery/selection (IN PROGRESS)
**Phase 2: Enhanced Functionality** - Add social/cultural research agent and improve reports
**Phase 3: Robustness & Reliability** - Error handling and monitoring improvements
**Phase 4: Security & Performance** - Security features and input validation
**Phase 5: User Experience** - Dashboard and improved UI
**Phase 6: Advanced Features** - Analytics and custom workflows
**Phase 7: Performance Optimization** - Scaling and performance improvements

## Key Features

- Multi-domain research across technical, economic, and social perspectives
- Built-in fact-checking and validation of information
- Modular architecture with independently deployable agents
- A2A protocol compliance for standardized communication
- Integration with Google's Gemini LLM for AI-powered research
- Comprehensive reporting with multiple perspectives
- Autonomous tool discovery and selection capabilities
- Enhanced research capabilities through tool integration

## Technical Requirements

- Each agent must be independently deployable
- All agents must implement A2A protocol
- System must handle agent failures gracefully
- Response time under 60 seconds for standard queries
- Reports must include source attribution
- Agents must be able to discover and select appropriate tools autonomously

## Current Status

The MVP (Phase 1) has been completed, with 4 core agents (orchestrator, tech research, economic research, and fact-checking) implemented with basic A2A protocol implementation and LLM integration. The system can be run with `python main.py` and accepts optional arguments for the API key and research query.

The Enhanced MVP (Phase 1) is in progress, with tool framework and registry system implemented, tool execution service created, agents enhanced with tool usage capabilities, and new A2A protocol messages for tool discovery and results added. The next steps involve implementing autonomous tool selection and usage logic in agents and historical effectiveness tracking for tools.