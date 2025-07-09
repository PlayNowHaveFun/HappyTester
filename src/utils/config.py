"""
Configuration management for Pine Ridge test automation
"""

import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """Configuration manager for test automation settings"""
    
    def __init__(self):
        # Load environment variables from .env file
        env_path = Path(__file__).parent.parent.parent / ".env"
        load_dotenv(env_path)
        
        # Pine Ridge Application Settings
        self.pine_ridge_base_url = os.getenv("PINE_RIDGE_BASE_URL", "https://pineridge-static.eng.airtime.com/")
        self.default_channel_id = os.getenv("DEFAULT_CHANNEL_ID", "QAtest")
        self.pak_token = os.getenv("PAK_TOKEN", "")
        
        # Browser Settings
        self.browser_timeout = int(os.getenv("BROWSER_TIMEOUT", "30"))
        self.verification_timeout = int(os.getenv("VERIFICATION_TIMEOUT", "300"))
        self.screenshot_dir = Path(os.getenv("SCREENSHOT_DIR", "./screenshots"))
        
        # Claude Computer Use Settings
        self.claude_api_key = os.getenv("CLAUDE_API_KEY", "")
        
        # Test Settings
        self.test_retry_count = int(os.getenv("TEST_RETRY_COUNT", "3"))
        self.test_timeout = int(os.getenv("TEST_TIMEOUT", "300"))
        
        # Ensure screenshot directory exists
        self.screenshot_dir.mkdir(exist_ok=True)
    
    def get_pine_ridge_url(self, channel_id: str = None, browser_name: str = None) -> str:
        """Generate Pine Ridge URL with parameters"""
        channel = channel_id or self.default_channel_id
        uid = browser_name or "TestUser"
        
        # Build URL with required parameters
        url = f"{self.pine_ridge_base_url}?"
        params = [
            f"PAK={self.pak_token}",
            f"UID={uid}",
            f"CID={channel}",
            "ALLOWPUBLISHAUDIO=1",
            "ALLOWPUBLISHVIDEO=1",
            "ALLOWPUBLISHSCREENSHARE=1",
            "ALLOWBOTCHAT=1",
            "ALLOWVOICEDATACOLLECTION=1"
        ]
        
        return url + "&".join(params)
    
    def validate(self) -> bool:
        """Validate that required configuration is present"""
        required_fields = [
            ("PAK_TOKEN", self.pak_token),
            ("CLAUDE_API_KEY", self.claude_api_key),
        ]
        
        missing_fields = [field for field, value in required_fields if not value]
        
        if missing_fields:
            raise ValueError(f"Missing required configuration: {', '.join(missing_fields)}")
        
        return True