#!/usr/bin/env python3
"""
Test script to focus on just the publish functionality
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

async def test_publish_only():
    """Test just the publish functionality"""
    load_dotenv()
    
    # Setup config
    config = SystemConfig.load_from_env()
    
    # Initialize MCP client
    mcp_client = PuppeteerMCPClient(config, headless=False)
    await mcp_client.initialize_webrtc_testing()
    
    try:
        # Launch Chrome
        print("🚀 Launching Chrome for publish test...")
        result = await mcp_client.launch_chrome_publisher({
            "url": f"{config.pine_ridge_base_url}?PAK={config.pak_token}&CID={config.default_channel_id}&UID=test_user&ALLOWPUBLISHAUDIO=1&ALLOWPUBLISHVIDEO=1"
        })
        
        if result.get("success"):
            print("✅ Chrome launched successfully")
            
            # Get the page
            page = mcp_client.browsers['chrome']['page']
            
            # Wait for page to load
            await asyncio.sleep(10)
            
            # Join the channel first
            print("🏠 Joining channel...")
            join_result = await mcp_client.join_pine_ridge_channel({
                "browser": "chrome",
                "channel_id": config.default_channel_id
            })
            
            if join_result.get("success"):
                print("✅ Successfully joined channel")
                
                # Wait a bit for UI to update
                await asyncio.sleep(5)
                
                # Now try to publish audio
                print("🎤 Testing publish audio...")
                publish_result = await mcp_client.publish_audio_stream({
                    "browser": "chrome"
                })
                
                if publish_result.get("success"):
                    print("✅ Audio publishing successful!")
                    print(f"Result: {publish_result}")
                else:
                    print("❌ Audio publishing failed")
                    print(f"Error: {publish_result.get('error')}")
                    
            else:
                print(f"❌ Failed to join channel: {join_result.get('error')}")
            
            # Keep browser open for inspection
            print("🔍 Browser window is open for manual inspection...")
            print("Press Enter to close...")
            input()
            
        else:
            print(f"❌ Failed to launch Chrome: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Cleanup
        await mcp_client.cleanup()

if __name__ == "__main__":
    asyncio.run(test_publish_only())