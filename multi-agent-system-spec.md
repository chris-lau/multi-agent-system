# Multi-Agent System Specification
## Using A2A Protocol

### Overview
A multi-agent system where domain-specific orchestrators coordinate specialized agents to address complex tasks across different domains. Each agent implements the A2A protocol for standardized communication and integrates with various tools for enhanced capabilities through autonomous tool discovery and selection. The system currently implements an orchestrator for multi-domain analysis, with support for additional orchestrator types for other specialized domains.

### Components

#### 1. Research Orchestrator
- **Role**: Coordinates tasks, aggregates results, manages tool usage, enables autonomous tool discovery and selection
- **Agent ID**: research-orchestrator-agent
- **Types**: Basic, Advanced, Custom (defined via JSON workflow configuration)
- **A2A Capabilities**:
  - Sends task requests to specialized agents
  - Receives and validates results
  - Manages task workflow
  - Generates final output
  - Discovers available tools for enhanced processing
  - Supports configurable workflow patterns (sequential, parallel, conditional)
- **A2A Message Types**:
  - `request:task` (outgoing)
  - `response:results` (incoming)
  - `request:discover-tools` (outgoing)
  - `response:available-tools` (incoming)
  - `request:use-tool` (outgoing)
  - `response:tool-result` (incoming)
- **Configuration**: Supports JSON-based workflow definitions for custom orchestrator behavior

#### 2. General Orchestrator Framework
- **Role**: Provides the framework for multiple orchestrator types to coordinate specialized agents for different task domains
- **Types**: Task Processing, Business Analysis, Technical Support, Customer Service, etc. (defined via JSON workflow configuration)
- **A2A Capabilities**:
  - Supports multiple orchestrator instances for different domains
  - Manages cross-orchestrator communication for complex multi-domain tasks
  - Enables tool usage across different orchestrator types
  - Supports configurable workflow patterns (sequential, parallel, conditional)
- **A2A Message Types**:
  - `request:orchestrator:task` (outgoing/incoming between orchestrators)
  - `response:orchestrator:results` (outgoing/incoming between orchestrators)
  - `request:discover-tools` (outgoing)
  - `response:available-tools` (incoming)
- **Configuration**: Supports JSON-based workflow definitions for custom orchestrator behavior

#### 2. Technology Agent
- **Role**: Analyzes technical aspects of queries using specialized tools with autonomous discovery and selection, with enhanced error handling and retry mechanisms
- **A2A Capabilities**:
  - Receives tech-focused sub-queries from orchestrators
  - Performs technical analysis
  - Returns tech-focused results
  - Discovers and selects appropriate tools autonomously
  - Implements error handling and retry mechanisms for robust operation
  - Provides logging and monitoring capabilities
- **A2A Message Types**:
  - `request:task` (incoming)
  - `response:results` (outgoing)
  - `request:discover-tools` (outgoing)
  - `response:available-tools` (incoming)

#### 3. Economic Agent
- **Role**: Analyzes economic implications using financial and economic tools with autonomous discovery and selection, with enhanced error handling and retry mechanisms
- **A2A Capabilities**:
  - Receives economic sub-queries from orchestrators
  - Performs economic analysis
  - Returns economic-focused results
  - Discovers and selects appropriate tools autonomously
  - Implements error handling and retry mechanisms for robust operation
  - Provides logging and monitoring capabilities
- **A2A Message Types**:
  - `request:task` (incoming)
  - `response:results` (outgoing)
  - `request:discover-tools` (outgoing)
  - `response:available-tools` (incoming)

#### 4. Social/Cultural Agent
- **Role**: Analyzes social/cultural impacts using sociological tools with autonomous discovery and selection, with enhanced error handling and retry mechanisms
- **A2A Capabilities**:
  - Receives social sub-queries from orchestrators
  - Performs social analysis
  - Returns social-focused results
  - Discovers and selects appropriate tools autonomously
  - Implements error handling and retry mechanisms for robust operation
  - Provides logging and monitoring capabilities
- **A2A Message Types**:
  - `request:task` (incoming)
  - `response:results` (outgoing)
  - `request:discover-tools` (outgoing)
  - `response:available-tools` (incoming)

#### 5. Fact-Checking Agent
- **Role**: Validates information from other agents using fact-checking tools with autonomous discovery and selection, with enhanced error handling and retry mechanisms
- **A2A Capabilities**:
  - Receives claims to verify from orchestrators
  - Cross-references multiple sources
  - Returns validation results
  - Discovers and selects appropriate tools autonomously
  - Implements error handling and retry mechanisms for robust operation
  - Provides logging and monitoring capabilities
- **A2A Message Types**:
  - `request:factcheck:verify` (incoming)
  - `response:factcheck:results` (outgoing)
  - `request:discover-tools` (outgoing)
  - `response:available-tools` (incoming)

### A2A Protocol Implementation

