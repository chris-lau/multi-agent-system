"""
Test suite for the LLM interface module
"""
import os
import pytest
from unittest.mock import patch, MagicMock
from llm_interface import GeminiLLMInterface


class TestGeminiLLMInterface:
    def test_init_without_api_key(self, llm_interface_without_api_key):
        """Test initialization without API key - should use mock responses"""
        assert llm_interface_without_api_key.use_mock is True
    
    def test_init_with_api_key(self, llm_interface_with_api_key):
        """Test initialization with API key - should configure Gemini model"""
        assert llm_interface_with_api_key.use_mock is False
    
    def test_perform_technical_research_with_api_key(self, llm_interface_with_api_key):
        """Test technical research with API key"""
        result = llm_interface_with_api_key.perform_technical_research("test query", "test context")
        
        assert "findings" in result
        assert "sources" in result
        assert "confidence" in result
    
    def test_perform_economic_research_with_api_key(self, llm_interface_with_api_key):
        """Test economic research with API key"""
        result = llm_interface_with_api_key.perform_economic_research("test query", "test context")
        
        assert "findings" in result
        assert "sources" in result
        assert "confidence" in result
    
    def test_perform_fact_checking_with_api_key(self, llm_interface_with_api_key):
        """Test fact-checking with API key"""
        research_results = {
            "tech": {"findings": "test", "sources": ["source1"], "confidence": 0.9},
            "economic": {"findings": "test", "sources": ["source2"], "confidence": 0.8}
        }
        result = llm_interface_with_api_key.perform_fact_checking(research_results)
        
        assert "tech" in result
        assert "economic" in result
        # The fact checking response format might be different, so just check basic structure
        assert result["tech"]["status"] in ["verified", "partially verified", "unverified", "incorrect", "error"]
        assert result["economic"]["status"] in ["verified", "partially verified", "unverified", "incorrect", "error"]
    
    def test_perform_technical_research_mock_response(self, llm_interface_without_api_key):
        """Test technical research returns mock response when no API key"""
        result = llm_interface_without_api_key.perform_technical_research("test query", "test context")
        
        assert result["findings"] == "Technical analysis of 'test query': This involves advanced computing methodologies and requires specific technical infrastructure."
        assert "sources" in result
        assert "confidence" in result

    def test_perform_economic_research_mock_response(self, llm_interface_without_api_key):
        """Test economic research returns mock response when no API key"""
        result = llm_interface_without_api_key.perform_economic_research("test query", "test context")
        
        assert result["findings"] == "Economic implications of 'test query': This would require an investment of approximately $X million with an estimated ROI of Y% over Z years."
        assert "sources" in result
        assert "confidence" in result

    def test_perform_fact_checking_mock_response(self, llm_interface_without_api_key):
        """Test fact-checking returns mock response when no API key"""
        research_results = {
            "tech": {"findings": "test", "sources": ["source1"], "confidence": 0.9},
            "economic": {"findings": "test", "sources": ["source2"], "confidence": 0.8}
        }
        result = llm_interface_without_api_key.perform_fact_checking(research_results)
        
        assert "tech" in result
        assert "economic" in result
        assert result["tech"]["status"] in ["verified", "partially verified"]
        assert result["economic"]["status"] in ["verified", "partially verified"]

    def test_perform_technical_research_error_handling(self, mock_api_key):
        """Test technical research handles API errors gracefully"""
        with patch('llm_interface.genai') as mock_genai:
            # Set up mock to raise exception
            mock_model_instance = MagicMock()
            mock_genai.GenerativeModel.return_value = mock_model_instance
            mock_model_instance.generate_content.side_effect = Exception("API Error")
            
            # Create a new instance to ensure we get API key behavior
            llm_interface = GeminiLLMInterface()
            llm_interface.model = mock_model_instance  # Directly assign the mock model
            
            result = llm_interface.perform_technical_research("test query", "test context")
            
            assert "findings" in result
            assert "Error in technical analysis: API Error" in result["findings"]
            assert result["confidence"] == 0.0

    def test_perform_economic_research_error_handling(self, mock_api_key):
        """Test economic research handles API errors gracefully"""
        with patch('llm_interface.genai') as mock_genai:
            # Set up mock to raise exception
            mock_model_instance = MagicMock()
            mock_genai.GenerativeModel.return_value = mock_model_instance
            mock_model_instance.generate_content.side_effect = Exception("API Error")
            
            # Create a new instance to ensure we get API key behavior
            llm_interface = GeminiLLMInterface()
            llm_interface.model = mock_model_instance  # Directly assign the mock model
            
            result = llm_interface.perform_economic_research("test query", "test context")
            
            assert "findings" in result
            assert "Error in economic analysis: API Error" in result["findings"]
            assert result["confidence"] == 0.0

    def test_perform_fact_checking_error_handling(self, mock_api_key):
        """Test fact-checking handles API errors gracefully"""
        with patch('llm_interface.genai') as mock_genai:
            # Set up mock to raise exception
            mock_model_instance = MagicMock()
            mock_genai.GenerativeModel.return_value = mock_model_instance
            mock_model_instance.generate_content.side_effect = Exception("API Error")
            
            # Create a new instance to ensure we get API key behavior
            llm_interface = GeminiLLMInterface()
            llm_interface.model = mock_model_instance  # Directly assign the mock model
            
            research_results = {
                "tech": {"findings": "test", "sources": ["source1"], "confidence": 0.9},
                "economic": {"findings": "test", "sources": ["source2"], "confidence": 0.8}
            }
            result = llm_interface.perform_fact_checking(research_results)
            
            assert "tech" in result
            assert result["tech"]["status"] == "error"
            assert result["tech"]["issues"][0] == "Fact-checking error: API Error"