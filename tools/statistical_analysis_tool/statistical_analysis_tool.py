"""
Statistical Analysis Tool for the Multi-Agent Research System
"""
from tools.tool_framework import Tool
from tools.config.tool_config import ToolConfig, DEFAULT_CONFIGS
from typing import Dict, Any


class StatisticalAnalysisTool(Tool):
    """Tool for performing statistical analysis - example implementation"""
    
    def __init__(self):
        super().__init__(
            tool_id="statistical-analysis",
            name="Statistical Analysis Tool",
            description="Performs statistical analysis on provided data",
            category="data-analysis"
        )
        self.config = ToolConfig("statistical_analysis_tool")
        # Use default config if no specific config is set
        for key, value in DEFAULT_CONFIGS["statistical_analysis_tool"].items():
            if self.config.get(key) is None:
                self.config.set(key, value)
    
    def get_params_definition(self):
        supported_analysis_types = self.config.get("supported_analysis_types", ["descriptive"])
        return {
            "data": {
                "type": "array",
                "required": True,
                "description": "Array of numerical values to analyze",
                "max_items": self.config.get("max_data_points", 10000)
            },
            "analysis_type": {
                "type": "string",
                "required": False,
                "default": "descriptive",
                "enum": supported_analysis_types,
                "description": f"Type of analysis to perform ({', '.join(supported_analysis_types)})"
            }
        }
    
    def execute(self, **params) -> Dict[str, Any]:
        data = params.get("data", [])
        analysis_type = params.get("analysis_type", "descriptive")
        
        print(f"Performing {analysis_type} analysis on data with {len(data)} values")
        
        # Mock statistical analysis
        if data:
            mean_val = sum(data) / len(data)
            min_val = min(data)
            max_val = max(data)
        else:
            mean_val, min_val, max_val = 0, 0, 0
        
        return {
            "analysis_type": analysis_type,
            "input_data": data,
            "statistics": {
                "count": len(data),
                "mean": mean_val,
                "min": min_val,
                "max": max_val,
                "range": max_val - min_val if data else 0
            }
        }