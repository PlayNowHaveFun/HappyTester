"""
Screenshot utility for Pine Ridge test automation
"""

import os
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from PIL import Image, ImageGrab


class ScreenshotManager:
    """Handle screenshot capture and management"""
    
    def __init__(self, screenshot_dir: Path):
        self.screenshot_dir = screenshot_dir
        self.screenshot_dir.mkdir(exist_ok=True)
    
    def capture_screen(self, filename: str = None) -> Path:
        """Capture full screen screenshot"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
            filename = f"screen_{timestamp}.png"
        
        screenshot_path = self.screenshot_dir / filename
        
        # Capture screenshot using PIL
        screenshot = ImageGrab.grab()
        screenshot.save(screenshot_path)
        
        return screenshot_path
    
    def capture_verification_screenshot(self, test_step: str) -> Path:
        """Capture screenshot for verification purposes"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"verification_{test_step}_{timestamp}.png"
        
        return self.capture_screen(filename)
    
    def capture_error_screenshot(self, error_context: str) -> Path:
        """Capture screenshot when error occurs"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"error_{error_context}_{timestamp}.png"
        
        return self.capture_screen(filename)
    
    def get_latest_screenshot(self) -> Optional[Path]:
        """Get the path of the most recent screenshot"""
        screenshots = list(self.screenshot_dir.glob("*.png"))
        
        if not screenshots:
            return None
        
        return max(screenshots, key=lambda p: p.stat().st_mtime)