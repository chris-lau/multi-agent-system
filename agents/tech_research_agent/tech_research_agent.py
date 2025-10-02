"""
Technology Research Agent for Multi-Agent Research System
Implements the Tech Research Agent using A2A protocol with tool capabilities
"""
from a2a_protocol import A2AMessage, MessageType, A2AClient, get_agent_capabilities
import json
from typing import Dict, Any
from llm_interface import GeminiLLMInterface


class TechResearchAgent:
    """Technology Research Agent - Researches technical aspects of queries"""
    
    def __init__(self):
        self.agent_id = "tech-research-agent"
        self.client = A2AClient(self.agent_id)
        self.llm_interface = GeminiLLMInterface()
        
        # Define supported message types
        self.supported_message_types = [
            MessageType.REQUEST_RESEARCH_TASK.value,
            MessageType.RESPONSE_TOOL_RESULT.value
        ]
    
    def get_capabilities(self):
        """Return agent capabilities in A2A format"""
        return get_agent_capabilities(
            agent_id=self.agent_id,
            name="Technology Research Agent",
            description="Researches technical aspects of the query, performs technical analysis using Gemini LLM, and uses technical tools for enhanced research",
            supported_types=[
                MessageType.REQUEST_RESEARCH_TASK.value,
                MessageType.RESPONSE_TOOL_RESULT.value
            ]
        )
    
    def receive_message(self, message: A2AMessage):
        """Handle incoming A2A messages"""
        print(f"Tech Research Agent received message of type: {message.type}")
        
        if message.type == MessageType.REQUEST_RESEARCH_TASK.value:
            self.handle_research_task(message)
        elif message.type == MessageType.RESPONSE_TOOL_RESULT.value:
            self.handle_tool_result(message)
        else:
            print(f"Tech Research Agent: Unknown message type received: {message.type}")
    
    def handle_research_task(self, message: A2AMessage):
        """Process a research task and respond with results"""
        query = message.payload.get("query", "")
        context = message.payload.get("context", "")
        
        print(f"Tech Research Agent processing: {query}")
        
        # Perform research using Gemini LLM
        tech_results = self.perform_technical_research(query, context)
        
        # Prepare response
        response_payload = {
            "agent_type": "tech",
            "query": query,
            "results": tech_results
        }
        
        response_msg = A2AMessage.create_message(
            MessageType.RESPONSE_RESEARCH_RESULTS,
            self.agent_id,
            message.sender,  # Send back to orchestrator
            response_payload
        )
        
        print(f"Tech Research Agent sending results to {message.sender}")
        self.client.send_message(message.sender, response_msg)
    
    def handle_tool_result(self, message: A2AMessage):
        """Handle results from tool execution"""
        tool_id = message.payload.get("tool_id", "unknown")
        result = message.payload.get("result", {})
        print(f"Tech Research Agent received tool result from {tool_id}: {result}")
        # In a real implementation, we would incorporate the tool result into our research process
    
    def perform_technical_research(self, query: str, context: str) -> Dict[str, Any]:
        """Perform technical research using Gemini LLM"""
        return self.llm_interface.perform_technical_research(query, context)
    
    def send_tool_request(self, tool_id: str, parameters: Dict[str, Any], receiver: str = "tool-service"):
        """Send a request to use a specific tool"""
        tool_payload = {
            "tool_id": tool_id,
            "parameters": parameters
        }
        
        tool_msg = A2AMessage.create_message(
            MessageType.REQUEST_USE_TOOL,
            self.agent_id,
            receiver,
            tool_payload
        )
        
        print(f"Tech Research Agent requesting tool execution: {tool_id}")
        self.client.send_message(receiver, tool_msg)