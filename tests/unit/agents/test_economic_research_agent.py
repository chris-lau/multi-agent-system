"""
Unit tests for economic_research_agent.py to improve test coverage
"""
import sys
import os
from unittest.mock import Mock, patch
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.economic_research_agent.economic_research_agent import EconomicResearchAgent
from a2a_protocol import A2AMessage, MessageType


class TestEconomicResearchAgent:
    """Test cases for EconomicResearchAgent class"""
    
    def test_init(self):
        """Test EconomicResearchAgent initialization"""
        agent = EconomicResearchAgent()
        
        assert agent.agent_id == "economic-research-agent"
        assert agent.client is not None
        assert agent.supported_message_types == [
            MessageType.REQUEST_RESEARCH_TASK.value,
            MessageType.RESPONSE_TOOL_RESULT.value
        ]
    
    def test_get_capabilities(self):
        """Test get_capabilities method returns correct structure"""
        agent = EconomicResearchAgent()
        capabilities = agent.get_capabilities()
        
        assert "id" in capabilities
        assert "name" in capabilities
        assert "description" in capabilities
        assert "supportedMessageTypes" in capabilities
        assert capabilities["id"] == "economic-research-agent"
        assert capabilities["name"] == "Economic Research Agent"
    
    @patch('builtins.print')
    def test_receive_message_unknown_type(self, mock_print):
        """Test handling of unknown message types"""
        agent = EconomicResearchAgent()
        message = A2AMessage.create_message(
            MessageType.REQUEST_FACTCHECK_VERIFY,  # Using existing message type and changing it
            "test-sender",
            "economic-research-agent",
            {}
        )
        message.type = "unknown-type"  # Override type to simulate unknown type
        
        agent.receive_message(message)
        
        mock_print.assert_called_with("Economic Research Agent: Unknown message type received: unknown-type")
    
    @patch('agents.economic_research_agent.economic_research_agent.EconomicResearchAgent.handle_research_task')
    @patch('builtins.print')
    def test_receive_message_research_task(self, mock_print, mock_handle_research_task):
        """Test handling of research task messages"""
        agent = EconomicResearchAgent()
        message = A2AMessage.create_message(
            MessageType.REQUEST_RESEARCH_TASK,
            "research-orchestrator-agent",
            "economic-research-agent",
            {}
        )
        
        agent.receive_message(message)
        
        mock_print.assert_called_with("Economic Research Agent received message of type: request:research:task")
        mock_handle_research_task.assert_called_once_with(message)
    
    @patch('agents.economic_research_agent.economic_research_agent.EconomicResearchAgent.handle_tool_result')
    @patch('builtins.print')
    def test_receive_message_tool_result(self, mock_print, mock_handle_tool_result):
        """Test handling of tool result messages"""
        agent = EconomicResearchAgent()
        message = A2AMessage.create_message(
            MessageType.RESPONSE_TOOL_RESULT,
            "tool-service",
            "economic-research-agent",
            {}
        )
        
        agent.receive_message(message)
        
        mock_print.assert_called_with("Economic Research Agent received message of type: response:tool-result")
        mock_handle_tool_result.assert_called_once_with(message)
    
    @patch('agents.economic_research_agent.economic_research_agent.EconomicResearchAgent.perform_economic_research')
    @patch('builtins.print')
    def test_handle_research_task(self, mock_print, mock_perform_research):
        """Test handling of research tasks"""
        agent = EconomicResearchAgent()
        
        # Mock the LLM interface and client
        agent.client.send_message = Mock()
        mock_perform_research.return_value = {
            "findings": "test findings",
            "sources": ["source1"],
            "confidence": 0.85
        }
        
        message = A2AMessage.create_message(
            MessageType.REQUEST_RESEARCH_TASK,
            "research-orchestrator-agent",
            "economic-research-agent",
            {
                "query": "test query",
                "context": "research the economic aspects of this query"
            }
        )
        
        agent.handle_research_task(message)
        
        # Verify that perform_economic_research was called with the right data
        mock_perform_research.assert_called_once_with("test query", "research the economic aspects of this query")
        
        # Verify that send_message was called (which means a response was sent)
        assert agent.client.send_message.called
    
    @patch('builtins.print')
    def test_handle_tool_result(self, mock_print):
        """Test handling of tool results"""
        agent = EconomicResearchAgent()
        message = A2AMessage.create_message(
            MessageType.RESPONSE_TOOL_RESULT,
            "tool-service",
            "economic-research-agent",
            {
                "tool_id": "web-search-tool",
                "result": {"data": "test result"}
            }
        )
        
        agent.handle_tool_result(message)
        
        mock_print.assert_any_call("Economic Research Agent received tool result from web-search-tool: {'data': 'test result'}")
    
    @patch('llm_interface.GeminiLLMInterface')
    def test_perform_economic_research(self, mock_llm_interface):
        """Test the perform_economic_research method"""
        agent = EconomicResearchAgent()
        
        mock_llm_instance = Mock()
        expected_result = {"status": "completed", "findings": "test findings"}
        mock_llm_instance.perform_economic_research.return_value = expected_result
        agent.llm_interface = mock_llm_instance
        
        query = "economic impact of AI"
        context = "analyze economic aspects"
        result = agent.perform_economic_research(query, context)
        
        mock_llm_instance.perform_economic_research.assert_called_once_with(query, context)
        assert result == expected_result
    
    @patch('builtins.print')
    def test_send_tool_request(self, mock_print):
        """Test sending tool requests"""
        agent = EconomicResearchAgent()
        agent.client.send_message = Mock()
        
        agent.send_tool_request("statistical-analysis", {"data": [1, 2, 3]}, "tool-service")
        
        # Verify that send_message was called once
        assert agent.client.send_message.called
        mock_print.assert_called_with("Economic Research Agent requesting tool execution: statistical-analysis")