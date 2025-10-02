# Economic Research Agent

The Economic Research Agent specializes in analyzing economic implications and performing economic analysis of queries using the Gemini LLM.

## Functionality

- Performs economic analysis of research queries
- Uses Gemini LLM for in-depth economic research
- Responds with economic findings, sources, and confidence levels
- Communicates with orchestrator agent using A2A protocol

## A2A Protocol Implementation

- Handles `request:research:task` message type
- Sends `response:research:results` messages back to orchestrator
- Follows standardized message structure for A2A communication

## Dependencies

- `a2a_protocol.py` - For A2A message handling
- `llm_interface.py` - For Gemini LLM integration

## Configuration

- Agent ID: `economic-research-agent`
- Supported message types: `request:research:task`

## Usage

This agent should be run as part of the Multi-Agent Research & Analysis System. It receives research tasks from the orchestrator and responds with economic analysis results.