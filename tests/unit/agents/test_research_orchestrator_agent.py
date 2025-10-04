"""
Unit tests for research_orchestrator_agent.py to improve test coverage
"""
import sys
import os
from unittest.mock import Mock, patch
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.orchestrator_agent.research_orchestrator_agent import ResearchOrchestratorAgent
from a2a_protocol import A2AMessage, MessageType


class TestResearchOrchestratorAgent:
    """Test cases for ResearchOrchestratorAgent class"""
    
    def test_init(self):
        """Test ResearchOrchestratorAgent initialization"""
        agent = ResearchOrchestratorAgent()
        
        assert agent.agent_id == "research-orchestrator-agent"
        assert agent.client is not None
        assert agent.agents == {
            "tech": "tech-research-agent",
            "economic": "economic-research-agent",
            "factcheck": "factcheck-agent"
        }
        assert agent.supported_message_types == [
            MessageType.RESPONSE_RESEARCH_RESULTS.value,
            MessageType.RESPONSE_FACTCHECK_RESULTS.value,
            MessageType.RESPONSE_TOOL_RESULT.value
        ]
        assert agent.research_results == {}
    
    def test_get_capabilities(self):
        """Test get_capabilities method returns correct structure"""
        agent = ResearchOrchestratorAgent()
        capabilities = agent.get_capabilities()
        
        assert "id" in capabilities
        assert "name" in capabilities
        assert "description" in capabilities
        assert "supportedMessageTypes" in capabilities
        assert capabilities["id"] == "research-orchestrator-agent"
        assert capabilities["name"] == "Research Orchestrator"
    
    @patch('builtins.print')
    def test_receive_message_unknown_type(self, mock_print):
        """Test handling of unknown message types"""
        agent = ResearchOrchestratorAgent()
        message = A2AMessage.create_message(
            MessageType.REQUEST_RESEARCH_TASK,  # Using existing message type and changing it
            "test-sender",
            "research-orchestrator-agent",
            {}
        )
        message.type = "unknown-type"  # Override type to simulate unknown type
        
        agent.receive_message(message)
        
        mock_print.assert_called_with("Orchestrator: Unknown message type received: unknown-type")
    
    @patch('agents.orchestrator_agent.research_orchestrator_agent.ResearchOrchestratorAgent.handle_research_results')
    @patch('builtins.print')
    def test_receive_message_research_results(self, mock_print, mock_handle_research_results):
        """Test handling of research results messages"""
        agent = ResearchOrchestratorAgent()
        message = A2AMessage.create_message(
            MessageType.RESPONSE_RESEARCH_RESULTS,
            "tech-research-agent",
            "research-orchestrator-agent",
            {}
        )
        
        agent.receive_message(message)
        
        mock_print.assert_called_with("Orchestrator received message of type: response:research:results")
        mock_handle_research_results.assert_called_once_with(message)
    
    @patch('agents.orchestrator_agent.research_orchestrator_agent.ResearchOrchestratorAgent.handle_factcheck_results')
    @patch('builtins.print')
    def test_receive_message_factcheck_results(self, mock_print, mock_handle_factcheck_results):
        """Test handling of fact-check results messages"""
        agent = ResearchOrchestratorAgent()
        message = A2AMessage.create_message(
            MessageType.RESPONSE_FACTCHECK_RESULTS,
            "factcheck-agent",
            "research-orchestrator-agent",
            {}
        )
        
        agent.receive_message(message)
        
        mock_print.assert_called_with("Orchestrator received message of type: response:factcheck:results")
        mock_handle_factcheck_results.assert_called_once_with(message)
    
    @patch('agents.orchestrator_agent.research_orchestrator_agent.ResearchOrchestratorAgent.handle_tool_result')
    @patch('builtins.print')
    def test_receive_message_tool_result(self, mock_print, mock_handle_tool_result):
        """Test handling of tool result messages"""
        agent = ResearchOrchestratorAgent()
        message = A2AMessage.create_message(
            MessageType.RESPONSE_TOOL_RESULT,
            "tool-service",
            "research-orchestrator-agent",
            {}
        )
        
        agent.receive_message(message)
        
        mock_print.assert_called_with("Orchestrator received message of type: response:tool-result")
        mock_handle_tool_result.assert_called_once_with(message)
    
    @patch('builtins.print')
    def test_handle_research_results(self, mock_print):
        """Test handling of research results"""
        agent = ResearchOrchestratorAgent()
        message = A2AMessage.create_message(
            MessageType.RESPONSE_RESEARCH_RESULTS,
            "tech-research-agent",
            "research-orchestrator-agent",
            {
                "agent_type": "tech",
                "results": {"finding": "test finding"}
            }
        )
        
        agent.handle_research_results(message)
        
        assert agent.research_results["tech"] == {"finding": "test finding"}
        mock_print.assert_any_call("Orchestrator stored research results from tech: {'finding': 'test finding'}")
    
    @patch('builtins.print')
    def test_handle_tool_result(self, mock_print):
        """Test handling of tool results"""
        agent = ResearchOrchestratorAgent()
        message = A2AMessage.create_message(
            MessageType.RESPONSE_TOOL_RESULT,
            "tool-service",
            "research-orchestrator-agent",
            {
                "tool_id": "web-search-tool",
                "result": {"data": "test result"}
            }
        )
        
        agent.handle_tool_result(message)
        
        mock_print.assert_called_with("Orchestrator received tool result from web-search-tool: {'data': 'test result'}")
    
    def test_all_research_results_collected_true(self):
        """Test all_research_results_collected when all results are present"""
        agent = ResearchOrchestratorAgent()
        agent.research_results = {
            "tech": {"finding": "tech finding"},
            "economic": {"finding": "economic finding"}
        }
        
        result = agent.all_research_results_collected()
        assert result is True
    
    def test_all_research_results_collected_false(self):
        """Test all_research_results_collected when results are missing"""
        agent = ResearchOrchestratorAgent()
        agent.research_results = {
            "tech": {"finding": "tech finding"}
        }
        
        result = agent.all_research_results_collected()
        assert result is False
    
    @patch('builtins.print')
    def test_send_results_to_factchecker(self, mock_print):
        """Test sending results to fact-checker"""
        agent = ResearchOrchestratorAgent()
        agent.client.send_message = Mock()
        agent.research_results = {
            "tech": {"finding": "tech finding"},
            "economic": {"finding": "economic finding"}
        }
        agent.current_query = "test query"
        
        agent.send_results_to_factchecker()
        
        # Verify that send_message was called
        assert agent.client.send_message.called
        mock_print.assert_called_with("Orchestrator sending fact-check request to factcheck-agent")
    
    @patch('builtins.print')
    def test_handle_factcheck_results(self, mock_print):
        """Test handling of fact-check results"""
        agent = ResearchOrchestratorAgent()
        agent.research_results = {
            "tech": {"findings": "tech findings", "sources": ["source1"]},
            "economic": {"findings": "economic findings", "sources": ["source2"]}
        }
        
        message = A2AMessage.create_message(
            MessageType.RESPONSE_FACTCHECK_RESULTS,
            "factcheck-agent",
            "research-orchestrator-agent",
            {
                "validation_results": {"status": "verified", "confidence": 0.95}
            }
        )
        
        agent.handle_factcheck_results(message)
        
        mock_print.assert_any_call("Orchestrator received fact-check validation: {'status': 'verified', 'confidence': 0.95}")
    
    def test_process_research_request(self):
        """Test processing a research request"""
        agent = ResearchOrchestratorAgent()
        agent.client.send_message = Mock()
        
        agent.process_research_request("test query")
        
        # Verify that current_query is set
        assert agent.current_query == "test query"
        # Verify that research_results is reset
        assert agent.research_results == {}
        # Verify that messages were sent to the tech and economic research agents
        assert agent.client.send_message.called  # At least one call should be made
    
    @patch('builtins.print')
    def test_send_research_task(self, mock_print):
        """Test sending a research task to an agent"""
        agent = ResearchOrchestratorAgent()
        agent.client.send_message = Mock()
        
        agent.send_research_task("tech", "tech-research-agent", "test query")
        
        # Verify that send_message was called
        assert agent.client.send_message.called
        mock_print.assert_called_with("Orchestrator sending tech research task to tech-research-agent")
    
    def test_send_tool_request(self):
        """Test sending a tool request"""
        agent = ResearchOrchestratorAgent()
        agent.client.send_message = Mock()
        
        agent.send_tool_request("web-search-tool", {"query": "test"}, "tool-service")
        
        # Verify that send_message was called once
        assert agent.client.send_message.called
    
    def test_generate_final_report(self):
        """Test generating final report"""
        agent = ResearchOrchestratorAgent()
        agent.research_results = {
            "tech": {"findings": "tech findings", "sources": ["tech source"]},
            "economic": {"findings": "economic findings", "sources": ["economic source"]}
        }
        
        validation_results = {
            "tech": "verified",
            "economic": "partially verified"
        }
        
        report = agent.generate_final_report(validation_results)
        
        # Check that the report contains expected parts
        assert "FINAL RESEARCH REPORT" in report
        assert "TECH RESEARCH:" in report
        assert "tech findings" in report
        assert "tech source" in report
        assert "ECONOMIC RESEARCH:" in report
        assert "economic findings" in report
        assert "economic source" in report
        assert "Validation: verified" in report
        assert "Validation: partially verified" in report