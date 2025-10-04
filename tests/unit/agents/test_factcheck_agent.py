"""
Unit tests for factcheck_agent.py to improve test coverage
"""
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.factcheck_agent.factcheck_agent import FactCheckAgent
from a2a_protocol import A2AMessage, MessageType


class TestFactCheckAgent:
    """Test cases for FactCheckAgent class"""
    
    def test_init(self):
        """Test FactCheckAgent initialization"""
        agent = FactCheckAgent()
        
        assert agent.agent_id == "factcheck-agent"
        assert agent.client is not None
        assert agent.supported_message_types == [
            MessageType.REQUEST_FACTCHECK_VERIFY.value,
            MessageType.RESPONSE_TOOL_RESULT.value
        ]
    
    def test_get_capabilities(self):
        """Test get_capabilities method returns correct structure"""
        agent = FactCheckAgent()
        capabilities = agent.get_capabilities()
        
        assert "id" in capabilities
        assert "name" in capabilities
        assert "description" in capabilities
        assert "supportedMessageTypes" in capabilities  # Changed from supported_message_types to supportedMessageTypes
        assert capabilities["id"] == "factcheck-agent"
        assert capabilities["name"] == "Fact-Checking Agent"
    
    @patch('builtins.print')
    def test_receive_message_unknown_type(self, mock_print):
        """Test handling of unknown message types"""
        agent = FactCheckAgent()
        message = A2AMessage.create_message(
            MessageType.REQUEST_RESEARCH_TASK,  # Using existing message type and changing it
            "test-sender",
            "factcheck-agent",
            {}
        )
        message.type = "unknown-type"  # Override type to simulate unknown type
        
        agent.receive_message(message)
        
        mock_print.assert_called_with("Fact-Check Agent: Unknown message type received: unknown-type")
    
    @patch('agents.factcheck_agent.factcheck_agent.FactCheckAgent.handle_verification_request')
    @patch('builtins.print')
    def test_receive_message_verification_request(self, mock_print, mock_handle_verification):
        """Test handling of verification request messages"""
        agent = FactCheckAgent()
        message = A2AMessage.create_message(
            MessageType.REQUEST_FACTCHECK_VERIFY,
            "test-sender",
            "factcheck-agent",
            {}
        )
        
        agent.receive_message(message)
        
        mock_print.assert_called_with("Fact-Check Agent received message of type: request:factcheck:verify")
        mock_handle_verification.assert_called_once_with(message)
    
    @patch('agents.factcheck_agent.factcheck_agent.FactCheckAgent.handle_tool_result')
    @patch('builtins.print')
    def test_receive_message_tool_result(self, mock_print, mock_handle_tool_result):
        """Test handling of tool result messages"""
        agent = FactCheckAgent()
        message = A2AMessage.create_message(
            MessageType.RESPONSE_TOOL_RESULT,
            "test-sender",
            "factcheck-agent",
            {}
        )
        
        agent.receive_message(message)
        
        mock_print.assert_called_with("Fact-Check Agent received message of type: response:tool-result")
        mock_handle_tool_result.assert_called_once_with(message)
    
    @patch('agents.factcheck_agent.factcheck_agent.FactCheckAgent.perform_fact_checking')
    @patch('builtins.print')
    def test_handle_verification_request(self, mock_print, mock_perform_fact_checking):
        """Test handling of verification requests"""
        agent = FactCheckAgent()
        
        # Mock the LLM interface and client
        agent.client.send_message = Mock()
        mock_perform_fact_checking.return_value = {
            "status": "verified",
            "confidence": 0.95,
            "sources": ["source1"]
        }
        
        message = A2AMessage.create_message(
            MessageType.REQUEST_FACTCHECK_VERIFY,
            "orchestrator-agent",
            "factcheck-agent",
            {"research_results": {"test": "data"}}
        )
        
        agent.handle_verification_request(message)
        
        # Verify that perform_fact_checking was called with the right data
        mock_perform_fact_checking.assert_called_once_with({"test": "data"})
        
        # Verify that send_message was called (which means a response was sent)
        assert agent.client.send_message.called
    
    @patch('builtins.print')
    def test_handle_tool_result(self, mock_print):
        """Test handling of tool results"""
        agent = FactCheckAgent()
        message = A2AMessage.create_message(
            MessageType.RESPONSE_TOOL_RESULT,
            "test-sender",
            "factcheck-agent",
            {
                "tool_id": "web-search-tool",
                "result": {"data": "test result"}
            }
        )
        
        agent.handle_tool_result(message)
        
        mock_print.assert_any_call("Fact-Check Agent received tool result from web-search-tool: {'data': 'test result'}")
    
    @patch('llm_interface.GeminiLLMInterface')
    def test_perform_fact_checking(self, mock_llm_interface):
        """Test the perform_fact_checking method"""
        agent = FactCheckAgent()
        
        mock_llm_instance = Mock()
        expected_result = {"status": "verified", "confidence": 0.9}
        mock_llm_instance.perform_fact_checking.return_value = expected_result
        agent.llm_interface = mock_llm_instance
        
        research_results = {"claim": "test claim", "evidence": ["evidence1"]}
        result = agent.perform_fact_checking(research_results)
        
        mock_llm_instance.perform_fact_checking.assert_called_once_with(research_results)
        assert result == expected_result

    @patch('time.sleep')
    @patch('agents.factcheck_agent.factcheck_agent.FactCheckAgent.perform_fact_checking')
    def test_perform_fact_checking_with_retry_success_on_second_attempt(self, mock_perform_fact_checking, mock_sleep):
        """Test retry mechanism for fact-checking - succeeds on second attempt"""
        agent = FactCheckAgent()
        
        # Configure mock to fail first, then succeed
        mock_perform_fact_checking.side_effect = [
            Exception("First attempt failed"),
            {"result": "success"}
        ]
        
        research_results = {"test": "data"}
        
        result = agent._perform_fact_checking_with_retry(research_results)
        
        # Should have called perform_fact_checking twice
        assert mock_perform_fact_checking.call_count == 2
        # Should have called sleep once (between attempts)
        assert mock_sleep.call_count == 1
        # Should return the success result
        assert result == {"result": "success"}

    @patch('time.sleep')
    @patch('agents.factcheck_agent.factcheck_agent.FactCheckAgent.perform_fact_checking')
    def test_perform_fact_checking_with_retry_all_failures(self, mock_perform_fact_checking, mock_sleep):
        """Test retry mechanism for fact-checking - fails after all attempts"""
        agent = FactCheckAgent()
        agent.max_retries = 3  # Ensure agent uses 3 retries in test
        
        # Configure mock to fail every time
        mock_perform_fact_checking.side_effect = Exception("Always fails")
        
        research_results = {"test": "data"}
        
        result = agent._perform_fact_checking_with_retry(research_results)
        
        # Should have called perform_fact_checking max_retries times
        assert mock_perform_fact_checking.call_count == 3
        # Should have called sleep twice (between 3 attempts)
        assert mock_sleep.call_count == 2
        # Should return None when all attempts fail
        assert result is None

    @patch('time.sleep')
    @patch('builtins.print')
    def test_send_message_with_retry_success_on_second_attempt(self, mock_print, mock_sleep):
        """Test retry mechanism for sending messages - succeeds on second attempt"""
        agent = FactCheckAgent()
        
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
        agent = FactCheckAgent()
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
        agent = FactCheckAgent()
        
        # Create a message that will cause an exception when processed
        message = A2AMessage.create_message(
            MessageType.REQUEST_FACTCHECK_VERIFY,
            "test-sender",
            "factcheck-agent",
            {}
        )
        
        # Mock handle_verification_request to raise an exception
        with patch.object(agent, 'handle_verification_request', side_effect=Exception("Processing error")):
            # This should not raise an exception due to error handling
            agent.receive_message(message)
            
            # Verify that error was logged/printed
            error_call_found = any("Error processing message" in str(call) for call in mock_print.call_args_list)
            assert error_call_found

    @patch('builtins.print')
    def test_send_tool_request(self, mock_print):
        """Test sending tool requests"""
        agent = FactCheckAgent()
        agent.client.send_message = Mock()
        
        agent.send_tool_request("web-search-tool", {"query": "test query"}, "tool-service")
        
        # Verify that send_message was called once
        assert agent.client.send_message.called
        mock_print.assert_called_with("Fact-Check Agent requesting tool execution: web-search-tool")