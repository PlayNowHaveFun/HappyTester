# Pine Ridge Test Automation

Automated testing framework for Pine Ridge WebRTC application using Claude Computer Use.

## Overview

This framework automates the execution of Pine Ridge test case C107928 (Publish Local Stream) using:
- Chrome browser as publisher
- Safari browser as subscriber  
- Claude Computer Use for browser automation
- Manual verification for audio quality

## Prerequisites

- macOS 12.0+ (Monterey or later)
- Python 3.9+
- Chrome browser (latest)
- Safari browser (latest)
- Claude API access

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd HappyTester
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your actual values
```

## Configuration

Edit the `.env` file with your configuration:

```env
# Pine Ridge Settings
PINE_RIDGE_BASE_URL=https://pineridge-static.eng.airtime.com/
DEFAULT_CHANNEL_ID=QAtest
PAK_TOKEN=your_pak_token_here

# Claude Computer Use
CLAUDE_API_KEY=your_claude_api_key_here

# Browser Settings
BROWSER_TIMEOUT=30
VERIFICATION_TIMEOUT=300
SCREENSHOT_DIR=./screenshots
```

## Usage

Run the test automation:

```bash
python main.py
```

## Test Flow

1. **Chrome Publisher Setup**:
   - Launches Chrome browser
   - Navigates to Pine Ridge URL
   - Clicks "Join Channel"
   - Verifies joined state
   - Clicks "Publish Audio"
   - Verifies channel panel with Stop button

2. **Safari Subscriber Setup**:
   - Launches Safari browser
   - Navigates to Pine Ridge URL
   - Joins the same channel
   - Positions window for verification

3. **Manual Verification**:
   - Displays verification prompt
   - User manually verifies audio transmission
   - Accepts Pass/Fail input with comments

4. **Results**:
   - Displays test results
   - Captures screenshots
   - Logs execution details

## Manual Verification

During execution, you will see:
- Chrome window on the left (publisher)
- Safari window on the right (subscriber)
- Command line prompt for verification

Verify that:
- Audio is being transmitted from Chrome to Safari
- You can hear the audio in Safari
- Both browsers show active connection

Enter 'p' for PASS or 'f' for FAIL when prompted.

## Project Structure

```
HappyTester/
├── src/
│   ├── automation/
│   │   ├── browser_controller.py    # Base browser automation
│   │   ├── chrome_publisher.py      # Chrome publisher logic
│   │   ├── safari_subscriber.py     # Safari subscriber logic
│   │   └── test_executor.py         # Test coordination
│   └── utils/
│       ├── config.py                # Configuration management
│       ├── logger.py                # Logging utilities
│       ├── screenshot.py            # Screenshot capture
│       └── verification.py          # Manual verification interface
├── main.py                          # Main entry point
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
└── README.md                        # This file
```

## Troubleshooting

**Browser Launch Issues**:
- Ensure Chrome and Safari are installed
- Check browser permissions for automation
- Verify microphone permissions

**Connection Issues**:
- Verify PAK token is valid
- Check network connectivity
- Ensure WebRTC ports are open

**Claude API Issues**:
- Verify API key is correct
- Check API rate limits
- Ensure Computer Use is enabled

## Logging

Logs are saved in `logs/` directory with timestamps.
Screenshots are saved in `screenshots/` directory.

## Future Enhancements

- Firefox browser support
- Windows platform support
- Automated audio quality verification
- TestRail integration
- Parallel test execution