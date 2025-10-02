"""
Orchestrator Agent for Multi-Agent Research System
Implements the Research Orchestrator using A2A protocol with tool capabilities
"""
from a2a_protocol import A2AMessage, MessageType, A2AClient, get_agent_capabilities
import json
from typing import List, Dict, Any
import time
from tools.tool_execution_service import ToolExecutionService
from tools.tool_framework import ToolRegistry


class ResearchOrchestratorAgent:
    """Research Orchestrator Agent - Coordinates research tasks and aggregates results"""
    
    def __init__(self):
        self.agent_id = "research-orchestrator-agent"
        self.client = A2AClient(self.agent_id)
        self.research_results = {}
        self.agents = {
            "tech": "tech-research-agent",
            "economic": "economic-research-agent",
            "factcheck": "factcheck-agent"
        }
        
        # Initialize tool framework
        self.tool_registry = ToolRegistry()
        self.tool_service = ToolExecutionService(self.tool_registry)
        
        # Define supported message types
        self.supported_message_types = [
            MessageType.RESPONSE_RESEARCH_RESULTS.value,
            MessageType.RESPONSE_FACTCHECK_RESULTS.value,
            MessageType.RESPONSE_TOOL_RESULT.value
        ]
    
    def get_capabilities(self):
        """Return agent capabilities in A2A format"""
        return get_agent_capabilities(
            agent_id=self.agent_id,
            name="Research Orchestrator",
            description="Coordinates research tasks, aggregates results from specialized agents, manages workflow, generates final reports, and uses tools for enhanced research",
            supported_types=[
                MessageType.RESPONSE_RESEARCH_RESULTS.value, 
                MessageType.RESPONSE_FACTCHECK_RESULTS.value,
                MessageType.RESPONSE_TOOL_RESULT.value
            ]
        )
    
    def receive_message(self, message: A2AMessage):
        """Handle incoming A2A messages"""
        print(f"Orchestrator received message of type: {message.type}")
        
        if message.type == MessageType.RESPONSE_RESEARCH_RESULTS.value:
            self.handle_research_results(message)
        elif message.type == MessageType.RESPONSE_FACTCHECK_RESULTS.value:
            self.handle_factcheck_results(message)
        elif message.type == MessageType.RESPONSE_TOOL_RESULT.value:
            self.handle_tool_result(message)
        else:
            print(f"Orchestrator: Unknown message type received: {message.type}")
    
    def handle_research_results(self, message: A2AMessage):
        """Handle research results from specialized agents"""
        agent_type = message.payload.get("agent_type", "unknown")
        results = message.payload.get("results", {})
        
        self.research_results[agent_type] = results
        print(f"Orchestrator stored research results from {agent_type}: {results}")
        
        # Check if we have results from all research agents
        if self.all_research_results_collected():
            print("All research results collected, sending to fact-checker...")
            self.send_results_to_factchecker()
    
    def handle_tool_result(self, message: A2AMessage):
        """Handle results from tool execution"""
        tool_id = message.payload.get("tool_id", "unknown")
        result = message.payload.get("result", {})
        print(f"Orchestrator received tool result from {tool_id}: {result}")
        # In a real implementation, we would incorporate the tool result into our research process
    
    def all_research_results_collected(self) -> bool:
        """Check if results from all research agents have been collected"""
        required_agents = ["tech", "economic"]
        return all(agent in self.research_results for agent in required_agents)
    
    def send_results_to_factchecker(self):
        """Send aggregated results to fact-checker for validation"""
        factcheck_payload = {
            "research_results": self.research_results,
            "query": self.current_query  # This would need to be stored from the original request
        }
        
        factcheck_msg = A2AMessage.create_message(
            MessageType.REQUEST_FACTCHECK_VERIFY,
            self.agent_id,
            self.agents["factcheck"],
            factcheck_payload
        )
        
        print(f"Orchestrator sending fact-check request to {self.agents['factcheck']}")
        self.client.send_message(self.agents["factcheck"], factcheck_msg)
    
    def handle_factcheck_results(self, message: A2AMessage):
        """Handle fact-check validation results"""
        validation_results = message.payload.get("validation_results", {})
        print(f"Orchestrator received fact-check validation: {validation_results}")
        
        # Generate final report
        final_report = self.generate_final_report(validation_results)
        print("Final report generated:")
        print(final_report)
    
    def process_research_request(self, query: str):
        """Process a research request from a user"""
        self.current_query = query
        self.research_results = {}  # Reset results
        
        # Create research tasks for specialized agents
        for agent_type, agent_id in self.agents.items():
            if agent_type != "factcheck":  # Don't send initial task to factchecker
                self.send_research_task(agent_type, agent_id, query)
    
    def send_research_task(self, agent_type: str, agent_id: str, query: str):
        """Send research task to specialized agent"""
        payload = {
            "query": query,
            "context": f"Research the {agent_type} aspects of this query",
            "task_type": agent_type
        }
        
        msg = A2AMessage.create_message(
            MessageType.REQUEST_RESEARCH_TASK,
            self.agent_id,
            agent_id,
            payload
        )
        
        print(f"Orchestrator sending {agent_type} research task to {agent_id}")
        self.client.send_message(agent_id, msg)
    
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
        
        print(f"Orchestrator requesting tool execution: {tool_id}")
        self.client.send_message(receiver, tool_msg)
    
    def generate_final_report(self, validation_results: Dict[str, Any]) -> str:
        """Generate final report combining all validated research results"""
        report_parts = ["FINAL RESEARCH REPORT", "="*20]
        
        # Add each agent's validated results
        for agent_type, result in self.research_results.items():
            report_parts.append(f"\n{agent_type.upper()} RESEARCH:")
            report_parts.append(f"Findings: {result.get('findings', 'Not available')}")
            report_parts.append(f"Sources: {result.get('sources', 'Not available')}")
            report_parts.append(f"Validation: {validation_results.get(agent_type, 'Not validated')}")
        
        return "\n".join(report_parts)