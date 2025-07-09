"""
Test execution coordinator for Pine Ridge test case C107928
"""

import asyncio
import time
from typing import Dict, Any
from datetime import datetime

from .chrome_publisher import ChromePublisher
from .safari_subscriber import SafariSubscriber
from utils.logger import Logger
from utils.verification import ManualVerificationInterface, VerificationResult


class TestResult:
    """Container for test execution results"""
    
    def __init__(self, passed: bool, execution_time: float, comment: str = "", error: str = ""):
        self.passed = passed
        self.execution_time = execution_time
        self.comment = comment
        self.error = error
        self.timestamp = datetime.now()


class TestExecutor:
    """Main test executor for C107928 test case"""
    
    def __init__(self, config):
        self.config = config
        self.logger = Logger.get_logger(__name__)
        self.verification_interface = ManualVerificationInterface()
        
        # Initialize browser controllers
        self.chrome_publisher = ChromePublisher(config)
        self.safari_subscriber = SafariSubscriber(config)
    
    async def execute_c107928(self, channel_id: str = None) -> TestResult:
        """Execute the complete C107928 test case"""
        
        start_time = time.time()
        
        try:
            self.logger.info("Starting execution of test case C107928")
            
            # Step 1: Setup Chrome publisher
            self.logger.info("Setting up Chrome publisher")
            publisher_result = await self.chrome_publisher.execute_publisher_workflow(channel_id)
            
            if not publisher_result["success"]:
                error_msg = f"Chrome publisher setup failed: {publisher_result.get('error', 'Unknown error')}"
                self.logger.error(error_msg)
                return TestResult(False, time.time() - start_time, error=error_msg)
            
            # Step 2: Setup Safari subscriber
            self.logger.info("Setting up Safari subscriber")
            subscriber_result = await self.safari_subscriber.execute_subscriber_workflow(channel_id)
            
            if not subscriber_result["success"]:
                error_msg = f"Safari subscriber setup failed: {subscriber_result.get('error', 'Unknown error')}"
                self.logger.error(error_msg)
                return TestResult(False, time.time() - start_time, error=error_msg)
            
            # Step 3: Position windows for verification
            await self.position_windows_for_verification()
            
            # Step 4: Manual verification
            self.logger.info("Starting manual verification")
            verification_result = self.verification_interface.get_verification_result(
                test_step="C107928 - Audio Stream Verification",
                instructions="Please verify that audio is being transmitted from Chrome (publisher) to Safari (subscriber). You should hear audio in the Safari window that originates from the Chrome window.",
                chrome_screenshot=str(publisher_result.get("screenshot_path", "")),
                safari_screenshot=str(subscriber_result.get("screenshot_path", ""))
            )
            
            # Step 5: Cleanup
            await self.cleanup_browsers()
            
            # Calculate execution time
            execution_time = time.time() - start_time
            
            # Create final result
            result = TestResult(
                passed=verification_result.passed,
                execution_time=execution_time,
                comment=verification_result.comment
            )
            
            self.logger.info(f"Test case C107928 completed: {'PASS' if result.passed else 'FAIL'}")
            return result
            
        except Exception as e:
            self.logger.error(f"Test execution failed with exception: {str(e)}")
            await self.cleanup_browsers()
            
            return TestResult(
                passed=False,
                execution_time=time.time() - start_time,
                error=str(e)
            )
    
    async def position_windows_for_verification(self) -> None:
        """Position browser windows for optimal manual verification"""
        
        try:
            self.logger.info("Positioning browser windows for verification")
            
            # Position Chrome on the left side using Selenium
            try:
                # Get screen dimensions for proper half-screen sizing
                import tkinter as tk
                root = tk.Tk()
                screen_width = root.winfo_screenwidth()
                screen_height = root.winfo_screenheight()
                root.destroy()
                
                # Calculate half-screen dimensions with full height
                half_width = screen_width // 2
                full_height = screen_height  # Use full screen height
                
                # Chrome: Left half of screen, full height
                self.chrome_publisher.driver.set_window_size(half_width, full_height)
                self.chrome_publisher.driver.set_window_position(0, 0)  # Left side, top of screen
                self.logger.info(f"Chrome positioned: {half_width}x{full_height} at (0,0)")
                
                # Safari: Right half of screen, full height
                self.safari_subscriber.driver.set_window_size(half_width, full_height)
                self.safari_subscriber.driver.set_window_position(half_width, 0)  # Right side, top of screen
                self.logger.info(f"Safari positioned: {half_width}x{full_height} at ({half_width},0)")
                
            except Exception as e:
                self.logger.error(f"Failed to position windows: {str(e)}")
            
            # Small delay to ensure positioning completes
            await asyncio.sleep(1)
            
            self.logger.info("Browser windows positioned for verification")
            
        except Exception as e:
            self.logger.warning(f"Failed to position windows optimally: {str(e)}")
    
    async def cleanup_browsers(self) -> None:
        """Clean up browser instances"""
        
        try:
            self.logger.info("Cleaning up browser instances")
            
            # Stop publishing if still active
            if self.chrome_publisher.is_running:
                await self.chrome_publisher.stop_publishing()
            
            # Close browsers
            self.chrome_publisher.close_browser()
            self.safari_subscriber.close_browser()
            
            self.logger.info("Browser cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")
    
    async def retry_test_execution(self, max_retries: int = 3) -> TestResult:
        """Execute test with retry logic"""
        
        for attempt in range(max_retries):
            self.logger.info(f"Test execution attempt {attempt + 1}/{max_retries}")
            
            result = await self.execute_c107928()
            
            if result.passed:
                return result
            
            if attempt < max_retries - 1:
                # Ask user if they want to retry
                retry_prompt = f"Attempt {attempt + 1} failed: {result.error or result.comment}"
                if not self.verification_interface.prompt_for_retry(retry_prompt):
                    break
                
                # Wait before retry
                await asyncio.sleep(5)
        
        return result