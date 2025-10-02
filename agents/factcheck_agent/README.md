# Fact-Check Agent

The Fact-Check Agent specializes in validating information from other agents by cross-referencing multiple sources using the Gemini LLM.

## Functionality

- Validates research results from other agents
- Uses Gemini LLM for fact-checking and verification
- Responds with validation status, confidence levels, and identified issues
- Communicates with orchestrator agent using A2A protocol

## A2A Protocol Implementation

- Handles `request:factcheck:verify` message type
- Sends `response:factcheck:results` messages back to orchestrator
- Follows standardized message structure for A2A communication

## Dependencies

- `a2a_protocol.py` - For A2A message handling
- `llm_interface.py` - For Gemini LLM integration

## Configuration

- Agent ID: `factcheck-agent`
- Supported message types: `request:factcheck:verify`

## Usage

This agent should be run as part of the Multi-Agent Research & Analysis System. It receives research results from the orchestrator for validation and responds with fact-checking results.