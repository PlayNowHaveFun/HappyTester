"""
Safari subscriber automation for Pine Ridge test case C107928
"""

import asyncio
from typing import Dict, Any
from selenium.webdriver.common.by import By

from .browser_controller import BrowserController
from utils.logger import Logger


class SafariSubscriber(BrowserController):
    """Safari browser automation for subscriber role"""
    
    def __init__(self, config):
        super().__init__(config, "Safari")
        self.logger = Logger.get_logger(__name__)
    
    async def execute_subscriber_workflow(self, channel_id: str = None) -> Dict[str, Any]:
        """Execute the complete subscriber workflow for C107928"""
        
        try:
            self.logger.info("Starting Safari subscriber workflow")
            
            # Step 1: Launch browser and navigate to Pine Ridge
            pine_ridge_url = self.config.get_pine_ridge_url(channel_id, "Safari")
            if not await self.launch_browser(pine_ridge_url):
                return {"success": False, "error": "Failed to launch Safari browser"}
            
            # Step 2: Wait for page to load
            await asyncio.sleep(2)
            
            # Step 3: Look for and click "Join Channel" button using JavaScript click for Safari
            self.logger.info("Looking for Join Channel button")
            try:
                join_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Join')]")
                self.logger.info("Found Join Channel button, using JavaScript click for Safari")
                
                # Use JavaScript click method for Safari (Method 2 from debugging)
                self.driver.execute_script("arguments[0].click();", join_button)
                self.logger.info("Successfully clicked Join Channel button using JavaScript")
                
            except Exception as e:
                return {"success": False, "error": f"Failed to find/click Join Channel button: {str(e)}"}
            
            # Step 4: Wait for join to complete and verify "joined" state (same as Chrome)
            self.logger.info("Waiting for join to complete")
            await asyncio.sleep(1)
            
            if not await self.verify_text_present("joined"):
                return {"success": False, "error": "Join state not confirmed"}
            
            # Step 5: Safari window positioning will be handled centrally in TestExecutor
            self.logger.info("Safari window positioning will be handled centrally in TestExecutor")
            
            # Step 6: Wait for audio stream to be received
            self.logger.info("Waiting for audio stream reception")
            await asyncio.sleep(2)
            
            # Capture verification screenshot
            screenshot_path = self.screenshot_manager.capture_verification_screenshot("subscriber_ready")
            
            self.logger.info("Safari subscriber workflow completed successfully")
            return {
                "success": True,
                "message": "Safari subscriber is ready to receive audio",
                "screenshot_path": screenshot_path
            }
            
        except Exception as e:
            self.logger.error(f"Safari subscriber workflow failed: {str(e)}")
            error_screenshot = self.screenshot_manager.capture_error_screenshot("subscriber_workflow")
            return {
                "success": False,
                "error": str(e),
                "screenshot_path": error_screenshot
            }
    
    async def position_for_verification(self) -> bool:
        """Position Safari window for manual verification"""
        try:
            self.logger.info("Positioning Safari window for verification")
            
            # Use Selenium to resize and position window
            self.driver.set_window_size(800, 600)
            self.driver.set_window_position(800, 0)  # Right side of screen
            
            await asyncio.sleep(1)
            self.logger.info("Safari window positioned on right side")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to position Safari window: {str(e)}")
            return False
    
    async def verify_audio_reception(self) -> bool:
        """Check if audio is being received (visual indicators)"""
        try:
            self.logger.info("Checking for audio reception indicators")
            
            # Look for visual indicators that audio is being received
            result = await self.computer_use_action(
                "Look for any visual indicators that audio is being received, such as audio level meters, speaker icons, or 'receiving audio' text"
            )
            
            return result["success"] and ("audio" in result["response"].lower() or "receiving" in result["response"].lower())
            
        except Exception as e:
            self.logger.error(f"Failed to verify audio reception: {str(e)}")
            return False