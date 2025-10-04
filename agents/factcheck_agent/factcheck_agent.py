"""
Fact-Checking Agent for Multi-Agent Research System
Implements the Fact-Checking Agent using A2A protocol with tool capabilities
"""
from a2a_protocol import A2AMessage, MessageType, A2AClient, get_agent_capabilities
import json
from typing import Dict, Any
from llm_interface import GeminiLLMInterface
import logging
import time


class FactCheckAgent:
    """Fact-Checking Agent - Validates information from other agents"""
    
    def __init__(self):
        self.agent_id = "factcheck-agent"
        self.client = A2AClient(self.agent_id)
        self.llm_interface = GeminiLLMInterface()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"{self.agent_id}")
        
        # Define supported message types
        self.supported_message_types = [
            MessageType.REQUEST_FACTCHECK_VERIFY.value,
            MessageType.RESPONSE_TOOL_RESULT.value
        ]
        
        # Retry configuration
        self.max_retries = 3
        self.retry_delay = 1  # seconds
    
    def get_capabilities(self):
        """Return agent capabilities in A2A format"""
        return get_agent_capabilities(
            agent_id=self.agent_id,
            name="Fact-Checking Agent",
            description="Validates information from other agents by cross-referencing multiple sources using Gemini LLM and validation tools",
            supported_types=[
                MessageType.REQUEST_FACTCHECK_VERIFY.value,
                MessageType.RESPONSE_TOOL_RESULT.value
            ]
        )
    
    def receive_message(self, message: A2AMessage):
        """Handle incoming A2A messages"""
        print(f"Fact-Check Agent received message of type: {message.type}")
        self.logger.info(f"Fact-Check Agent received message of type: {message.type}")
        
        try:
            if message.type == MessageType.REQUEST_FACTCHECK_VERIFY.value:
                self.handle_verification_request(message)
            elif message.type == MessageType.RESPONSE_TOOL_RESULT.value:
                self.handle_tool_result(message)
            else:
                print(f"Fact-Check Agent: Unknown message type received: {message.type}")
                self.logger.warning(f"Fact-Check Agent: Unknown message type received: {message.type}")
        except Exception as e:
            print(f"Error processing message {message.type}: {str(e)}")
            self.logger.error(f"Error processing message {message.type}: {str(e)}")
            # In a real implementation, we might want to send an error response
    
    def handle_verification_request(self, message: A2AMessage):
        """Process a verification request and respond with validation results"""
        research_results = message.payload.get("research_results", {})
        
        print(f"Fact-Check Agent validating research results: {list(research_results.keys())}")
        self.logger.info(f"Fact-Check Agent validating research results: {list(research_results.keys())}")
        
        # Perform fact-checking using Gemini LLM with retry mechanism
        validation_results = self._perform_fact_checking_with_retry(research_results)
        
        if validation_results is None:
            print(f"Failed to perform fact-checking after {self.max_retries} attempts")
            self.logger.error(f"Failed to perform fact-checking after {self.max_retries} attempts")
            # In a real implementation, we might send an error message back
            return
        
        # Prepare response
        response_payload = {
            "validation_results": validation_results,
            "research_results": research_results  # Include original results
        }
        
        response_msg = A2AMessage.create_message(
            MessageType.RESPONSE_FACTCHECK_RESULTS,
            self.agent_id,
            message.sender,  # Send back to orchestrator
            response_payload
        )
        
        print(f"Fact-Check Agent sending validation results to {message.sender}")
        self.logger.info(f"Fact-Check Agent sending validation results to {message.sender}")
        
        # Send message with retry mechanism
        self._send_message_with_retry(message.sender, response_msg)
    
    def _perform_fact_checking_with_retry(self, research_results: Dict[str, Any]):
        """Perform fact-checking with retry mechanism"""
        last_exception = None
        for attempt in range(self.max_retries):
            try:
                self.logger.info(f"Attempt {attempt + 1}/{self.max_retries} for fact-checking task")
                return self.perform_fact_checking(research_results)
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
        print(f"Fact-Check Agent received tool result from {tool_id}: {result}")
        # In a real implementation, we would incorporate the tool result into our validation process
    
    def perform_fact_checking(self, research_results: Dict[str, Any]) -> Dict[str, Any]:
        """Perform fact-checking using Gemini LLM"""
        return self.llm_interface.perform_fact_checking(research_results)
    
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
        
        print(f"Fact-Check Agent requesting tool execution: {tool_id}")
        self.client.send_message(receiver, tool_msg)