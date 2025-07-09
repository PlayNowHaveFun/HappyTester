#!/usr/bin/env python3
"""
Test Chrome positioning only - to verify full height layout
"""

import sys
import asyncio
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from automation.chrome_publisher import ChromePublisher
from utils.config import Config
from utils.logger import Logger

async def test_chrome_positioning():
    """Test Chrome positioning to verify full height layout"""
    
    logger = Logger.get_logger(__name__)
    logger.info("Testing Chrome positioning")
    
    try:
        # Load configuration
        config = Config()
        
        # Initialize Chrome publisher
        chrome_publisher = ChromePublisher(config)
        
        # Execute Chrome workflow
        result = await chrome_publisher.execute_publisher_workflow()
        
        if result["success"]:
            # Test positioning
            logger.info("Positioning Chrome for testing")
            
            # Get screen dimensions
            import tkinter as tk
            root = tk.Tk()
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()
            root.destroy()
            
            # Calculate half-screen dimensions with full height
            half_width = screen_width // 2
            full_height = screen_height
            
            # Chrome: Left half of screen, full height
            chrome_publisher.driver.set_window_size(half_width, full_height)
            chrome_publisher.driver.set_window_position(0, 0)
            logger.info(f"Chrome positioned: {half_width}x{full_height} at (0,0)")
            
            # Wait for user to verify positioning
            input("Press Enter to continue after verifying Chrome is positioned on left half with full height...")
            
            # Cleanup
            chrome_publisher.close_browser()
            logger.info("Chrome positioning test completed")
        else:
            logger.error(f"Chrome workflow failed: {result}")
        
    except Exception as e:
        logger.error(f"Test failed: {str(e)}")
        return 1

if __name__ == "__main__":
    asyncio.run(test_chrome_positioning())