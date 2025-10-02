# Multi-Agent System

This project implements a multi-agent system that uses specialized agents to address complex tasks across different domains. The system leverages the A2A (Agent-to-Agent) protocol for standardized communication between agents and currently focuses on research tasks using Google's Gemini LLM. The system is designed to support multiple orchestrator types for various specialized domains.

## Features

- **Configurable Orchestrator Agent**: Coordinates research tasks, aggregates results from specialized agents; supports multiple orchestrator types (basic, advanced, custom workflows)
- **Technology Research Agent**: Performs technical analysis using Gemini LLM
- **Economic Research Agent**: Performs economic analysis using Gemini LLM
- **Social/Cultural Research Agent**: Analyzes social and cultural impacts using Gemini LLM
- **Fact-Checking Agent**: Validates information from other agents using Gemini LLM
- **A2A Protocol Compliance**: Standardized communication between agents
- **Tool Framework**: Enhanced research capabilities through integrated tools with autonomous discovery and selection
- **JSON-Based Workflow Configuration**: Custom orchestrator behaviors using JSON configuration files
- **Modular Architecture**: Agents can be developed and tested independently
- **Visual Orchestrator Builder Ready**: Compatible with visual interface for creating custom research workflows (future feature)

## Prerequisites

- Python 3.7+
- Google Generative AI library: `pip install google-generativeai`

## Installation

1. Clone the repository or download the files
2. Install required dependencies:
   ```bash
   pip install google-generativeai
   ```

## Usage

Run the system with optional arguments:

```bash
python main.py [--api-key API_KEY] [--query "Your research query here"] [--model MODEL_NAME]
```

### Options:

- `--api-key`: Google Gemini API key (optional, can also be set as environment variable)
- `--query`: Research query to process (default: "Analyze the impact of AI on healthcare")
- `--model`: Gemini model to use (default: "gemini-pro")
- `--orchestrator`: Orchestrator type to use (basic, advanced, custom; default: "basic")
- `--workflow-config`: Path to JSON workflow configuration file (for custom orchestrator)

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

## How It Works

1. The Orchestrator Agent receives a research query
2. It discovers and selects relevant tools using the tool framework
3. It distributes specialized research tasks to specialized agents (Tech, Economic, Social/Cultural)
4. Each research agent discovers and selects appropriate tools autonomously for enhanced analysis
5. Each research agent uses the Gemini LLM to perform domain-specific analysis
6. Results are sent back to the Orchestrator Agent
7. The Orchestrator sends results to the Fact-Checking Agent for validation
8. The Fact-Checking Agent discovers and uses validation tools autonomously
9. The Fact-Checking Agent uses the Gemini LLM to validate the information
10. The Orchestrator generates a final comprehensive report

## API Key

To use the real Gemini LLM (instead of mock responses):
1. Get an API key from [Google AI Studio](https://aistudio.google.com/)
2. Either:
   - Pass it with the `--api-key` argument, or
   - Set the environment variable `GOOGLE_API_KEY` before running

If no API key is provided, the system will use mock responses for demonstration purposes.

## Architecture

- `a2a_protocol.py`: Implements the A2A protocol for agent communication
- `llm_interface.py`: Interfaces with Google's Gemini LLM
- `main.py`: Entry point with argument parsing
- `tools/`: Tool framework and execution service
  - `tool_framework.py`: Base classes and interfaces for tools
  - `tool_execution_service.py`: Service for executing tools with parallel execution capabilities
  - `tool_discovery.py`: Dynamic discovery and loading of tools from directories
  - `config/tool_config.py`: Configuration management for individual tools
  - `web_search_tool/`: Web search tool implementation
  - `document_parser_tool/`: Document parsing tool implementation  
  - `statistical_analysis_tool/`: Statistical analysis tool implementation
- `demo_tools.py`: Demo script showcasing the tool framework
- `tests/`: Test suite for the entire system
  - `integration/test_tool_integration.py`: Test script specifically for tool integration
  - `unit/core/test_llm_interface.py`: Tests for LLM interface functionality
  - `unit/tools/test_tool_execution_service.py`: Tests for tool execution service
- `agents/`: Contains individual agent implementations
  - `orchestrator_agent/`: Research Orchestrator agent directory
    - `research_orchestrator_agent.py`: Coordinates the research process
    - `README.md`: Documentation for the orchestrator agent
  - `tech_research_agent/`: Tech research agent directory
    - `tech_research_agent.py`: Performs technical research
    - `README.md`: Documentation for the tech research agent
  - `economic_research_agent/`: Economic research agent directory
    - `economic_research_agent.py`: Performs economic research
    - `README.md`: Documentation for the economic research agent
  - `social_cultural_research_agent/`: Social/Cultural research agent directory
    - `social_cultural_research_agent.py`: Analyzes social and cultural impacts
    - `README.md`: Documentation for the social/cultural research agent
  - `factcheck_agent/`: Fact-check agent directory
    - `factcheck_agent.py`: Validates research results
    - `README.md`: Documentation for the fact-check agent