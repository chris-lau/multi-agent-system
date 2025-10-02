# Orchestrator Agent

The Orchestrator Agent coordinates research tasks, aggregates results from specialized agents, manages workflow, and generates final reports.

## Functionality

- Coordinates research tasks across specialized agents
- Aggregates results from different research domains
- Manages the research workflow
- Generates comprehensive final reports
- Communicates with specialized agents using A2A protocol
- Sends results to fact-checking agent for validation

## A2A Protocol Implementation

- Handles `response:research:results` and `response:factcheck:results` message types
- Sends research tasks to specialized agents
- Coordinates the overall research workflow

## Dependencies

- `a2a_protocol.py` - For A2A message handling
- `llm_interface.py` - For any LLM interactions (if needed in future enhancements)

## Configuration

- Agent ID: `orchestrator-agent`
- Supported message types: `response:research:results`, `response:factcheck:results`

## Usage

This agent is part of the Multi-Agent Research & Analysis System. It should be run as part of the complete system along with other agents.