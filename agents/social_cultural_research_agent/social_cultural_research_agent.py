"""
Social/Cultural Research Agent for Multi-Agent Research System
Implements the Social/Cultural Research Agent using A2A protocol with tool capabilities
"""
from a2a_protocol import A2AMessage, MessageType, A2AClient, get_agent_capabilities
import json
from typing import Dict, Any
from llm_interface import GeminiLLMInterface
import logging
import time


class SocialCulturalResearchAgent:
    """Social/Cultural Research Agent - Analyzes social and cultural impacts of queries"""
    
    def __init__(self):
        self.agent_id = "social-cultural-research-agent"
        self.client = A2AClient(self.agent_id)
        self.llm_interface = GeminiLLMInterface()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"{self.agent_id}")
        
        # Define supported message types
        self.supported_message_types = [
            MessageType.REQUEST_RESEARCH_TASK.value,
            MessageType.RESPONSE_TOOL_RESULT.value
        ]
        
        # Retry configuration
        self.max_retries = 3
        self.retry_delay = 1  # seconds
    
    def get_capabilities(self):
        """Return agent capabilities in A2A format"""
        return get_agent_capabilities(
            agent_id=self.agent_id,
            name="Social/Cultural Research Agent",
            description="Analyzes social and cultural impacts of the query, performs social analysis using Gemini LLM, and uses social/cultural tools for enhanced research",
            supported_types=[
                MessageType.REQUEST_RESEARCH_TASK.value,
                MessageType.RESPONSE_TOOL_RESULT.value
            ]
        )
    
    def receive_message(self, message: A2AMessage):
        """Handle incoming A2A messages"""
        print(f"Social/Cultural Research Agent received message of type: {message.type}")
        self.logger.info(f"Social/Cultural Research Agent received message of type: {message.type}")
        
        try:
            if message.type == MessageType.REQUEST_RESEARCH_TASK.value:
                self.handle_research_task(message)
            elif message.type == MessageType.RESPONSE_TOOL_RESULT.value:
                self.handle_tool_result(message)
            else:
                print(f"Social/Cultural Research Agent: Unknown message type received: {message.type}")
                self.logger.warning(f"Social/Cultural Research Agent: Unknown message type received: {message.type}")
        except Exception as e:
            print(f"Error processing message {message.type}: {str(e)}")
            self.logger.error(f"Error processing message {message.type}: {str(e)}")
            # In a real implementation, we might want to send an error response
    
    def handle_research_task(self, message: A2AMessage):
        """Process a research task and respond with results"""
        query = message.payload.get("query", "")
        context = message.payload.get("context", "")
        
        print(f"Social/Cultural Research Agent processing: {query}")
        self.logger.info(f"Social/Cultural Research Agent processing: {query}")
        
        # Perform research using Gemini LLM with retry mechanism
        social_cultural_results = self._perform_research_with_retry(query, context)
        
        if social_cultural_results is None:
            print(f"Failed to perform research after {self.max_retries} attempts")
            self.logger.error(f"Failed to perform research after {self.max_retries} attempts")
            # In a real implementation, we might send an error message back
            return
        
        # Prepare response
        response_payload = {
            "agent_type": "social_cultural",
            "query": query,
            "results": social_cultural_results
        }
        
        response_msg = A2AMessage.create_message(
            MessageType.RESPONSE_RESEARCH_RESULTS,
            self.agent_id,
            message.sender,  # Send back to orchestrator
            response_payload
        )
        
        print(f"Social/Cultural Research Agent sending results to {message.sender}")
        self.logger.info(f"Social/Cultural Research Agent sending results to {message.sender}")
        
        # Send message with retry mechanism
        self._send_message_with_retry(message.sender, response_msg)
    
    def _perform_research_with_retry(self, query: str, context: str):
        """Perform research with retry mechanism"""
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                self.logger.info(f"Attempt {attempt + 1}/{self.max_retries} for research task")
                return self.perform_social_cultural_research(query, context)
            except Exception as e:
                last_exception = e
                self.logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < self.max_retries - 1:  # Don't sleep on the last attempt
                    time.sleep(self.retry_delay)
        
        self.logger.error(f"All {self.max_retries} attempts failed. Last error: {str(last_exception)}")
        return None
    
    def _send_message_with_retry(self, receiver: str, message: A2AMessage):
        """Send message with retry mechanism"""
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                self.logger.info(f"Attempt {attempt + 1}/{self.max_retries} to send message")
                return self.client.send_message(receiver, message)
            except Exception as e:
                last_exception = e
                self.logger.warning(f"Attempt {attempt + 1} to send message failed: {str(e)}")
                if attempt < self.max_retries - 1:  # Don't sleep on the last attempt
                    time.sleep(self.retry_delay)
        
        self.logger.error(f"Failed to send message after {self.max_retries} attempts. Last error: {str(last_exception)}")
    
    def handle_tool_result(self, message: A2AMessage):
        """Handle results from tool execution"""
        tool_id = message.payload.get("tool_id", "unknown")
        result = message.payload.get("result", {})
        print(f"Social/Cultural Research Agent received tool result from {tool_id}: {result}")
        # In a real implementation, we would incorporate the tool result into our research process
    
    def perform_social_cultural_research(self, query: str, context: str) -> Dict[str, Any]:
        """Perform social/cultural research using Gemini LLM"""
        return self.llm_interface.perform_social_cultural_research(query, context)
    
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
        
        print(f"Social/Cultural Research Agent requesting tool execution: {tool_id}")
        self.client.send_message(receiver, tool_msg)