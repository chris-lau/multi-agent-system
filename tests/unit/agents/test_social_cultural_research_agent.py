"""
Unit tests for social_cultural_research_agent.py to improve test coverage
"""
import sys
import os
from unittest.mock import Mock, patch
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.social_cultural_research_agent.social_cultural_research_agent import SocialCulturalResearchAgent
from a2a_protocol import A2AMessage, MessageType


class TestSocialCulturalResearchAgent:
    """Test cases for SocialCulturalResearchAgent class"""
    
    def test_init(self):
        """Test SocialCulturalResearchAgent initialization"""
        agent = SocialCulturalResearchAgent()
        
        assert agent.agent_id == "social-cultural-research-agent"
        assert agent.client is not None
        assert agent.supported_message_types == [
            MessageType.REQUEST_RESEARCH_TASK.value,
            MessageType.RESPONSE_TOOL_RESULT.value
        ]
    
    def test_get_capabilities(self):
        """Test get_capabilities method returns correct structure"""
        agent = SocialCulturalResearchAgent()
        capabilities = agent.get_capabilities()
        
        assert "id" in capabilities
        assert "name" in capabilities
        assert "description" in capabilities
        assert "supportedMessageTypes" in capabilities
        assert capabilities["id"] == "social-cultural-research-agent"
        assert capabilities["name"] == "Social/Cultural Research Agent"
    
    @patch('builtins.print')
    def test_receive_message_unknown_type(self, mock_print):
        """Test handling of unknown message types"""
        agent = SocialCulturalResearchAgent()
        message = A2AMessage.create_message(
            MessageType.REQUEST_FACTCHECK_VERIFY,  # Using existing message type and changing it
            "test-sender",
            "social-cultural-research-agent",
            {}
        )
        message.type = "unknown-type"  # Override type to simulate unknown type
        
        agent.receive_message(message)
        
        mock_print.assert_called_with("Social/Cultural Research Agent: Unknown message type received: unknown-type")
    
    @patch('agents.social_cultural_research_agent.social_cultural_research_agent.SocialCulturalResearchAgent.handle_research_task')
    @patch('builtins.print')
    def test_receive_message_research_task(self, mock_print, mock_handle_research_task):
        """Test handling of research task messages"""
        agent = SocialCulturalResearchAgent()
        message = A2AMessage.create_message(
            MessageType.REQUEST_RESEARCH_TASK,
            "research-orchestrator-agent",
            "social-cultural-research-agent",
            {}
        )
        
        agent.receive_message(message)
        
        mock_print.assert_called_with("Social/Cultural Research Agent received message of type: request:research:task")
        mock_handle_research_task.assert_called_once_with(message)
    
    @patch('agents.social_cultural_research_agent.social_cultural_research_agent.SocialCulturalResearchAgent.handle_tool_result')
    @patch('builtins.print')
    def test_receive_message_tool_result(self, mock_print, mock_handle_tool_result):
        """Test handling of tool result messages"""
        agent = SocialCulturalResearchAgent()
        message = A2AMessage.create_message(
            MessageType.RESPONSE_TOOL_RESULT,
            "tool-service",
            "social-cultural-research-agent",
            {}
        )
        
        agent.receive_message(message)
        
        mock_print.assert_called_with("Social/Cultural Research Agent received message of type: response:tool-result")
        mock_handle_tool_result.assert_called_once_with(message)
    
    @patch('agents.social_cultural_research_agent.social_cultural_research_agent.SocialCulturalResearchAgent.perform_social_cultural_research')
    @patch('builtins.print')
    def test_handle_research_task(self, mock_print, mock_perform_research):
        """Test handling of research tasks"""
        agent = SocialCulturalResearchAgent()
        
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
            "social-cultural-research-agent",
            {
                "query": "test query",
                "context": "research the social aspects of this query"
            }
        )
        
        agent.handle_research_task(message)
        
        # Verify that perform_social_cultural_research was called with the right data
        mock_perform_research.assert_called_once_with("test query", "research the social aspects of this query")
        
        # Verify that send_message was called (which means a response was sent)
        assert agent.client.send_message.called
    
    @patch('builtins.print')
    def test_handle_tool_result(self, mock_print):
        """Test handling of tool results"""
        agent = SocialCulturalResearchAgent()
        message = A2AMessage.create_message(
            MessageType.RESPONSE_TOOL_RESULT,
            "tool-service",
            "social-cultural-research-agent",
            {
                "tool_id": "web-search-tool",
                "result": {"data": "test result"}
            }
        )
        
        agent.handle_tool_result(message)
        
        mock_print.assert_any_call("Social/Cultural Research Agent received tool result from web-search-tool: {'data': 'test result'}")
    
    @patch('llm_interface.GeminiLLMInterface')
    def test_perform_social_cultural_research(self, mock_llm_interface):
        """Test the perform_social_cultural_research method"""
        agent = SocialCulturalResearchAgent()
        
        mock_llm_instance = Mock()
        expected_result = {"status": "completed", "findings": "test findings"}
        mock_llm_instance.perform_social_cultural_research.return_value = expected_result
        agent.llm_interface = mock_llm_instance
        
        query = "social impact of AI"
        context = "analyze social aspects"
        result = agent.perform_social_cultural_research(query, context)
        
        mock_llm_instance.perform_social_cultural_research.assert_called_once_with(query, context)
        assert result == expected_result

    @patch('time.sleep')
    @patch('agents.social_cultural_research_agent.social_cultural_research_agent.SocialCulturalResearchAgent.perform_social_cultural_research')
    def test_perform_research_with_retry_success_on_second_attempt(self, mock_perform_research, mock_sleep):
        """Test retry mechanism - succeeds on second attempt"""
        agent = SocialCulturalResearchAgent()
        
        # Configure mock to fail first, then succeed
        mock_perform_research.side_effect = [
            Exception("First attempt failed"),
            {"result": "success"}
        ]
        
        query = "test query"
        context = "test context"
        
        result = agent._perform_research_with_retry(query, context)
        
        # Should have called perform_social_cultural_research twice
        assert mock_perform_research.call_count == 2
        # Should have called sleep once (between attempts)
        assert mock_sleep.call_count == 1
        # Should return the success result
        assert result == {"result": "success"}

    @patch('time.sleep')
    @patch('agents.social_cultural_research_agent.social_cultural_research_agent.SocialCulturalResearchAgent.perform_social_cultural_research')
    def test_perform_research_with_retry_all_failures(self, mock_perform_research, mock_sleep):
        """Test retry mechanism - fails after all attempts"""
        agent = SocialCulturalResearchAgent()
        agent.max_retries = 3  # Ensure agent uses 3 retries in test
        
        # Configure mock to fail every time
        mock_perform_research.side_effect = Exception("Always fails")
        
        query = "test query"
        context = "test context"
        
        result = agent._perform_research_with_retry(query, context)
        
        # Should have called perform_social_cultural_research max_retries times
        assert mock_perform_research.call_count == 3
        # Should have called sleep twice (between 3 attempts)
        assert mock_sleep.call_count == 2
        # Should return None when all attempts fail
        assert result is None

    @patch('time.sleep')
    @patch('builtins.print')
    def test_send_message_with_retry_success_on_second_attempt(self, mock_print, mock_sleep):
        """Test retry mechanism for sending messages - succeeds on second attempt"""
        agent = SocialCulturalResearchAgent()
        
        # Mock the client to fail first, then succeed 
        mock_client = Mock()
        mock_client.send_message.side_effect = [
            Exception("First send failed"),
            True  # Second send succeeds
        ]
        agent.client = mock_client
        
        mock_message = Mock()
        
        result = agent._send_message_with_retry("receiver-id", mock_message)
        
        # Should have called send_message twice
        assert mock_client.send_message.call_count == 2
        # Should have called sleep once
        assert mock_sleep.call_count == 1
        # Should return the success result
        assert result is True

    @patch('time.sleep')
    def test_send_message_with_retry_all_failures(self, mock_sleep):
        """Test retry mechanism for sending messages - fails after all attempts"""
        agent = SocialCulturalResearchAgent()
        agent.max_retries = 3  # Ensure agent uses 3 retries in test
        
        # Mock the client to fail every time
        mock_client = Mock()
        mock_client.send_message.side_effect = Exception("Always fails")
        agent.client = mock_client
        
        mock_message = Mock()
        
        result = agent._send_message_with_retry("receiver-id", mock_message)
        
        # Should have called send_message max_retries times
        assert mock_client.send_message.call_count == 3
        # Should have called sleep twice (between 3 attempts)
        assert mock_sleep.call_count == 2
        # Should return None when all attempts fail
        assert result is None

    @patch('builtins.print')
    def test_receive_message_with_error_handling(self, mock_print):
        """Test error handling in receive_message method"""
        agent = SocialCulturalResearchAgent()
        
        # Create a message that will cause an exception when processed
        message = A2AMessage.create_message(
            MessageType.REQUEST_RESEARCH_TASK,
            "test-sender",
            "social-cultural-research-agent",
            {}
        )
        
        # Mock handle_research_task to raise an exception
        with patch.object(agent, 'handle_research_task', side_effect=Exception("Processing error")):
            # This should not raise an exception due to error handling
            agent.receive_message(message)
            
            # Verify that error was logged/printed
            error_call_found = any("Error processing message" in str(call) for call in mock_print.call_args_list)
            assert error_call_found
    
    @patch('builtins.print')
    def test_send_tool_request(self, mock_print):
        """Test sending tool requests"""
        agent = SocialCulturalResearchAgent()
        agent.client.send_message = Mock()
        
        agent.send_tool_request("web-search", {"query": "social implications"}, "tool-service")
        
        # Verify that send_message was called once
        assert agent.client.send_message.called
        mock_print.assert_called_with("Social/Cultural Research Agent requesting tool execution: web-search")