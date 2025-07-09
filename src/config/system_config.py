"""
System Configuration Management
Handles environment variables and system settings
"""

import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class SystemConfig:
    """
    System configuration for Claude-Puppeteer WebRTC testing
    """
    # TestRail Configuration
    testrail_url: str
    testrail_username: str
    testrail_api_key: str
    
    # Pine Ridge Configuration
    pine_ridge_base_url: str
    default_channel_id: str
    pak_token: str
    
    # Claude Configuration
    claude_api_key: str
    
    # Browser Configuration
    chrome_executable_path: Optional[str] = None
    safari_executable_path: Optional[str] = None
    browser_timeout: int = 30
    
    # WebRTC Configuration
    webrtc_connection_timeout: int = 30
    audio_verification_timeout: int = 300
    
    # MCP Configuration
    mcp_server_port: int = 8000
    mcp_log_level: str = "INFO"
    
    # Execution Configuration
    max_retries: int = 3
    screenshot_quality: int = 80
    enable_verbose_logging: bool = True
    
    @classmethod
    def load_from_env(cls) -> 'SystemConfig':
        """
        Load configuration from environment variables
        """
        # Required environment variables
        required_vars = [
            'PINE_RIDGE_BASE_URL', 'PAK_TOKEN', 'CLAUDE_API_KEY'
        ]
        
        # Check for required variables
        for var in required_vars:
            if not os.getenv(var):
                print(f"⚠️  Warning: Required environment variable {var} not set")
        
        return cls(
            # TestRail Configuration (optional for now)
            testrail_url=os.getenv('TESTRAIL_URL', 'https://example.testrail.io'),
            testrail_username=os.getenv('TESTRAIL_USERNAME', 'user'),
            testrail_api_key=os.getenv('TESTRAIL_API_KEY', 'key'),
            
            # Pine Ridge Configuration
            pine_ridge_base_url=os.getenv('PINE_RIDGE_BASE_URL', 'https://pineridge-static.eng.airtime.com/'),
            default_channel_id=os.getenv('DEFAULT_CHANNEL_ID', 'QAtest'),
            pak_token=os.getenv('PAK_TOKEN', ''),
            
            # Claude Configuration
            claude_api_key=os.getenv('CLAUDE_API_KEY', ''),
            
            # Browser Configuration
            chrome_executable_path=os.getenv('CHROME_EXECUTABLE_PATH'),
            safari_executable_path=os.getenv('SAFARI_EXECUTABLE_PATH'),
            browser_timeout=int(os.getenv('BROWSER_TIMEOUT', '30')),
            
            # WebRTC Configuration
            webrtc_connection_timeout=int(os.getenv('WEBRTC_CONNECTION_TIMEOUT', '30')),
            audio_verification_timeout=int(os.getenv('AUDIO_VERIFICATION_TIMEOUT', '300')),
            
            # MCP Configuration
            mcp_server_port=int(os.getenv('MCP_SERVER_PORT', '8000')),
            mcp_log_level=os.getenv('MCP_LOG_LEVEL', 'INFO'),
            
            # Execution Configuration
            max_retries=int(os.getenv('MAX_RETRIES', '3')),
            screenshot_quality=int(os.getenv('SCREENSHOT_QUALITY', '80')),
            enable_verbose_logging=os.getenv('ENABLE_VERBOSE_LOGGING', 'true').lower() == 'true'
        )