# Multi-Agent Research & Analysis System - Project Context

## Project Overview

The Multi-Agent Research & Analysis System is an AI-powered platform that uses multiple specialized agents to address complex tasks across different domains. By leveraging the A2A (Agent-to-Agent) protocol for standardized communication and integrating with various tools through autonomous discovery and selection, the system provides comprehensive, validated results with modular, independently deployable components.

## Core Architecture

### Agents
- **Research Orchestrator Agent**: Coordinates research tasks, aggregates results, manages tool usage, enables autonomous tool discovery and selection for research tasks
- **Tech Research Agent**: Performs technical analysis using Gemini LLM
- **Economic Research Agent**: Performs economic analysis using Gemini LLM
- **Social/Cultural Research Agent**: Analyzes social and cultural impacts using Gemini LLM
- **Fact-Check Agent**: Validates information from other agents using Gemini LLM

### Tool Framework
- **Tool Framework**: Base classes and interfaces for tools that agents can use
- **Tool Execution Service**: Service for executing tools with parallel execution capabilities
- **Tool Discovery**: Dynamic discovery and loading of tools from directories
- **Tool Configuration**: Configuration management for individual tools
- Individual tool implementations: Web Search Tool, Document Parser Tool, Statistical Analysis Tool

### A2A Protocol Implementation
- Standardized communication between agents
- Message types: request:research:task, response:research:results, request:factcheck:verify, response:factcheck:results, request:use-tool, response:tool-result
- Required endpoints: POST `/a2a/message`, GET `/a2a/capabilities`, GET `/a2a/status`
- Agent capabilities format in JSON-LD

## Building and Running

### Prerequisites
- Python 3.7+
- Google Generative AI library: `pip install google-generativeai`

### Installation
1. Clone the repository or download the files
2. Install required dependencies:
   ```bash
   pip install google-generativeai
   ```

### Usage
Run the system with optional arguments:
```bash
python main.py [--api-key API_KEY] [--query "Your research query here"] [--model MODEL_NAME] [--orchestrator ORCHESTRATOR_TYPE] [--workflow-config CONFIG_PATH]
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

## Project Structure

```
multi-agents/
├── a2a_protocol.py                 # A2A protocol implementation
├── llm_interface.py                # Interfaces with Google's Gemini LLM
├── main.py                         # Entry point with argument parsing
├── demo_tools.py                   # Demo script showcasing the tool framework
├── development-phases.md           # Development roadmap
├── multi-agent-system-spec.md      # System specification
├── product-definition.md           # Product definition
├── pytest.ini                      # Pytest configuration
├── QWEN.md                         # This file
├── README.md                       # Project documentation
├── __pycache__/                    # Python cache
├── .pytest_cache/                  # Pytest cache
├── agents/                         # Agent implementations
│   ├── orchestrator_agent/         # Research Orchestrator agent directory
│   │   ├── research_orchestrator_agent.py  # Coordinates the research process
│   │   └── README.md               # Documentation for the orchestrator agent
│   ├── tech_research_agent/        # Tech research agent directory
│   │   ├── tech_research_agent.py  # Performs technical research
│   │   └── README.md               # Documentation for the tech research agent
│   ├── economic_research_agent/    # Economic research agent directory
│   │   ├── economic_research_agent.py  # Performs economic research
│   │   └── README.md               # Documentation for the economic research agent
│   ├── social_cultural_research_agent/  # Social/Cultural research agent directory
│   │   ├── social_cultural_research_agent.py  # Analyzes social and cultural impacts
│   │   └── README.md               # Documentation for the social/cultural research agent
│   └── factcheck_agent/            # Fact-check agent directory
│       ├── factcheck_agent.py      # Validates research results
│       └── README.md               # Documentation for the fact-check agent
├── config/                         # Configuration files
├── tools/                          # Tool framework
│   ├── tool_framework.py           # Base classes and interfaces for tools
│   ├── tool_execution_service.py   # Service for executing tools with parallel execution capabilities
│   ├── tool_discovery.py           # Dynamic discovery and loading of tools from directories
│   ├── config/tool_config.py       # Configuration management for individual tools
│   ├── web_search_tool/            # Web search tool implementation
│   ├── document_parser_tool/       # Document parsing tool implementation  
│   └── statistical_analysis_tool/  # Statistical analysis tool implementation
└── tests/                          # Test suite for the entire system
    ├── unit/
    │   ├── core/test_llm_interface.py         # LLM interface tests
    │   └── tools/test_tool_execution_service.py # Tool execution service tests
    └── integration/test_tool_integration.py      # Tool integration tests
