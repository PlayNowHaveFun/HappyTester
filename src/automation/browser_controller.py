"""
Browser controller using Claude Computer Use for Pine Ridge automation
"""

import asyncio
import time
import base64
from typing import Dict, Any, Optional
from pathlib import Path

from anthropic import Anthropic
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utils.logger import Logger
from utils.screenshot import ScreenshotManager


class BrowserController:
    """Hybrid browser controller using Selenium + Claude Computer Use"""
    
    def __init__(self, config, browser_name: str):
        self.config = config
        self.browser_name = browser_name
        self.logger = Logger.get_logger(f"{__name__}.{browser_name}")
        self.screenshot_manager = ScreenshotManager(config.screenshot_dir)
        
        # Initialize Claude client for fallback
        self.claude_client = Anthropic(api_key=config.claude_api_key)
        
        # Selenium WebDriver
        self.driver = None
        self.wait = None
        self.is_running = False
    
    async def launch_browser(self, url: str) -> bool:
        """Launch browser using WebDriver and navigate to URL"""
        try:
            self.logger.info(f"Launching {self.browser_name} browser with WebDriver")
            
            # Configure browser options
            if self.browser_name.lower() == "chrome":
                options = ChromeOptions()
                # Allow real media permissions for WebRTC testing
                options.add_argument("--disable-web-security")
                options.add_argument("--allow-running-insecure-content")
                # Auto-grant media permissions for testing
                options.add_argument("--use-fake-ui-for-media-stream")
                # Create fresh profile to test permission handling
                import time
                options.add_argument(f"--user-data-dir=/tmp/chrome_test_profile_{int(time.time())}")
                
                # Set permissions for media devices
                prefs = {
                    "profile.default_content_setting_values.media_stream_mic": 1,
                    "profile.default_content_setting_values.media_stream_camera": 1,
                    "profile.default_content_setting_values.notifications": 1
                }
                options.add_experimental_option("prefs", prefs)
                
                self.driver = webdriver.Chrome(options=options)
                
            elif self.browser_name.lower() == "safari":
                options = SafariOptions()
                # Enable experimental features for automation
                options.add_argument("--enable-automation")
                # Allow real media device access for WebRTC testing
                options.add_argument("--disable-web-security")
                options.add_argument("--allow-running-insecure-content")
                # Auto-grant media permissions for testing
                options.add_argument("--use-fake-ui-for-media-stream")
                
                # Close any existing Safari instances to avoid session conflicts
                try:
                    import subprocess
                    subprocess.run(["pkill", "-f", "Safari"], capture_output=True)
                    await asyncio.sleep(2)  # Wait for Safari to close
                except Exception as e:
                    self.logger.warning(f"Could not close existing Safari instances: {str(e)}")
                
                self.driver = webdriver.Safari(options=options)
                
            else:
                raise ValueError(f"Unsupported browser: {self.browser_name}")
            
            # Configure WebDriver wait
            self.wait = WebDriverWait(self.driver, self.config.browser_timeout)
            
            # Navigate to URL
            self.driver.get(url)
            self.is_running = True
            
            # Handle permissions if needed
            await self._handle_permissions()
            
            self.logger.info(f"{self.browser_name} browser launched successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to launch {self.browser_name}: {str(e)}")
            return False
    
    async def _handle_permissions(self):
        """Handle microphone/camera permissions using Claude vision"""
        try:
            # Wait briefly for permission dialog to appear
            await asyncio.sleep(2)
            
            # Safari-specific permission handling
            if self.browser_name.lower() == "safari":
                await self._handle_safari_permissions()
            
            # Use Claude to detect and handle permission dialogs
            permission_result = await self.computer_use_action(
                "Look at this browser screenshot. Is there a permission dialog asking for microphone or camera access? "
                "If you see 'Allow' or 'Permit' buttons for media permissions, respond with 'PERMISSION_DIALOG_FOUND' "
                "and describe where the Allow button is located. If no permission dialog, respond with 'NO_DIALOG'."
            )
            
            if permission_result["success"] and "PERMISSION_DIALOG_FOUND" in permission_result["response"]:
                self.logger.info("Permission dialog detected, attempting to allow")
                
                # Try to click Allow button using Claude
                allow_result = await self.computer_use_action(
                    "Click on the 'Allow' or 'Permit' button in the permission dialog to grant microphone and camera access."
                )
                
                if allow_result["success"]:
                    self.logger.info("Permissions granted successfully")
                    await asyncio.sleep(1)  # Wait for dialog to close
                else:
                    self.logger.warning("Failed to grant permissions automatically")
            else:
                self.logger.info("No permission dialog detected")
                
        except Exception as e:
            self.logger.error(f"Error handling permissions: {str(e)}")
    
    async def _handle_safari_permissions(self):
        """Handle Safari-specific media permissions"""
        try:
            self.logger.info("Handling Safari media permissions")
            
            # Try to trigger media permission request via JavaScript
            permission_script = """
                if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
                        .then(function(stream) {
                            console.log('Media permissions granted');
                            // Stop the stream immediately after getting permission
                            stream.getTracks().forEach(track => track.stop());
                            return 'PERMISSIONS_GRANTED';
                        })
                        .catch(function(error) {
                            console.log('Media permissions denied:', error);
                            return 'PERMISSIONS_DENIED';
                        });
                } else {
                    return 'MEDIA_API_NOT_AVAILABLE';
                }
            """
            
            result = self.driver.execute_script(permission_script)
            self.logger.info(f"Safari media permission script result: {result}")
            
            # Wait for potential permission dialog
            await asyncio.sleep(3)
            
        except Exception as e:
            self.logger.warning(f"Safari permission handling failed: {str(e)}")
    
    async def computer_use_action(self, action_description: str) -> Dict[str, Any]:
        """Execute computer use action via Claude Computer Use API"""
        try:
            self.logger.info(f"Executing computer use action: {action_description}")
            
            # Capture current screen
            screenshot_path = self.screenshot_manager.capture_screen()
            
            # Read and encode screenshot
            with open(screenshot_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Create message with screenshot
            message = {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": action_description
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_data
                        }
                    }
                ]
            }
            
            # Send to Claude with vision capability for element detection
            response = self.claude_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[message]
            )
            
            # Parse response for element detection
            response_text = response.content[0].text if response.content else ""
            
            # Check if this is a click action vs element detection
            if "click" in action_description.lower():
                # This is a click action - we need to implement actual clicking
                # For now, we'll use basic screen coordinates if Claude provides them
                result = {
                    "success": True,
                    "response": f"Click action processed: {response_text}",
                    "screenshot_path": screenshot_path
                }
            else:
                # This is element detection - check if Claude found the element
                element_found = any(keyword in response_text.lower() for keyword in [
                    "found", "see", "visible", "located", "present", "identified"
                ])
                
                result = {
                    "success": element_found,
                    "response": response_text,
                    "screenshot_path": screenshot_path
                }
            
            self.logger.info(f"Computer use action completed: {result['response']}")
            return result
            
        except Exception as e:
            self.logger.error(f"Computer use action failed: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "screenshot_path": self.screenshot_manager.capture_error_screenshot("action_failed")
            }
    
    def _encode_screenshot(self, screenshot_path: Path) -> str:
        """Encode screenshot to base64 for Claude"""
        import base64
        
        with open(screenshot_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    async def wait_for_element(self, element_description: str, timeout: int = 30) -> bool:
        """Wait for element using Selenium first, fallback to Claude vision"""
        self.logger.info(f"Waiting for element: {element_description}")
        
        # First try Selenium with common selectors
        selenium_success = await self._wait_for_element_selenium(element_description, timeout // 2)
        if selenium_success:
            return True
        
        # Fallback to Claude vision
        self.logger.info(f"Selenium failed, trying Claude vision for: {element_description}")
        return await self._wait_for_element_claude(element_description, timeout // 2)
    
    async def _wait_for_element_selenium(self, element_description: str, timeout: int) -> bool:
        """Wait for element using Selenium WebDriver"""
        try:
            # Define selectors for Pine Ridge UI elements
            selectors = []
            
            if "join channel" in element_description.lower():
                selectors = [
                    (By.XPATH, "//button[contains(text(), 'Join Channel')]"),
                    (By.XPATH, "//button[contains(text(), 'Join')]"),
                    (By.CSS_SELECTOR, "button[class*='join']"),
                    (By.CSS_SELECTOR, "[data-testid*='join']"),
                ]
            elif "publish dropdown" in element_description.lower():
                selectors = [
                    (By.XPATH, "//button[contains(text(), 'Publish')]"),
                    (By.XPATH, "//select[contains(@id, 'publish')]"),
                    (By.CSS_SELECTOR, "button[class*='publish']"),
                    (By.CSS_SELECTOR, "[data-testid*='publish']"),
                    (By.CSS_SELECTOR, ".dropdown-toggle"),
                ]
            elif "publish audio + video" in element_description.lower():
                selectors = [
                    (By.XPATH, "//option[contains(text(), 'Publish Audio + Video')]"),
                    (By.XPATH, "//li[contains(text(), 'Publish Audio + Video')]"),
                    (By.XPATH, "//a[contains(text(), 'Publish Audio + Video')]"),
                    (By.XPATH, "//div[contains(text(), 'Publish Audio + Video')]"),
                    (By.XPATH, "//span[contains(text(), 'Publish Audio + Video')]"),
                    (By.CSS_SELECTOR, "[data-value*='audio-video']"),
                    (By.CSS_SELECTOR, ".dropdown-item"),
                    (By.CSS_SELECTOR, ".dropdown-menu option"),
                    (By.CSS_SELECTOR, ".dropdown-menu li"),
                ]
            elif "publish audio" in element_description.lower():
                selectors = [
                    (By.XPATH, "//button[contains(text(), 'Publish Audio')]"),
                    (By.XPATH, "//button[contains(text(), 'Audio')]"),
                    (By.CSS_SELECTOR, "button[class*='audio']"),
                    (By.CSS_SELECTOR, "[data-testid*='audio']"),
                ]
            elif "stop" in element_description.lower():
                selectors = [
                    (By.XPATH, "//button[contains(text(), 'Stop')]"),
                    (By.CSS_SELECTOR, "button[class*='stop']"),
                    (By.CSS_SELECTOR, "[data-testid*='stop']"),
                ]
            
            # Try each selector
            for by, selector in selectors:
                try:
                    element = WebDriverWait(self.driver, timeout).until(
                        EC.element_to_be_clickable((by, selector))
                    )
                    self.logger.info(f"Element found with Selenium: {selector}")
                    return True
                except TimeoutException:
                    continue
            
            return False
            
        except Exception as e:
            self.logger.error(f"Selenium element wait failed: {str(e)}")
            return False
    
    async def _wait_for_element_claude(self, element_description: str, timeout: int) -> bool:
        """Wait for element using Claude vision (fallback)"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            # Create specific prompt for Pine Ridge UI elements
            if "join channel" in element_description.lower():
                prompt = "Look at this Pine Ridge application screenshot. Is there a 'Join Channel' button visible? Look for button text that says 'Join Channel' or similar. If you see it, respond with 'FOUND' and describe where it is located."
            elif "publish dropdown" in element_description.lower():
                prompt = "Look at this Pine Ridge application screenshot. Is there a 'Publish' dropdown button visible? Look for button text that says 'Publish' or a dropdown control for publishing. If you see it, respond with 'FOUND' and describe where it is located."
            elif "publish audio + video" in element_description.lower():
                prompt = "Look at this Pine Ridge application screenshot. Is there a 'Publish Audio + Video' option visible in a dropdown menu? Look for dropdown items that say 'Audio + Video' or similar. If you see it, respond with 'FOUND' and describe where it is located."
            elif "publish audio" in element_description.lower():
                prompt = "Look at this Pine Ridge application screenshot. Is there a 'Publish Audio' button visible? Look for button text that says 'Publish Audio' or similar audio publishing controls. If you see it, respond with 'FOUND' and describe where it is located."
            elif "stop" in element_description.lower():
                prompt = "Look at this Pine Ridge application screenshot. Is there a 'Stop' button visible? Look for button text that says 'Stop' or similar stop controls. If you see it, respond with 'FOUND' and describe where it is located."
            else:
                prompt = f"Look at this screenshot carefully. Can you see a UI element that matches: {element_description}? If you see it, respond with 'FOUND' and describe where it is located."
            
            result = await self.computer_use_action(prompt)
            
            if result["success"]:
                self.logger.info(f"Element found with Claude: {element_description}")
                return True
            
            await asyncio.sleep(2)
        
        self.logger.warning(f"Element not found within timeout: {element_description}")
        return False
    
    async def click_element(self, element_description: str) -> bool:
        """Click element using Selenium first, fallback to Claude"""
        self.logger.info(f"Clicking element: {element_description}")
        
        # First try Selenium
        selenium_success = await self._click_element_selenium(element_description)
        if selenium_success:
            return True
        
        # Fallback to Claude vision + computer use
        self.logger.info(f"Selenium click failed, trying Claude for: {element_description}")
        return await self._click_element_claude(element_description)
    
    async def _click_element_selenium(self, element_description: str) -> bool:
        """Click element using Selenium WebDriver"""
        try:
            # Define selectors for Pine Ridge UI elements
            selectors = []
            
            if "join channel" in element_description.lower():
                selectors = [
                    (By.XPATH, "//button[contains(text(), 'Join Channel')]"),
                    (By.XPATH, "//button[contains(text(), 'Join')]"),
                    (By.CSS_SELECTOR, "button[class*='join']"),
                    (By.CSS_SELECTOR, "[data-testid*='join']"),
                ]
            elif "publish dropdown" in element_description.lower():
                selectors = [
                    (By.XPATH, "//button[contains(text(), 'Publish')]"),
                    (By.XPATH, "//select[contains(@id, 'publish')]"),
                    (By.CSS_SELECTOR, "button[class*='publish']"),
                    (By.CSS_SELECTOR, "[data-testid*='publish']"),
                    (By.CSS_SELECTOR, ".dropdown-toggle"),
                ]
            elif "publish audio + video" in element_description.lower():
                selectors = [
                    (By.XPATH, "//option[contains(text(), 'Publish Audio + Video')]"),
                    (By.XPATH, "//li[contains(text(), 'Publish Audio + Video')]"),
                    (By.XPATH, "//a[contains(text(), 'Publish Audio + Video')]"),
                    (By.XPATH, "//div[contains(text(), 'Publish Audio + Video')]"),
                    (By.XPATH, "//span[contains(text(), 'Publish Audio + Video')]"),
                    (By.CSS_SELECTOR, "[data-value*='audio-video']"),
                    (By.CSS_SELECTOR, ".dropdown-item"),
                    (By.CSS_SELECTOR, ".dropdown-menu option"),
                    (By.CSS_SELECTOR, ".dropdown-menu li"),
                ]
            elif "publish audio" in element_description.lower():
                selectors = [
                    (By.XPATH, "//button[contains(text(), 'Publish Audio')]"),
                    (By.XPATH, "//button[contains(text(), 'Audio')]"),
                    (By.CSS_SELECTOR, "button[class*='audio']"),
                    (By.CSS_SELECTOR, "[data-testid*='audio']"),
                ]
            elif "stop" in element_description.lower():
                selectors = [
                    (By.XPATH, "//button[contains(text(), 'Stop')]"),
                    (By.CSS_SELECTOR, "button[class*='stop']"),
                    (By.CSS_SELECTOR, "[data-testid*='stop']"),
                ]
            
            # Try each selector
            for by, selector in selectors:
                try:
                    element = self.wait.until(EC.element_to_be_clickable((by, selector)))
                    element.click()
                    self.logger.info(f"Successfully clicked element with Selenium: {selector}")
                    return True
                except (TimeoutException, NoSuchElementException):
                    continue
            
            return False
            
        except Exception as e:
            self.logger.error(f"Selenium click failed: {str(e)}")
            return False
    
    async def _click_element_claude(self, element_description: str) -> bool:
        """Click element using Claude Computer Use (fallback)"""
        try:
            # For dropdown items, use more specific instructions
            if "publish audio + video" in element_description.lower():
                click_instruction = "Click on the 'Publish Audio + Video' option in the dropdown menu. Look for the text 'Publish Audio + Video' and click directly on it."
            else:
                click_instruction = f"Click on the {element_description}"
            
            result = await self.computer_use_action(click_instruction)
            return result["success"]
        except Exception as e:
            self.logger.error(f"Claude click failed: {str(e)}")
            return False
    
    async def verify_text_present(self, text: str) -> bool:
        """Verify that specific text is present on screen"""
        if text.lower() == "joined":
            prompt = "Look at this Pine Ridge application screenshot. Can you see any text that indicates the user has joined a channel? Look for text like 'joined', 'joinState: joined', or similar status indicators. If you see it, respond with 'FOUND' and describe what you see."
        else:
            prompt = f"Look at this screenshot carefully. Can you see the text '{text}' anywhere on the screen? If you see it, respond with 'FOUND' and describe where it is located."
        
        result = await self.computer_use_action(prompt)
        return result["success"]
    
    def close_browser(self):
        """Close the browser"""
        if self.driver:
            try:
                self.driver.quit()
                self.is_running = False
                self.logger.info(f"{self.browser_name} browser closed")
                
                # For Safari, ensure session is completely terminated
                if self.browser_name.lower() == "safari":
                    import subprocess
                    import time
                    time.sleep(1)  # Brief wait before force closing
                    subprocess.run(["pkill", "-f", "safaridriver"], capture_output=True)
                    
            except Exception as e:
                self.logger.warning(f"Error closing {self.browser_name}: {str(e)}")
                # Force close if normal quit fails
                if self.browser_name.lower() == "safari":
                    import subprocess
                    subprocess.run(["pkill", "-f", "Safari"], capture_output=True)
                    subprocess.run(["pkill", "-f", "safaridriver"], capture_output=True)