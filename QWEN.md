# Multi-Agent Research & Analysis System - Project Context

## Project Overview

The Multi-Agent Research & Analysis System is an AI-powered research platform that uses multiple specialized agents to answer complex questions across different domains. The system leverages the A2A (Agent-to-Agent) protocol for standardized communication and integrates with various research tools through autonomous discovery and selection, providing comprehensive, validated research results with modular, independently deployable components.

The system implements a multi-agent architecture where:
- An orchestrator agent coordinates research tasks and aggregates results
- Specialized research agents handle domain-specific queries (technical, economic, social/cultural)
- A fact-checking agent validates information from other agents
- All communication follows the A2A protocol for interoperability
- Agents can autonomously discover and select appropriate tools for their research tasks

## Core Architecture

### Agents
- **Orchestrator Agent**: Coordinates research tasks, aggregates results, manages tool usage, and generates final reports
- **Technology Research Agent**: Performs technical analysis based on user queries
- **Economic Research Agent**: Performs economic analysis based on user queries
- **Social/Cultural Research Agent**: Analyzes social and cultural impacts based on user queries
- **Fact-Checking Agent**: Validates information from other agents

### Tool Framework
- **Tool Framework**: Base classes and interfaces for tools that agents can use
- **Tool Registry**: Central registry of available tools with capabilities and metadata
- **Tool Execution Service**: Service for executing tools with parallel execution capabilities
- **Example Tools**: WebSearchTool, DocumentParsingTool, StatisticalAnalysisTool (currently mock implementations)

### A2A Protocol Implementation
- **Message Structure**: JSON-based messages with standardized fields
- **Required Endpoints**: POST `/a2a/message`, GET `/a2a/capabilities`, GET `/a2a/status`
- **Message Types**: request:research:task, response:research:results, request:factcheck:verify, response:factcheck:results, request:use-tool, response:tool-result
- **Tool Discovery**: request:discover-tools, response:available-tools messages

## Building and Running

### Prerequisites
- Python 3.7+
- Google Generative AI library: `pip install google-generativeai`

### Installation
```bash
pip install google-generativeai
```

### Usage
Run the system with optional arguments:
```bash
python main.py [--api-key API_KEY] [--query "Your research query here"] [--model MODEL_NAME]
```

Options:
- `--api-key`: Google Gemini API key (optional, can also be set as environment variable)
- `--query`: Research query to process (default: "Analyze the impact of AI on healthcare")
- `--model`: Gemini model to use (default: "gemini-pro")

Examples:
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

### Demo Scripts
- `demo_tools.py`: Demonstrates the tool framework functionality
- `test_tool_integration.py`: Tests tool integration with agents

## Project Structure

```
multi-agents/
├── a2a_protocol.py               # A2A protocol implementation
├── conftest.py                   # Pytest configuration
├── demo_tools.py                 # Tool framework demonstration
├── development-phases.md         # Development roadmap
├── llm_interface.py              # Gemini LLM interface
├── main.py                       # Main application entry point
├── product-definition.md         # Product definition
├── pytest.ini                    # Pytest configuration
├── QWEN.md                       # This file
├── README.md                     # Project documentation
├── research-system-spec.md       # System specification
├── tests/                        # Test suite
│   ├── unit/
│   │   ├── core/test_llm_interface.py         # LLM interface tests
│   │   └── tools/test_tool_execution_service.py # Tool execution service tests
│   └── integration/test_tool_integration.py      # Tool integration tests
├── __pycache__/                  # Python cache
├── .pytest_cache/                # Pytest cache
├── agents/                       # Agent implementations
│   ├── orchestrator_agent/ (Research Orchestrator agent directory)
│   ├── tech_research_agent/
│   ├── economic_research_agent/
│   ├── social_cultural_research_agent/
│   └── factcheck_agent/
└── tools/                        # Tool framework
    ├── tool_framework.py
    ├── tool_execution_service.py
    └── example_tools.py
```

## Development Phases

### Phase 1: MVP (Completed)
- Basic 4-agent system with A2A protocol
- Simple research query interface and report generation