```

## Development Phases

### Phase 1: MVP (Completed)
- Create Research Orchestrator Agent with basic A2A protocol implementation
- Create tech research agent with basic A2A protocol implementation
- Create economic research agent with basic A2A protocol implementation
- Create fact-checking agent with basic A2A protocol implementation
- Implement basic A2A message handling for all agents
- Implement simple research query interface
- Develop basic text-based report generation
- Validate concept through sample research queries
- Implement tool framework and registry system
- Create basic tool execution service
- Enhance each agent with tool usage capabilities
- Add web search tool integration
- Add document parsing tool
- Update A2A protocol with tool-related message types
- Test tool integration with existing agents
- Create Tool Decision Engine for autonomous tool selection
- Enable agents to discover available tools and their capabilities
- Implement autonomous tool selection and usage logic in agents
- Add tool usage decision-making capabilities to agents
- Implement historical effectiveness tracking for tools
- Add usage examples to tool definitions
- Update the tool registry with discovery APIs
- Implement the `request:discover-tools` and `response:available-tools` A2A messages
- Refactor tools into independently manageable directories with separate files and READMEs

### Phase 2: Enhanced Functionality (Planned)
- Add social/cultural research agent
- Improve report formatting and structure
- Implement basic error handling and retry mechanisms
- Add logging and basic monitoring
- Add support for multiple orchestrator types (basic, advanced, custom)

### Phase 3: Robustness & Reliability (Planned)
- Implement comprehensive error handling and timeout mechanisms
- Add graceful degradation when agents are unavailable
- Implement message queuing for reliability
- Add health checks and agent status monitoring
- Implement JSON-based workflow configuration system for orchestrators

### Phase 4: Tool Enhancement (Planned)
- Replace mock tools with real implementations (WebSearchTool, DocumentParsingTool, StatisticalAnalysisTool)
- Implement real WebSearchTool using Tavily API or DuckDuckGo API
- Implement real DocumentParsingTool with PyPDF2 and python-docx support
- Enhance StatisticalAnalysisTool with comprehensive statistical functions using numpy/scipy
- Add API key management for external services
- Implement environment-based configuration to switch between mock and real tools
- Add comprehensive error handling for external API calls
- Implement rate limiting and retry logic for external services
- Add caching mechanism for tool results to improve performance
- Create additional real tools (Code execution tool, Database query tool, etc.)
- Test real tool implementations with existing agent workflows

### Future Phases
- Security & Performance enhancements
- User Experience improvements
- Advanced features including visual orchestrator builder
- Performance optimization

## Development Conventions

- Each agent is contained in its own directory with dedicated README documentation
- All agents implement the A2A protocol for standardized communication
- LLM integration is handled through the `llm_interface.py` module
- Tool framework allows for modular enhancement of agent capabilities
- Type hints are used throughout the codebase for better maintainability
- Error handling is implemented at each level of the system
- Tests are provided for different system components in the `tests/` directory
- Configuration management for individual tools using JSON-based configuration files
- Dynamic tool discovery enables flexible addition of new tools

## Key Design Patterns

- **Agent-to-Agent (A2A) Protocol**: Standardized communication between agents
- **Tool Framework**: Abstract base classes for creating tools with consistent interfaces
- **Message Router Pattern**: Handles message routing between agents in the demo environment
- **Dependency Injection**: Agents receive tool registries and other dependencies
- **Strategy Pattern**: Different tool implementations can be swapped based on environment
- **Factory Pattern**: Creates appropriate orchestrator based on configuration
- **Configuration Management**: Individual tool configuration through dedicated files
- **Dynamic Discovery**: Automatic discovery and loading of tools from directories

## Testing

The project includes various test files organized in the `tests/` directory:
- Unit tests for core functionality (LLM interface, tool execution service)
- Integration tests for tool integration with agents
- Test configuration in `pytest.ini`
- Shared fixtures in `tests/conftest.py`

Run tests using:
```bash
python -m pytest tests/
```

## Integration with LLMs

The system interfaces with Google's Gemini LLM through the `llm_interface.py` module. It provides mock responses when no API key is provided and uses real LLM responses when an API key is configured. The system handles both technical and economic research as well as fact-checking using the LLM.