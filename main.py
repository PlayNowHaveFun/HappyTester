#!/usr/bin/env python3
"""
Pine Ridge WebRTC Testing System - Main Entry Point
Claude-Puppeteer Integration with Agentic Capabilities
"""

import asyncio
import os
import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.claude_agent_controller import ClaudeAgentController
from src.mcp.puppeteer_mcp_client import PuppeteerMCPClient
from src.testrail.testrail_mcp_integration import TestRailMCPIntegration
from src.config.system_config import SystemConfig

def setup_environment():
    """Setup environment and load configuration"""
    load_dotenv()
    
    # Create necessary directories
    os.makedirs("screenshots", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    return SystemConfig.load_from_env()

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Pine Ridge WebRTC Testing System")
    parser.add_argument("--test-case", default="C107928", help="Test case ID to execute")
    parser.add_argument("--channel-id", help="Channel ID override")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("--headless", action="store_true", help="Run browsers in headless mode")
    parser.add_argument("--timeout", type=int, default=300, help="Test timeout in seconds")
    
    return parser.parse_args()

async def main():
    """
    Main entry point for Claude-Puppeteer WebRTC testing system
    """
    args = parse_arguments()
    
    try:
        # Setup environment
        config = setup_environment()
        
        # Override config with command line arguments
        if args.channel_id:
            config.default_channel_id = args.channel_id
        if args.verbose:
            config.enable_verbose_logging = True
        
        print("🚀 Pine Ridge WebRTC Testing System")
        print("=" * 50)
        print(f"Test Case: {args.test_case}")
        print(f"Channel ID: {config.default_channel_id}")
        print(f"Verbose Mode: {config.enable_verbose_logging}")
        print(f"Headless Mode: {args.headless}")
        print("=" * 50)
        
        # Initialize MCP client (always non-headless for human verification)
        print("📡 Initializing Puppeteer MCP Client...")
        mcp_client = PuppeteerMCPClient(config, headless=False)  # Always non-headless for human verification
        await mcp_client.initialize_webrtc_testing()
        
        # Initialize Claude Agent Controller
        print("🧠 Initializing Claude Agent Controller...")
        claude_agent = ClaudeAgentController(mcp_client, config)
        
        # Initialize TestRail integration
        print("📊 Initializing TestRail Integration...")
        testrail_integration = TestRailMCPIntegration(config)
        
        # Execute test case
        print(f"🎯 Starting test execution for {args.test_case}")
        print("-" * 50)
        
        result = await claude_agent.execute_test_case(args.test_case)
        
        # Report results to TestRail
        print("📋 Updating TestRail with results...")
        testrail_result = await testrail_integration.execute_test_case_with_reporting(
            args.test_case, result
        )
        
        # Display results
        print("=" * 50)
        print("✅ Test execution completed successfully!")
        print(f"📊 Result: {result.overall_status}")
        print(f"⏱️  Execution Time: {result.total_execution_time:.2f} seconds")
        print(f"🔄 Retry Count: {result.retry_count}")
        print(f"📋 TestRail Status: {testrail_result.status}")
        
        if result.screenshots:
            print(f"📸 Screenshots saved: {len(result.screenshots)} files")
        
        if result.overall_status == "PASSED":
            print("🎉 Test PASSED!")
            return 0
        else:
            print("❌ Test FAILED!")
            print(f"Error: {result.error_message}")
            return 1
            
    except KeyboardInterrupt:
        print("\\n⚠️  Test execution interrupted by user")
        return 130
        
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1
    
    finally:
        # Cleanup
        try:
            if 'mcp_client' in locals():
                await mcp_client.cleanup()
            print("🧹 Cleanup completed")
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)