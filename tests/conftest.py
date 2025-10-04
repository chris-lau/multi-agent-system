"""
Pytest configuration and fixtures for the Multi-Agent Research & Analysis System
"""
import os
import pytest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__))))

from llm_interface import GeminiLLMInterface
from tools.tool_framework import ToolRegistry
from tools.tool_execution_service import ToolExecutionService


@pytest.fixture
def mock_api_key():
    """Fixture to temporarily set a mock API key for tests"""
    original_api_key = os.environ.get('GOOGLE_API_KEY')
    os.environ['GOOGLE_API_KEY'] = 'test-api-key'
    original_model = os.environ.get('GEMINI_MODEL')
    os.environ['GEMINI_MODEL'] = 'gemini-pro'
    
    yield
    
    # Restore original values after test
    if original_api_key:
        os.environ['GOOGLE_API_KEY'] = original_api_key
    elif 'GOOGLE_API_KEY' in os.environ:
        del os.environ['GOOGLE_API_KEY']
    
    if original_model:
        os.environ['GEMINI_MODEL'] = original_model
    elif 'GEMINI_MODEL' in os.environ:
        del os.environ['GEMINI_MODEL']


@pytest.fixture
def mock_genai():
    """Fixture to mock the genai module"""
    with patch('llm_interface.genai') as mock_genai:
        # Set up basic mock return values
        mock_model_instance = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model_instance
        mock_response = MagicMock()
        mock_response.text = '{"findings": "test findings", "sources": ["source1"], "confidence": 0.9}'
        mock_model_instance.generate_content.return_value = mock_response
        
        yield mock_genai, mock_model_instance, mock_response


@pytest.fixture
def llm_interface_with_api_key(mock_api_key):
    """Fixture for LLM interface with mocked API key"""
    with patch('llm_interface.genai') as mock_genai:
        # Set up basic mock return values
        mock_model_instance = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model_instance
        mock_response = MagicMock()
        mock_response.text = '{"findings": "test findings", "sources": ["source1"], "confidence": 0.9}'
        mock_model_instance.generate_content.return_value = mock_response
        
        llm_interface = GeminiLLMInterface()
        llm_interface.model = mock_model_instance  # Directly assign the mock model
        return llm_interface


@pytest.fixture
def llm_interface_without_api_key():
    """Fixture for LLM interface without API key (uses mock responses)"""
    original_api_key = os.environ.get('GOOGLE_API_KEY')
    if 'GOOGLE_API_KEY' in os.environ:
        del os.environ['GOOGLE_API_KEY']
    
    llm_interface = GeminiLLMInterface()
    
    # Restore original API key if it existed
    if original_api_key:
        os.environ['GOOGLE_API_KEY'] = original_api_key
    
    return llm_interface


@pytest.fixture
def tool_registry():
    """Fixture for a fresh tool registry instance"""
    return ToolRegistry()


@pytest.fixture
def tool_execution_service(tool_registry):
    """Fixture for tool execution service with registry"""
    return ToolExecutionService(tool_registry)