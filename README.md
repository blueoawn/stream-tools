# Stream Tools

A collection of modular streaming tools for OBS Studio. Each tool can be used independently or together as part of your streaming setup.

## Available Tools

### 1. Display Giphy
Fetches random GIFs from Giphy and displays them in OBS via Browser Source using WebSocket control.

**Use case**: Automatically show celebration GIFs, reactions, or themed animations during your stream.

[📖 Full Documentation](tools/display-giphy/)

**Quick start**:
```bash
# From repository root
cp .env.example .env  # Configure once for all tools
pip install -r tools/display-giphy/requirements.txt
python tools/display-giphy/main.py
```

### 2. Shake Everything
An OBS Python script that shakes all scene items with configurable intensity and duration. Perfect for adding dynamic effects triggered by hotkeys or Stream Deck.

**Use case**: Add visual impact to channel points redemptions, alerts, or dramatic moments.

[📖 Full Documentation](tools/shake-everything/)

**Quick start**:
1. Open OBS Studio → Tools → Scripts
2. Configure Python 3.11 in Python Settings tab
3. Load `tools/shake-everything/main.py`
4. Configure hotkey in OBS Settings → Hotkeys
5. Press your hotkey to shake!

## Installation Options

### Option 1: Clone Everything (Recommended)
Get access to all tools in one place:

```bash
git clone https://github.com/blueoawn/stream-tools.git
cd stream-tools
```

### Option 2: Individual Tool Installation
Each tool is self-contained in its own directory. You can:

1. Download just the tool folder you need
2. Navigate to `tools/<tool-name>/` after cloning
3. Follow the individual tool's README for setup

## Quick Start

### 1. Configure Environment Variables

**Important**: All tools that require configuration use a shared `.env` file in the repository root.

```bash
# Copy the example file
cp .env.example .env

# Edit with your settings
nano .env  # or use your preferred editor
```

The `.env` file contains:
- **OBS WebSocket settings** (address, port, password)
- **Giphy API key** (for display-giphy tool)

Tools will automatically look for this file at the repository root.

### 2. Install Tool Dependencies

Each tool has its own `requirements.txt`. Install dependencies for the tools you want to use:

```bash
# For display-giphy
pip install -r tools/display-giphy/requirements.txt

# shake-everything uses OBS's built-in Python - no separate install needed
```

## Project Structure

```
stream-tools/
├── README.md                      # This file
├── .env.example                   # Shared configuration template
├── .gitignore                     # Git ignore rules
└── tools/
    ├── display-giphy/            # Giphy → OBS integration
    │   ├── main.py
    │   ├── requirements.txt
    │   └── README.md
    └── shake-everything/         # OBS scene shake effect
        ├── main.py
        ├── README.md
        ├── requirements.txt
        └── images/
```

## Requirements

### General Requirements
- **OBS Studio** (version 27.0 or newer)
- **Python 3.11** (64-bit or 32-bit to match your OBS installation)

### Tool-Specific Requirements
Each tool has its own `requirements.txt` or dependencies. Check the individual tool's README for details.

## Contributing

Have a new stream tool idea? Contributions are welcome!

1. Fork the repository
2. Create a new directory under `tools/` for your tool
3. Include a comprehensive README.md with setup instructions
4. Keep dependencies isolated (separate `requirements.txt` per tool)
5. Submit a pull request

### Guidelines for New Tools
- **Modular**: Each tool should work independently
- **Documented**: Include clear setup and usage instructions
- **Self-contained**: Keep all dependencies within the tool's directory
- **Secure**: Use `.env` files for sensitive data (never commit secrets!)

## Troubleshooting

### Python Version Issues
- OBS Studio requires Python 3.11 or earlier (3.13 is not yet supported)
- Ensure Python architecture matches OBS (64-bit vs 32-bit)

### OBS WebSocket Connection
For tools using OBS WebSocket:
1. Enable WebSocket server in OBS: Tools → WebSocket Server Settings
2. Note the port (default: 4455) and password
3. Update your `.env` file with these credentials

### General Tips
- Check individual tool READMEs for specific troubleshooting
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Ensure `.env` files are configured correctly (never use `.env.example` directly)

## License

Each tool may have its own license. Check individual tool directories for details.

## Support

If you encounter issues:
1. Check the individual tool's README and troubleshooting section
2. Verify all requirements are met (Python version, OBS version, etc.)
3. Open an issue on GitHub with detailed error information

## Roadmap

Future tool ideas:
- Stream deck integration templates
- Chat command triggers
- Twitch/YouTube API integrations
- Audio reactive visualizations
- Scene switcher automation

Have a suggestion? Open an issue or submit a PR!

---

**Happy Streaming!** 🎥✨
