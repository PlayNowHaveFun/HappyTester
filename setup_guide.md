# Pine Ridge WebRTC Testing System - Setup Guide

## Quick Start

### 1. Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your actual values
# Required fields:
# - TESTRAIL_URL, TESTRAIL_USERNAME, TESTRAIL_API_KEY
# - PAK_TOKEN (already provided)
# - CLAUDE_API_KEY (already provided)
```

### 3. Run the System
```bash
# Run the main test case C107928
python main.py

# Or run with specific configuration
python main.py --channel-id QAtest --verbose
```

## System Architecture

The redesigned system leverages Claude's agentic capabilities through:

1. **MCP Integration**: Direct Puppeteer control via Model Context Protocol
2. **Multi-Browser Orchestration**: Intelligent Chrome + Safari coordination
3. **WebRTC Monitoring**: Real-time connection state tracking
4. **Adaptive Execution**: Dynamic plan generation and error recovery
5. **TestRail Integration**: Automated result reporting

## Key Features

### Agentic Capabilities
- **Dynamic Planning**: Claude generates execution plans based on WebRTC state
- **Adaptive Recovery**: Intelligent retry mechanisms with learning
- **Visual Intelligence**: Screenshot analysis and UI element recognition
- **Context Awareness**: WebRTC-specific decision making

### WebRTC Optimizations
- **Connection Monitoring**: Real-time peer connection state tracking
- **Audio Stream Detection**: Automatic audio flow verification
- **Browser Synchronization**: Coordinated publisher/subscriber setup
- **Quality Assessment**: Connection quality metrics and reporting

### Enhanced Reliability
- **Multi-Strategy Element Detection**: Fallback element finding approaches
- **Graceful Degradation**: Automatic fallback to manual verification
- **Comprehensive Error Handling**: Detailed error reporting and recovery
- **Screenshot Evidence**: Visual proof of test execution states

## Running Different Modes

### Development Mode
```bash
# Run with verbose logging
ENABLE_VERBOSE_LOGGING=true python main.py

# Run with custom timeout
WEBRTC_CONNECTION_TIMEOUT=60 python main.py
```

### Production Mode
```bash
# Run with minimal logging
ENABLE_VERBOSE_LOGGING=false python main.py

# Run with retry configuration
MAX_RETRIES=5 python main.py
```

### Debug Mode
```bash
# Run with MCP debugging
MCP_LOG_LEVEL=DEBUG python main.py

# Run with screenshot capture
SCREENSHOT_QUALITY=100 python main.py
```

## System Components

### Core Files
- `main.py` - Main entry point
- `src/core/claude_agent_controller.py` - Claude agent intelligence
- `src/mcp/puppeteer_mcp_client.py` - MCP-Puppeteer integration
- `src/orchestration/multi_browser_orchestrator.py` - Multi-browser coordination

### Configuration Files
- `.env` - Environment variables
- `requirements.txt` - Python dependencies
- `src/config/system_config.py` - System configuration management

### Supporting Modules
- `src/webrtc/` - WebRTC monitoring and analysis
- `src/execution/` - Action execution and retry logic
- `src/observation/` - Feedback processing and visual analysis
- `src/testrail/` - TestRail integration and reporting

## Expected Execution Flow

1. **Initialization**: Load configuration and start MCP server
2. **Chrome Publisher Setup**: Launch Chrome, join channel, publish audio
3. **Safari Subscriber Setup**: Launch Safari, join same channel
4. **WebRTC Connection**: Monitor connection establishment
5. **Manual Verification**: Present verification UI to user
6. **Result Reporting**: Update TestRail with test results
7. **Cleanup**: Close browsers and cleanup resources

## Performance Expectations

- **Setup Time**: < 30 seconds for browser initialization
- **Execution Time**: < 3 minutes for automated steps
- **Success Rate**: 90%+ for automated components
- **Manual Verification**: User-controlled timing

## Troubleshooting

### Common Issues
1. **Browser Launch Failures**: Check executable paths in .env
2. **MCP Connection Issues**: Verify MCP server port availability
3. **WebRTC Connection Failures**: Check network/firewall settings
4. **TestRail API Errors**: Verify credentials and API access

### Debug Steps
1. Enable verbose logging: `ENABLE_VERBOSE_LOGGING=true`
2. Check MCP server status: `MCP_LOG_LEVEL=DEBUG`
3. Verify browser automation: Check screenshot directory
4. Monitor WebRTC state: Review connection metrics in logs

## Next Steps

After running the system successfully:

1. **Customize Configuration**: Adjust timeouts and retry settings
2. **Extend Test Cases**: Add more WebRTC test scenarios
3. **Enhance Verification**: Add automated audio quality checks
4. **Scale Testing**: Implement parallel test execution
5. **Monitor Performance**: Track success rates and execution times

The system is designed to be extensible and maintainable, with clear separation of concerns and modular architecture for future enhancements.