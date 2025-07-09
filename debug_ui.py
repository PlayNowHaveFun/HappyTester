#!/usr/bin/env python3
"""
Debug script to analyze Pine Ridge UI structure
"""

import asyncio
import os
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.mcp.puppeteer_mcp_client import PuppeteerMCPClient
from src.config.system_config import SystemConfig
from dotenv import load_dotenv

async def debug_pine_ridge_ui():
    """Debug Pine Ridge UI to understand structure"""
    load_dotenv()
    
    # Setup config
    config = SystemConfig.load_from_env()
    
    # Initialize MCP client
    mcp_client = PuppeteerMCPClient(config, headless=False)
    await mcp_client.initialize_webrtc_testing()
    
    try:
        # Launch Chrome
        print("🚀 Launching Chrome for UI debugging...")
        result = await mcp_client.launch_chrome_publisher({
            "url": f"{config.pine_ridge_base_url}?PAK={config.pak_token}&CID={config.default_channel_id}&ALLOWPUBLISHAUDIO=1"
        })
        
        if result.get("success"):
            print("✅ Chrome launched successfully")
            
            # Get the page
            page = mcp_client.browsers['chrome']['page']
            
            # Wait for page to load
            await asyncio.sleep(10)
            
            # Debug the page
            await mcp_client.debug_page_elements(page)
            
            # Keep browser open for manual inspection
            print("🔍 Browser window is open for manual inspection...")
            print("Press Enter to close...")
            input()
            
        else:
            print(f"❌ Failed to launch Chrome: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        # Cleanup
        await mcp_client.cleanup()

if __name__ == "__main__":
    asyncio.run(debug_pine_ridge_ui())