### Phase 1: Enhanced MVP (Completed)
- Tool framework and registry system
- Basic tool execution service
- Agent enhancement with tool usage capabilities
- Web search and document parsing integration
- Tool discovery and selection capabilities

### Phase 2: Enhanced Functionality (Planned)
- Add social/cultural research agent
- Improve report formatting and structure
- Implement basic error handling and retry mechanisms
- Add logging and basic monitoring

### Phase 3: Robustness & Reliability (Planned)
- Comprehensive error handling and timeout mechanisms
- Graceful degradation when agents are unavailable
- Message queuing for reliability
- Health checks and agent status monitoring

### Phase 4: Tool Enhancement (Planned)
- Replace mock tools with real implementations:
  - WebSearchTool using Tavily API or DuckDuckGo API
  - DocumentParsingTool with PyPDF2 and python-docx support
  - StatisticalAnalysisTool with numpy/scipy functions
- API key management for external services
- Environment-based configuration for mock/real tool switching
- Error handling for external API calls
- Rate limiting and retry logic
- Caching mechanisms for tool results

### Future Phases
- Security & Performance improvements
- User Experience enhancements
- Advanced features
- Performance optimization

## Development Conventions

- Each agent is contained in its own directory with dedicated README documentation
- All agents implement the A2A protocol for standardized communication
- LLM integration is handled through the `llm_interface.py` module
- Tool framework allows for modular enhancement of agent capabilities
- Type hints are used throughout the codebase for better maintainability
- Error handling is implemented at each level of the system
- Tests are provided for different system components

## Key Design Patterns

- **Agent-to-Agent (A2A) Protocol**: Standardized communication between agents
- **Tool Framework**: Abstract base classes for creating tools with consistent interfaces
- **Message Router Pattern**: Handles message routing between agents in the demo environment
- **Dependency Injection**: Agents receive tool registries and other dependencies
- **Strategy Pattern**: Different tool implementations can be swapped based on environment

## Testing

The project includes various test files:
- `tests/unit/core/test_llm_interface.py`: Tests for LLM interface functionality
- `tests/unit/tools/test_tool_execution_service.py`: Tests for tool execution service
- `tests/integration/test_tool_integration.py`: Tests for tool integration with agents
- Test configuration in `pytest.ini`

## Current Status

The system has completed the MVP and Enhanced MVP phases with a functional multi-agent architecture and tool framework. The tools are currently implemented as mock versions, with the real implementations planned for Phase 4. The system can run research queries and demonstrate the multi-agent workflow with mock tools returning simulated data.

## Future Work

The next major focus is implementing real tool implementations (Phase 4), including:
- Web search integration with actual search APIs
- Document parsing with real parsing libraries
- Statistical analysis with proper mathematical functions
- API key management for external services
- Error handling and retry logic for external services
- Caching mechanisms for improved performance

## Python Learning Context

This project also serves as a practical learning environment for Python development, focusing on:

### Learning Approach
- Practical, interactive approach focusing on concept explanation
- Structured practice with real-world examples
- Code review and feedback mechanisms
- Project-based learning using the multi-agent system
- Debugging and problem-solving skills development
- Progressive skill development through the implementation phases

### Structured Goal-Setting
- SMART goals for each development phase
- Skill matrices for tracking progress across different Python concepts
- Progressive learning from basic concepts to advanced topics like:
  - Object-oriented programming (agents, tools)
  - Asynchronous programming (tool execution service)
  - API integration (LLM interface)
  - Data structures and algorithms

### Progress Tracking
- Automated assessments through testing
- Code journals for reflecting on learning
- Project milestones aligned with development phases
- Regular self-evaluation of Python skills
- Blind code reviews for unbiased feedback
- Spaced repetition for reinforcing key concepts

### Weekly Routine
- Structured practice sessions with the multi-agent codebase
- Implementation of new features following development phases
- Regular code reviews and refactoring exercises
- Progress dashboard for tracking learning metrics

### Advanced Techniques
- Code quality metrics and how to improve them
- Learning velocity calculation to optimize study time
- Gap analysis to identify areas for improvement
- Tool usage patterns and best practices in Python

This learning framework is designed to help users develop Python skills through hands-on work with the multi-agent research system, starting from basic understanding and progressing through increasingly complex features and implementations.