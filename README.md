# Multi-Agent Research & Analysis System

This project implements a multi-agent system that uses specialized agents to answer complex research questions across different domains. The system leverages the A2A (Agent-to-Agent) protocol for standardized communication between agents and uses Google's Gemini LLM for research tasks.

## Features

- **Orchestrator Agent**: Coordinates research tasks, aggregates results from specialized agents
- **Technology Research Agent**: Performs technical analysis using Gemini LLM
- **Economic Research Agent**: Performs economic analysis using Gemini LLM
- **Fact-Checking Agent**: Validates information from other agents using Gemini LLM
- **A2A Protocol Compliance**: Standardized communication between agents
- **Modular Architecture**: Agents can be developed and tested independently

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
python main.py [--api-key API_KEY] [--query "Your research query here"]
```

### Options:

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

## How It Works

1. The Orchestrator Agent receives a research query
2. It distributes specialized research tasks to the Tech Research Agent and Economic Research Agent
3. Each research agent uses the Gemini LLM to perform domain-specific analysis
4. Results are sent back to the Orchestrator Agent
5. The Orchestrator sends results to the Fact-Checking Agent for validation
6. The Fact-Checking Agent uses the Gemini LLM to validate the information
7. The Orchestrator generates a final comprehensive report

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
- `agents/`: Contains individual agent implementations
  - `orchestrator_agent/`: Orchestrator agent directory
    - `orchestrator_agent.py`: Coordinates the research process
    - `README.md`: Documentation for the orchestrator agent
  - `tech_research_agent/`: Tech research agent directory
    - `tech_research_agent.py`: Performs technical research
    - `README.md`: Documentation for the tech research agent
  - `economic_research_agent/`: Economic research agent directory
    - `economic_research_agent.py`: Performs economic research
    - `README.md`: Documentation for the economic research agent
  - `factcheck_agent/`: Fact-check agent directory
    - `factcheck_agent.py`: Validates research results
    - `README.md`: Documentation for the fact-check agent