#### Message Structure
```
{
  "type": "request:task",
  "version": "1.0",
  "id": "unique-message-id",
  "timestamp": "ISO-8601-timestamp",
  "sender": "sender-agent-id",
  "receiver": "receiver-agent-id",
  "payload": {
    "query": "task-or-query-string",
    "context": "additional-context",
    "task_type": "technical|economic|social|factcheck|business|support",
    "deadline": "optional-deadline"
  },
  "metadata": {
    "priority": "high|normal|low",
    "dependencies": ["dependency-ids"],
    "callback_url": "optional-callback-endpoint"
  }
}
```

#### Task Message Structure
```
{
  "type": "request:task",
  "version": "1.0",
  "id": "unique-message-id",
  "timestamp": "ISO-8601-timestamp",
  "sender": "sender-agent-id",
  "receiver": "receiver-agent-id",
  "payload": {
    "query": "task-query-string",
    "context": "additional-context",
    "task_type": "technical|economic|social|factcheck",
    "deadline": "optional-deadline"
  },
  "metadata": {
    "priority": "high|normal|low",
    "dependencies": ["dependency-ids"],
    "callback_url": "optional-callback-endpoint"
  }
}
```

#### Orchestrator-to-Orchestrator Message Structure
```
{
  "type": "request:orchestrator:task",
  "version": "1.0",
  "id": "unique-message-id",
  "timestamp": "ISO-8601-timestamp",
  "sender": "sender-orchestrator-id",
  "receiver": "receiver-orchestrator-id",
  "payload": {
    "query": "orchestrator-task-query-string",
    "context": "additional-orchestrator-context",
    "task_type": "business|analysis|support|etc",
    "required_agents": ["agent-ids"],
    "deadline": "optional-deadline"
  },
  "metadata": {
    "priority": "high|normal|low",
    "dependencies": ["dependency-ids"],
    "callback_url": "optional-callback-endpoint"
  }
}
```

#### Tool Discovery Message Structure
```
{
  "type": "request:discover-tools",
  "version": "1.0",
  "id": "unique-message-id",
  "timestamp": "ISO-8601-timestamp",
  "sender": "sender-agent-id",
  "receiver": "tool-registry-id",
  "payload": {
    "category_filter": "optional-category-to-filter-tools",
    "capability_requirements": ["specific capabilities needed"]
  },
  "metadata": {
    "priority": "high|normal|low",
    "search_context": "context for the search (e.g., task query)"
  }
}
```

#### Required Endpoints for Each Agent
- **POST** `/a2a/message` - Receive A2A messages
- **GET** `/a2a/capabilities` - Return agent capabilities (JSON-LD format)
- **GET** `/a2a/status` - Return current status

#### Agent Capabilities Format (JSON-LD)
```
{
  "@context": "https://a2a-protocol.org/context.jsonld",
  "id": "agent-unique-identifier",
  "name": "Agent Display Name",
  "version": "1.0.0",
  "description": "Brief description",
  "supportedMessageTypes": [
    {
      "type": "request:task",
      "direction": "incoming",
      "schema": "schema-reference"
    },
    {
      "type": "response:results",
      "direction": "outgoing",
      "schema": "schema-reference"
    },
    {
      "type": "request:discover-tools",
      "direction": "outgoing",
      "schema": "schema-reference"
    },
    {
      "type": "response:available-tools",
      "direction": "incoming",
      "schema": "schema-reference"
    }
  ],
  "endpoints": {
    "message": "/a2a/message",
    "capabilities": "/a2a/capabilities",
    "status": "/a2a/status"
  }
}
```

### Workflow with Autonomous Tool Discovery and Usage

1. User submits task or query to appropriate Orchestrator
2. Orchestrator parses request and identifies required task types and domains
3. Orchestrator discovers relevant tools using `request:discover-tools`
4. Orchestrator autonomously selects appropriate tools based on decision logic
5. Orchestrator sends parallel A2A messages to appropriate specialized agents (Tech, Economic, Social/Cultural, etc.)
6. Specialized agents discover and select tools relevant to their assigned tasks
7. Agents execute selected tools (using real implementations) and process results
8. Specialized agents return results to Orchestrator
9. Orchestrator collects all results
10. Orchestrator sends results to Fact-Checking agent for validation (if applicable)
11. Fact-Checking agent discovers and uses validation tools autonomously
12. Fact-Checking agent uses real tools with actual functionality for validation
13. Orchestrator generates comprehensive output combining validated results
14. Output delivered to user

### Orchestrator-to-Orchestrator Communication (Future Implementation)

1. User submits complex multi-domain task
2. Main orchestrator identifies that multiple orchestrator types are needed
3. Main orchestrator communicates with specialized orchestrators using `request:orchestrator:task`
4. Specialized orchestrators coordinate their respective specialized agents
5. Specialized orchestrators return results to main orchestrator
6. Main orchestrator combines results from multiple orchestrators
7. Final output delivered to user

