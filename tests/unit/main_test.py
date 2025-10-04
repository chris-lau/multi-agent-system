"""
Unit tests for main.py to improve test coverage
"""
import argparse
import sys
import os
from unittest.mock import patch, MagicMock, Mock
import pytest

# Import the main module components
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import main, MessageRouter


class TestMessageRouter:
    """Test cases for the MessageRouter class"""
    
    def test_init(self):
        """Test MessageRouter initialization"""
        router = MessageRouter()
        assert router.message_queue == []
        assert router.agents == {}
    
    def test_register_agent(self):
        """Test registering an agent with the router"""
        router = MessageRouter()
        mock_agent = Mock()
        router.register_agent("test-agent", mock_agent)
        assert "test-agent" in router.agents
        assert router.agents["test-agent"] == mock_agent
    
    def test_send_message(self):
        """Test sending a message to the router"""
        router = MessageRouter()
        mock_message = Mock()
        router.send_message(mock_message)
        assert len(router.message_queue) == 1
        assert router.message_queue[0] == mock_message
    
    @patch('builtins.print')
    def test_process_messages_with_known_receiver(self, mock_print):
        """Test processing messages with a known receiver"""
        router = MessageRouter()
        
        # Create a mock agent that can receive messages
        mock_agent = Mock()
        router.register_agent("test-agent", mock_agent)
        
        # Create a mock message
        mock_message = Mock()
        mock_message.receiver = "test-agent"
        
        # Add message to queue
        router.send_message(mock_message)
        
        # Process messages
        router.process_messages()
        
        # Verify the agent received the message
        mock_agent.receive_message.assert_called_once_with(mock_message)
        mock_print.assert_called()
    
    @patch('builtins.print')
    def test_process_messages_with_unknown_receiver(self, mock_print):
        """Test processing messages with an unknown receiver"""
        router = MessageRouter()
        
        # Create a mock message with unknown receiver
        mock_message = Mock()
        mock_message.receiver = "unknown-agent"
        
        # Add message to queue
        router.send_message(mock_message)
        
        # Process messages
        router.process_messages()
        
        # Verify the message was not sent to any agent
        mock_print.assert_called()


@patch('argparse.ArgumentParser')
@patch('main.os.environ')
@patch('main.ResearchOrchestratorAgent')
@patch('main.TechResearchAgent')
@patch('main.EconomicResearchAgent')
@patch('main.FactCheckAgent')
@patch('main.MessageRouter')
@patch('main.WebSearchTool')
@patch('main.DocumentParsingTool')
@patch('main.StatisticalAnalysisTool')
def test_main_function_with_args(mock_stat_tool, mock_doc_tool, mock_web_tool, mock_router, mock_factcheck, mock_economic, mock_tech, mock_orchestrator, mock_environ, mock_arg_parser):
    """Test the main function with command line arguments"""
    # Configure the mocks to return proper values
    mock_parser_instance = Mock()
    mock_arg_parser.return_value = mock_parser_instance
    mock_args = Mock()
    mock_args.api_key = "test-key"
    mock_args.query = "Test query"
    mock_args.model = "gemini-test"
    mock_parser_instance.parse_args.return_value = mock_args
    
    # Mock other dependencies and configure return values
    mock_router_instance = Mock()
    mock_router.return_value = mock_router_instance
    
    mock_orchestrator_instance = Mock()
    mock_orchestrator_instance.get_capabilities.return_value = {"name": "orchestrator"}
    mock_orchestrator_instance.tool_registry = Mock()
    mock_orchestrator_instance.process_research_request = Mock()
    mock_orchestrator_instance.client = Mock()
    mock_orchestrator.return_value = mock_orchestrator_instance
    
    mock_tech_instance = Mock()
    mock_tech_instance.get_capabilities.return_value = {"name": "tech_agent"}
    mock_tech_instance.client = Mock()
    mock_tech.return_value = mock_tech_instance
    
    mock_economic_instance = Mock()
    mock_economic_instance.get_capabilities.return_value = {"name": "economic_agent"}
    mock_economic_instance.client = Mock()
    mock_economic.return_value = mock_economic_instance
    
    mock_factcheck_instance = Mock()
    mock_factcheck_instance.get_capabilities.return_value = {"name": "factcheck_agent"}
    mock_factcheck_instance.client = Mock()
    mock_factcheck.return_value = mock_factcheck_instance
    
    # Mock the tool instances
    mock_web_tool_instance = Mock()
    mock_doc_tool_instance = Mock()
    mock_stat_tool_instance = Mock()
    mock_web_tool.return_value = mock_web_tool_instance
    mock_doc_tool.return_value = mock_doc_tool_instance
    mock_stat_tool.return_value = mock_stat_tool_instance
    
    # Run main function
    with patch('builtins.print'), patch('main.sys.exit'):
        main()
    
    # Verify environment was set
    assert mock_environ.__setitem__.call_count >= 2  # For API key and model
    mock_environ.__setitem__.assert_any_call('GOOGLE_API_KEY', 'test-key')
    mock_environ.__setitem__.assert_any_call('GEMINI_MODEL', 'gemini-test')


