"""
Unit tests for statistical_analysis_tool.py to improve test coverage
"""
import sys
import os
from unittest.mock import Mock, patch
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.statistical_analysis_tool.statistical_analysis_tool import StatisticalAnalysisTool


class TestStatisticalAnalysisTool:
    """Test cases for StatisticalAnalysisTool class"""
    
    def test_init(self):
        """Test StatisticalAnalysisTool initialization"""
        tool = StatisticalAnalysisTool()
        
        assert tool.tool_id == "statistical-analysis"
        assert tool.name == "Statistical Analysis Tool"
        assert tool.description == "Performs statistical analysis on provided data"
        assert tool.category == "data-analysis"
        assert tool.config is not None
    
    def test_get_params_definition(self):
        """Test parameter definition for StatisticalAnalysisTool"""
        tool = StatisticalAnalysisTool()
        params_def = tool.get_params_definition()
        
        assert "data" in params_def
        assert params_def["data"]["type"] == "array"
        assert params_def["data"]["required"] == True
        assert "analysis_type" in params_def
        assert params_def["analysis_type"]["type"] == "string"
        assert params_def["analysis_type"]["required"] == False
        assert params_def["analysis_type"]["default"] == "descriptive"
        assert "enum" in params_def["analysis_type"]
        assert "max_items" in params_def["data"]
    
    def test_get_params_definition_with_custom_analysis_types(self):
        """Test parameter definition with custom supported analysis types from config"""
        tool = StatisticalAnalysisTool()
        # Manually set a custom config value to test
        tool.config.set("supported_analysis_types", ["descriptive", "correlation", "regression"])
        
        params_def = tool.get_params_definition()
        assert params_def["analysis_type"]["enum"] == ["descriptive", "correlation", "regression"]
        assert "descriptive, correlation, regression" in params_def["analysis_type"]["description"]
    
    def test_get_params_definition_with_custom_max_items(self):
        """Test parameter definition with custom max_data_points from config"""
        tool = StatisticalAnalysisTool()
        # Manually set a custom config value to test
        tool.config.set("max_data_points", 5000)
        
        params_def = tool.get_params_definition()
        assert params_def["data"]["max_items"] == 5000
    
    @patch('builtins.print')
    def test_execute(self, mock_print):
        """Test execution of StatisticalAnalysisTool with data"""
        tool = StatisticalAnalysisTool()
        data = [1, 2, 3, 4, 5]
        result = tool.execute(data=data, analysis_type="descriptive")
        
        # Verify print was called
        mock_print.assert_called_once_with(f"Performing descriptive analysis on data with {len(data)} values")
        
        # Verify result structure
        assert result["analysis_type"] == "descriptive"
        assert result["input_data"] == data
        assert "statistics" in result
        
        stats = result["statistics"]
        assert stats["count"] == 5
        assert stats["mean"] == 3.0  # (1+2+3+4+5)/5
        assert stats["min"] == 1
        assert stats["max"] == 5
        assert stats["range"] == 4  # 5-1
    
    @patch('builtins.print')
    def test_execute_empty_data(self, mock_print):
        """Test execution of StatisticalAnalysisTool with empty data"""
        tool = StatisticalAnalysisTool()
        data = []
        result = tool.execute(data=data)
        
        # Verify print was called
        mock_print.assert_called_once_with("Performing descriptive analysis on data with 0 values")
        
        # Verify result structure
        stats = result["statistics"]
        assert stats["count"] == 0
        assert stats["mean"] == 0
        assert stats["min"] == 0
        assert stats["max"] == 0
        assert stats["range"] == 0
    
    @patch('builtins.print')
    def test_execute_with_custom_analysis_type(self, mock_print):
        """Test execution with a custom analysis type"""
        tool = StatisticalAnalysisTool()
        data = [10, 20, 30]
        result = tool.execute(data=data, analysis_type="correlation")
        
        # Verify print was called with the custom analysis type
        mock_print.assert_called_once_with("Performing correlation analysis on data with 3 values")
        
        # Verify result structure
        assert result["analysis_type"] == "correlation"
        assert result["input_data"] == data
        assert "statistics" in result
    
    @patch('builtins.print')
    def test_execute_single_data_point(self, mock_print):
        """Test execution with a single data point"""
        tool = StatisticalAnalysisTool()
        data = [42]
        result = tool.execute(data=data)
        
        # Verify print was called
        mock_print.assert_called_once_with("Performing descriptive analysis on data with 1 values")
        
        # Verify result structure
        stats = result["statistics"]
        assert stats["count"] == 1
        assert stats["mean"] == 42
        assert stats["min"] == 42
        assert stats["max"] == 42
        assert stats["range"] == 0  # 42-42