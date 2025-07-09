# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Pine Ridge test automation framework that automates WebRTC audio/video testing using Claude's agentic capabilities with Puppeteer through the Model Context Protocol (MCP). The redesigned system provides intelligent, adaptive automation with dynamic planning and error recovery.

**Target Test Case:** C107928 - Publish Local Stream  
**Browser Setup:** Chrome (publisher) + Safari (subscriber)  
**Platform:** macOS only (MVP scope)  
**Verification:** Automated setup + Manual audio verification  
**Architecture:** Claude Agent + MCP + Puppeteer Integration  

## Project Structure

Redesigned architecture with Claude-Puppeteer MCP integration:

### Core Implementation
- `main.py` - Main entry point with argument parsing and orchestration
- `src/core/claude_agent_controller.py` - Claude agent with agentic capabilities
- `src/mcp/puppeteer_mcp_client.py` - MCP-Puppeteer integration layer
- `src/config/system_config.py` - Configuration management
- `src/testrail/testrail_mcp_integration.py` - TestRail integration

### Supporting Components
- `src/core/` - Core intelligence and planning components
- `src/mcp/` - Model Context Protocol integration
- `src/execution/` - Action execution and retry logic
- `src/observation/` - Feedback processing and analysis
- `src/orchestration/` - Multi-browser coordination
- `src/webrtc/` - WebRTC monitoring and metrics
- `src/testrail/` - TestRail API integration

### Specifications
- `Spec/Project-spec.md` - Complete technical architecture and requirements
- `Spec/mvp-requirements.md` - MVP scope and acceptance criteria
- `setup_guide.md` - Setup and execution instructions

## Development Commands

### Setup and Installation
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp .env.example .env
# Edit .env with your actual values
```

### Running Tests
```bash
# Run the main test case C107928
python main.py

# Run with specific options
python main.py --channel-id QAtest --verbose

# Run in headless mode
python main.py --headless --timeout 300

# Run with custom test case
python main.py --test-case C107928 --verbose
```

### Development Tools
- Python 3.9+ for automation framework
- VSCode as the development environment
- Pyppeteer for browser automation
- Anthropic SDK for Claude integration
- AsyncIO for asynchronous execution
- MCP (Model Context Protocol) for tool integration

## Architecture Overview

### Core Components (Implemented)

1. **Claude Agent Controller (`src/core/claude_agent_controller.py`)**
   - Agentic intelligence with dynamic planning
   - Adaptive execution with error recovery
   - Context-aware decision making for WebRTC testing
   - Integration with Anthropic Claude API

2. **MCP Puppeteer Client (`src/mcp/puppeteer_mcp_client.py`)**
   - Model Context Protocol integration
   - Direct Puppeteer browser control
   - WebRTC-specific browser configurations
   - Multi-browser coordination (Chrome + Safari)

3. **System Configuration (`src/config/system_config.py`)**
   - Environment variable management
   - Configuration validation and defaults
   - Runtime parameter override support

4. **TestRail Integration (`src/testrail/testrail_mcp_integration.py`)**
   - Automated result reporting
   - Test execution logging
   - Screenshot attachment support
   - Execution metrics tracking

5. **Multi-Browser Orchestration**
   - Chrome publisher setup with WebRTC optimization
   - Safari subscriber coordination
   - Timing synchronization and state management
   - Manual verification interface

### Pine Ridge Application Integration

- **Base URL:** https://pineridge-static.eng.airtime.com/
- **Authentication:** PAK token in URL parameters
- **Key Parameters:** PAK, UID, CID, ALLOWPUBLISHAUDIO=1, ALLOWPUBLISHVIDEO=1
- **Test Channel:** QAtest (default)

### TestRail API Integration

- **Endpoints:**
  - `GET /get_cases/{suite_id}` - Retrieve test cases
  - `POST /add_result/{run_id}` - Update test results
  - `GET /get_runs/{project_id}` - Get test runs
- **Authentication:** API key-based with rate limiting
- **Target Test Case:** C107928

## Environment Configuration

Required environment variables:
```
TESTRAIL_URL=your-testrail-instance
TESTRAIL_USERNAME=your-username
TESTRAIL_API_KEY=your-api-key
PINE_RIDGE_BASE_URL=https://pineridge-static.eng.airtime.com/
DEFAULT_CHANNEL_ID=QAtest
BROWSER_TIMEOUT=30
VERIFICATION_TIMEOUT=300
```

## Development Workflow

### MVP Implementation Phases

1. **Core Automation (Week 1-2)**
   - VSCode project setup
   - Chrome browser automation
   - Pine Ridge interaction logic
   - Basic UI verification

2. **Multi-Browser Support (Week 2-3)**
   - Safari browser automation
   - Browser coordination
   - Manual verification interface
   - Publisher/subscriber workflow

3. **TestRail Integration (Week 3-4)**
   - TestRail API client
   - Result updating
   - Screenshot capture
   - Execution reporting

4. **Testing & Polish (Week 4)**
   - End-to-end testing
   - Error handling
   - Documentation

## Browser Automation Patterns

### Chrome Publisher Setup
1. Navigate to Pine Ridge URL with PAK token
2. Identify "Join Channel" button using visual recognition
3. Click and wait for UI state change to "joined"
4. Locate "Publish Audio" button
5. Click and verify channel panel appears with Stop button

### Safari Subscriber Setup
1. Launch Safari in parallel/sequentially
2. Navigate to same Pine Ridge URL
3. Join same channel (QAtest)
4. Set up to receive audio stream
5. Position window for manual verification

## Performance Requirements

- Browser launch: < 10 seconds
- Page navigation: < 15 seconds
- Join channel: < 30 seconds
- Total automated steps: < 3 minutes
- Overall test execution: < 5 minutes
- Success rate target: 80%+ (MVP), 90%+ (production)

## Security Considerations

- Store TestRail credentials in environment variables
- Use isolated browser profiles for testing
- Clear browser data between test runs
- Handle camera/microphone permissions securely
- Sanitize logs to remove sensitive tokens

## Error Handling Strategy

- Implement retry logic for failed UI interactions
- Create graceful degradation when automation fails
- Provide clear error messages for troubleshooting
- Allow manual intervention when needed
- Use dynamic waiting based on UI state rather than fixed delays

## Manual Verification Interface

- Position Chrome and Safari side-by-side
- Capture screenshots of publisher and subscriber states
- Present clear verification prompt: "Please verify audio is heard from Chrome to Safari"
- Handle Pass/Fail input with optional comments
- No timeout pressure on user verification

## Important Implementation Notes

- Use descriptive language for UI elements ("blue Join Channel button")
- Implement fallback strategies if elements move or change
- Handle WebRTC connection establishment delays
- Coordinate timing between publisher and subscriber actions
- Use combination of text content, colors, and positioning for element identification

## Future Enhancements

- Firefox browser support
- Windows platform support
- Automated audio/video quality verification
- Mobile browser testing (iOS Safari, Android Chrome)
- Advanced test case parsing and execution