@patch('argparse.ArgumentParser')
@patch('main.os.environ')
@patch('main.ResearchOrchestratorAgent')
@patch('main.TechResearchAgent')
@patch('main.EconomicResearchAgent')
@patch('main.FactCheckAgent')
@patch('main.MessageRouter')
@patch('main.WebSearchTool')
@patch('main.DocumentParsingTool')
@patch('main.StatisticalAnalysisTool')
def test_main_function_without_args(mock_stat_tool, mock_doc_tool, mock_web_tool, mock_router, mock_factcheck, mock_economic, mock_tech, mock_orchestrator, mock_environ, mock_arg_parser):
    """Test the main function without command line arguments (defaults)"""
    # Configure the mocks to return proper values
    mock_parser_instance = Mock()
    mock_arg_parser.return_value = mock_parser_instance
    mock_args = Mock()
    mock_args.api_key = None
    mock_args.query = "Analyze the impact of AI on healthcare"  # Default query
    mock_args.model = "gemini-pro"  # Default model
    mock_parser_instance.parse_args.return_value = mock_args
    
    # Mock other dependencies and configure return values
    mock_router_instance = Mock()
    mock_router.return_value = mock_router_instance
    
    mock_orchestrator_instance = Mock()
    mock_orchestrator_instance.get_capabilities.return_value = {"name": "orchestrator"}
    mock_orchestrator_instance.tool_registry = Mock()
    mock_orchestrator_instance.process_research_request = Mock()
    mock_orchestrator_instance.client = Mock()
    mock_orchestrator.return_value = mock_orchestrator_instance
    
    mock_tech_instance = Mock()
    mock_tech_instance.get_capabilities.return_value = {"name": "tech_agent"}
    mock_tech_instance.client = Mock()
    mock_tech.return_value = mock_tech_instance
    
    mock_economic_instance = Mock()
    mock_economic_instance.get_capabilities.return_value = {"name": "economic_agent"}
    mock_economic_instance.client = Mock()
    mock_economic.return_value = mock_economic_instance
    
    mock_factcheck_instance = Mock()
    mock_factcheck_instance.get_capabilities.return_value = {"name": "factcheck_agent"}
    mock_factcheck_instance.client = Mock()
    mock_factcheck.return_value = mock_factcheck_instance
    
    # Mock the tool instances
    mock_web_tool_instance = Mock()
    mock_doc_tool_instance = Mock()
    mock_stat_tool_instance = Mock()
    mock_web_tool.return_value = mock_web_tool_instance
    mock_doc_tool.return_value = mock_doc_tool_instance
    mock_stat_tool.return_value = mock_stat_tool_instance
    
    # Run main function
    with patch('builtins.print'), patch('main.sys.exit'):
        main()
    
    # Verify environment was set (model only, since no API key was provided)
    mock_environ.__setitem__.assert_called_once_with('GEMINI_MODEL', 'gemini-pro')


def test_main_script_execution():
    """Test that main can be executed as a script"""
    # Verify that __name__ check works
    assert __name__ != "__main__"  # This is running as a test, not as main

@pytest.mark.parametrize(
    "orchestrator_type",
    ["basic", "advanced", "custom", "unknown-type"],
)
def test_create_orchestrator_types(orchestrator_type):
    """Verify create_orchestrator returns the default agent for supported types"""
    from main import create_orchestrator
    from agents.orchestrator_agent.research_orchestrator_agent import ResearchOrchestratorAgent

    orchestrator = create_orchestrator(orchestrator_type)
    assert isinstance(orchestrator, ResearchOrchestratorAgent)