### Orchestrator Factory Pattern
- Implements factory pattern to instantiate appropriate orchestrator based on configuration
- Supports runtime selection of orchestrator type (basic, advanced, custom) via command-line options or configuration
- Validates workflow configuration before orchestrator instantiation
- Ensures backward compatibility with existing orchestrator functionality

### JSON-Based Workflow Configuration System (Phase 3)
- Define custom orchestrator behaviors using JSON configuration files
- Support for different orchestrator types (basic, advanced, custom)
- Configuration schema for defining agent interactions and message routing
- Conditional logic and branching in task workflows
- Support for sequential, parallel, and conditional execution patterns
- Visual builder compatibility for generating workflow configurations

### Error Handling & Monitoring
- Agents return standardized error responses in A2A format
- Timeout handling for unresponsive agents
- Comprehensive retry logic for failed communications (with configurable retry attempts and delays)
- Error handling and retry mechanisms implemented in all agents for robust operation
- Python logging integrated across all agents for monitoring and debugging
- Graceful degradation when agents are unavailable
- Improved output formatting and structure in orchestrator for better readability
- Factory pattern implementation for multiple orchestrator types (basic, advanced, custom)

### Independence & Testing
- Each agent runs as separate service
- Direct A2A communication between agents for validation tasks
- Independent deployment and scaling
- Individual agent testing via A2A-compatible client
- Mock agents for testing orchestration logic

### Security Considerations
- A2A message signing and verification
- Authentication between agents (if required)
- Input validation on all agent endpoints
- Rate limiting on message endpoints

### Tool Framework

#### Tool Definition Structure
```
{
  "tool_id": "unique-tool-identifier",
  "name": "Tool Display Name",
  "description": "Brief description of the tool's function",
  "category": "information-retrieval|data-analysis|validation|domain-specific|processing",
  "parameters": {
    "param1": {"type": "string", "required": true, "description": "Description of parameter"},
    "param2": {"type": "number", "required": false, "description": "Description of parameter"}
  },
  "output_schema": {
    "result": {"type": "string", "description": "Expected output format"}
  },
  "usage_examples": [
    {
      "scenario": "Example use case",
      "parameters": {"param1": "example_value"}
    }
  ]
}
```

### Workflow Configuration System

#### JSON-Based Orchestrator Workflows
- Define custom orchestrator behaviors using JSON configuration files
- Support for different orchestrator types (basic, advanced, custom)
- Configuration schema for defining agent interactions and message routing
- Conditional logic and branching in task workflows
- Support for sequential, parallel, and conditional execution patterns
- Visual builder compatibility for generating workflow configurations

#### Visual Orchestrator Builder (Future Implementation)
- User-friendly interface for creating custom task workflows
- Drag-and-drop functionality for arranging task steps
- Configuration export in JSON format for use by the orchestrator factory
- Workflow validation and error checking
- Template library for common task patterns
- Real-time preview of workflow execution

### Tool Management System

#### Tool Registry with Discovery Capabilities
- Central registry of available tools
- Metadata about each tool's capabilities, parameters, usage examples and effectiveness
- Tool availability and health monitoring
- Discovery API for agents to query tool capabilities
- Support for both mock and real tool implementations with environment-based switching

#### Tool Decision Engine
- Logic for agents to evaluate which tools to use
- Historical effectiveness tracking
- Recommendation system based on task requirements
- Resource optimization for tool execution
- Ability to select between mock and real implementations based on environment and availability
- Cross-orchestrator tool recommendation sharing

#### Real Tool Implementations
- **WebSearchTool**: Implemented using Tavily API, DuckDuckGo API, or Google Custom Search API (configurable)
- **DocumentParsingTool**: Implemented with PyPDF2 for PDF parsing, python-docx for Word documents, and BeautifulSoup for HTML
- **StatisticalAnalysisTool**: Enhanced with comprehensive statistical functions using numpy and scipy
- **API Key Management**: Secure storage and retrieval of API keys for external services
- **Environment Configuration**: Support for switching between mock and real implementations based on environment variables
- **Error Handling**: Comprehensive error handling for external API calls with fallback mechanisms
- **Rate Limiting & Retry Logic**: Built-in rate limiting and retry mechanisms for external services
- **Caching Mechanism**: Caching of tool results to improve performance and reduce external API calls

#### Independent Tool Management
- **Directory Structure**: Each tool in its own directory with separate files
- **Documentation**: Individual README files for each tool with detailed usage instructions
- **Separation of Concerns**: Each tool's implementation isolated in its own file
- **Dynamic Loading**: Tools can be loaded dynamically from their separate directories
- **Independent Updates**: Tools can be updated independently without affecting other components
- **Configuration Management**: Individual tool configuration through dedicated files
- **Testing**: Individual test suites for each tool in their respective directories

This specification provides a framework for agents to autonomously discover and select appropriate tools to enhance their task processing capabilities while maintaining the modular, A2A protocol-based architecture.