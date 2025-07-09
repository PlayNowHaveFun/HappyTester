# Pine Ridge WebRTC Testing System - Deployment Guide

## Quick Start

### Prerequisites
- **macOS**: Required for Safari WebKit testing
- **Python 3.9+**: Recommended Python version
- **Git**: For cloning the repository

### 1. Clone and Setup
```bash
git clone https://github.com/PlayNowHaveFun/HappyTester.git
cd HappyTester

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium webkit
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your credentials
nano .env
```

### 3. Run Test
```bash
# Run full test suite
python main.py

# Run specific test case
python main.py --test-case C107928 --channel-id MyChannel
```

## Detailed Setup Guide

### System Requirements

#### Hardware Requirements
- **CPU**: Intel/Apple Silicon (M1/M2 recommended)
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 2GB free space for browsers and dependencies
- **Network**: Stable internet connection for WebRTC testing

#### Software Requirements
- **Operating System**: macOS 10.15+ (Catalina or later)
- **Python**: 3.9.0 or higher
- **Git**: Latest version
- **Browser Support**: 
  - Chrome/Chromium (automatically installed by Playwright)
  - Safari (system default)

### Environment Variables Configuration

Create a `.env` file in the project root with the following variables:

```env
# Required Configuration
PINE_RIDGE_BASE_URL=https://pineridge-static.eng.airtime.com/
PAK_TOKEN=your_pak_token_here
CLAUDE_API_KEY=your_claude_api_key_here

# Optional Configuration
DEFAULT_CHANNEL_ID=QAtest
BROWSER_TIMEOUT=30
WEBRTC_CONNECTION_TIMEOUT=30
AUDIO_VERIFICATION_TIMEOUT=300
MAX_RETRIES=3
SCREENSHOT_DIR=./screenshots
LOG_DIR=./logs
ENABLE_VERBOSE_LOGGING=true

# TestRail Integration (Optional)
TESTRAIL_URL=https://your-instance.testrail.io
TESTRAIL_USERNAME=your_username
TESTRAIL_API_KEY=your_api_key

# Advanced Configuration
MCP_SERVER_PORT=8000
MCP_LOG_LEVEL=INFO
SCREENSHOT_QUALITY=80
TEST_RETRY_COUNT=3
TEST_TIMEOUT=300
```

### Obtaining Required Credentials

#### 1. **PAK Token**
- Contact your Pine Ridge administrator
- Request a publishable PAK token for testing
- Ensure token has audio/video publishing permissions

