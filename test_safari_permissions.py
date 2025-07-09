#!/usr/bin/env python3
"""
Test script to verify Safari permissions handling
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

async def test_safari_permissions():
    """Test Safari permissions handling"""
    load_dotenv()
    
    # Setup config
    config = SystemConfig.load_from_env()
    
    # Initialize MCP client
    mcp_client = PuppeteerMCPClient(config, headless=False)
    await mcp_client.initialize_webrtc_testing()
    
    try:
        # Launch Safari only
        print("🦁 Testing Safari permissions...")
        result = await mcp_client.launch_safari_subscriber({
            "url": f"{config.pine_ridge_base_url}?PAK={config.pak_token}&CID={config.default_channel_id}&UID=test_subscriber&ALLOWPUBLISHAUDIO=1&ALLOWPUBLISHVIDEO=1"
        })
        
        if result.get("success"):
            print("✅ Safari launched successfully")
            
            # Get the page
            page = mcp_client.browsers['safari']['page']
            
            # Wait for page to load
            await asyncio.sleep(10)
            
            # Check if any permission dialogs appeared
            print("🔍 Checking for permission dialogs...")
            
            # Try to access getUserMedia to trigger permissions
            try:
                await page.evaluate("""
                    async () => {
                        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                            console.log('Testing getUserMedia access...');
                            try {
                                const stream = await navigator.mediaDevices.getUserMedia({
                                    audio: true,
                                    video: false
                                });
                                console.log('getUserMedia success:', stream);
                                return 'success';
                            } catch (e) {
                                console.log('getUserMedia error:', e);
                                return 'error: ' + e.message;
                            }
                        } else {
                            console.log('getUserMedia not available');
                            return 'unavailable';
                        }
                    }
                """)
                print("✅ getUserMedia test completed")
            except Exception as e:
                print(f"⚠️  getUserMedia test failed: {e}")
            
            # Keep browser open for inspection
            print("🔍 Safari window is open for manual inspection...")
            print("Press Enter to close...")
            input()
            
        else:
            print(f"❌ Failed to launch Safari: {result.get('error')}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Cleanup
        await mcp_client.cleanup()

if __name__ == "__main__":
    asyncio.run(test_safari_permissions())