"""
Configuration management for tools in the Multi-Agent Research System
"""
import json
import os
from typing import Dict, Any, Optional


class ToolConfig:
    """Configuration management for individual tools"""
    
    def __init__(self, tool_name: str, config_file_path: str = "config/tools_config.json"):
        self.tool_name = tool_name
        self.config_file_path = config_file_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r') as f:
                all_configs = json.load(f)
                return all_configs.get(self.tool_name, {})
        return {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value by key"""
        self.config[key] = value
        self._save_config()
    
    def _save_config(self):
        """Save configuration to file"""
        all_configs = {}
        if os.path.exists(self.config_file_path):
            with open(self.config_file_path, 'r') as f:
                all_configs = json.load(f)
        
        all_configs[self.tool_name] = self.config
        
        # Ensure the config directory exists
        os.makedirs(os.path.dirname(self.config_file_path), exist_ok=True)
        
        with open(self.config_file_path, 'w') as f:
            json.dump(all_configs, f, indent=2)


# Default configuration values that would be used if no config file exists
DEFAULT_CONFIGS = {
    "web_search_tool": {
        "default_num_results": 5,
        "enable_caching": True,
        "cache_duration_minutes": 60,
        "timeout_seconds": 30
    },
    "document_parser_tool": {
        "supported_formats": ["pdf", "docx", "txt", "rtf"],
        "max_file_size_mb": 10,
        "enable_caching": True,
        "cache_duration_minutes": 1440  # 24 hours
    },
    "statistical_analysis_tool": {
        "max_data_points": 10000,
        "precision": 2,
        "supported_analysis_types": ["descriptive", "correlation"]
    }
}