#### 2. **Claude API Key**
- Visit [Anthropic Console](https://console.anthropic.com/)
- Create an account or sign in
- Generate an API key from the API Keys section
- Ensure you have sufficient credits for API usage

#### 3. **TestRail Credentials** (Optional)
- Log in to your TestRail instance
- Go to Account Settings > API Keys
- Generate a new API key
- Note your username and TestRail URL

### Installation Steps

#### 1. **System Dependencies**
```bash
# Install Python 3.9+ (if not already installed)
brew install python@3.9

# Install Git (if not already installed)
brew install git

# Verify installations
python3 --version
git --version
```

#### 2. **Project Setup**
```bash
# Clone repository
git clone https://github.com/PlayNowHaveFun/HappyTester.git
cd HappyTester

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

#### 3. **Browser Installation**
```bash
# Install Playwright browsers
playwright install chromium webkit

# Verify installations
playwright --version
```

#### 4. **Configuration**
```bash
# Copy environment template
cp .env.example .env

# Edit configuration
nano .env  # or use your preferred editor

# Create required directories
mkdir -p screenshots logs
```

#### 5. **Verification**
```bash
# Test configuration
python -c "
from src.config.system_config import SystemConfig
config = SystemConfig.load_from_env()
print('✅ Configuration loaded successfully')
print(f'Pine Ridge URL: {config.pine_ridge_base_url}')
print(f'Default Channel: {config.default_channel_id}')
"

# Test browser automation
python test_safari_permissions.py
```

### Usage Examples

#### Basic Test Execution
```bash
# Run default test case
python main.py

# Run with verbose logging
python main.py --verbose

# Run specific test case
python main.py --test-case C107928

# Run with custom channel
python main.py --channel-id MyTestChannel

# Run with timeout
python main.py --timeout 600
```

#### Advanced Usage
```bash
# Run in headless mode (not recommended for this system)
python main.py --headless

# Run with specific configuration
PINE_RIDGE_BASE_URL="https://custom-url.com" python main.py

# Run component tests
python test_publish_only.py
python test_chrome_positioning.py
```

### Troubleshooting

#### Common Issues

##### 1. **Browser Launch Failures**
```bash
# Error: Browser not found
# Solution: Install Playwright browsers
playwright install chromium webkit

# Error: Permission denied
# Solution: Grant terminal permissions in macOS System Preferences
```

##### 2. **Configuration Issues**
```bash
# Error: Missing environment variables
# Solution: Verify .env file exists and contains required variables
cat .env | grep -E "(PAK_TOKEN|CLAUDE_API_KEY|PINE_RIDGE_BASE_URL)"

# Error: Invalid PAK token
# Solution: Verify token with Pine Ridge administrator
```

##### 3. **WebRTC Connection Issues**
```bash
# Error: Connection timeout
# Solution: Check network connectivity and firewall settings
ping pineridge-static.eng.airtime.com

# Error: Media permission denied
# Solution: Grant microphone/camera permissions to Terminal
```

##### 4. **Safari Permission Issues**
```bash
# Error: Safari permission popups
# Solution: The system automatically handles these, but if issues persist:
# 1. Reset Safari permissions: Safari > Settings > Websites > Camera/Microphone
# 2. Restart Safari completely
# 3. Re-run the test
```

#### Debug Mode
```bash
# Enable debug logging
export ENABLE_VERBOSE_LOGGING=true
python main.py --verbose

# Check logs
tail -f logs/pine_ridge_test_*.log

# View screenshots
open screenshots/
```

#### Performance Optimization
```bash
# Reduce screenshot quality for faster execution
export SCREENSHOT_QUALITY=60

# Reduce timeouts for faster feedback
export BROWSER_TIMEOUT=20
export WEBRTC_CONNECTION_TIMEOUT=20

# Increase retries for unstable networks
export MAX_RETRIES=5
```

### Deployment Scenarios

#### 1. **Local Development**
- Use default configuration
- Run tests manually
- Enable verbose logging for debugging

#### 2. **CI/CD Integration**
```yaml
# GitHub Actions example
name: WebRTC Test
on: [push, pull_request]
jobs:
  test:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install chromium webkit
      - name: Run tests
        env:
          PAK_TOKEN: ${{ secrets.PAK_TOKEN }}
          CLAUDE_API_KEY: ${{ secrets.CLAUDE_API_KEY }}
        run: python main.py
```

#### 3. **Production Monitoring**
```bash
# Run with monitoring
python main.py --verbose > production.log 2>&1

# Schedule regular runs
# Add to crontab:
# 0 */6 * * * cd /path/to/HappyTester && source venv/bin/activate && python main.py
```

### Maintenance

#### Regular Updates
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Update browsers
playwright install chromium webkit

# Update repository
git pull origin master
```

#### Log Management
```bash
# Clean old logs (keep last 7 days)
find logs/ -name "*.log" -mtime +7 -delete

# Clean old screenshots (keep last 100)
ls -t screenshots/ | tail -n +101 | xargs -I {} rm screenshots/{}
```

#### Health Checks
```bash
# Test system health
python -c "
import asyncio
from src.config.system_config import SystemConfig
from src.mcp.puppeteer_mcp_client import PuppeteerMCPClient

async def health_check():
    config = SystemConfig.load_from_env()
    client = PuppeteerMCPClient(config)
    await client.initialize_webrtc_testing()
    await client.cleanup()
    print('✅ System health check passed')

asyncio.run(health_check())
"
```

### Support

#### Getting Help
- **Documentation**: Check `ARCHITECTURE.md` for system details
- **Issues**: Report bugs on GitHub Issues
- **Community**: Join discussions in GitHub Discussions

#### Performance Monitoring
- **Metrics**: Check `logs/` directory for performance data
- **Screenshots**: Review `screenshots/` for visual evidence
- **Benchmarks**: Use provided performance benchmarks in `ARCHITECTURE.md`

### Security Considerations

#### API Key Security
- Never commit API keys to version control
- Use environment variables for all sensitive data
- Rotate API keys regularly
- Use separate keys for different environments

#### Browser Security
- System uses real browser instances (not headless) for security
- Automatic cleanup of browser profiles after tests
- No persistent storage of sensitive data

#### Network Security
- All external communications use HTTPS
- No sensitive data logged or stored
- Proper cleanup of temporary files

This deployment guide provides comprehensive instructions for setting up and running the Pine Ridge WebRTC Testing System in various environments. For additional help, consult the `ARCHITECTURE.md` file or open an issue on GitHub.