# Display Giphy

Fetches random GIFs from Giphy and displays them in OBS via Browser Source using WebSocket control. Perfect for showing celebration GIFs, reactions, or themed animations during your stream.

## Features

- Fetch random GIFs from Giphy based on tags
- Automatically update OBS Browser Sources via WebSocket
- Forces browser source refresh using CSS timestamp trick
- Configurable GIF tags, source names, and OBS connection settings

## Requirements

- Python 3.11 or compatible version
- OBS Studio with WebSocket server enabled
- Giphy API key (free tier available)

## Installation

### 1. Install Python Dependencies

From the repository root:

```bash
pip install -r tools/display-giphy/requirements.txt
```

Or from this directory:

```bash
cd tools/display-giphy
pip install -r requirements.txt
```

### 2. Configure Environment Variables

**Important**: This tool uses the `.env` file located at the **repository root**, not in this directory.

From the repository root:

```bash
cp .env.example .env
```

Edit the `.env` file with your settings:

```env
# OBS WebSocket Configuration
OBS_ADDRESS=localhost
OBS_PORT=4455
OBS_PASSWORD=your_obs_password_here

# Giphy API Configuration
GIPHY_KEY=your_giphy_api_key_here
```

#### Getting a Giphy API Key

1. Go to [Giphy Developers](https://developers.giphy.com/)
2. Create an account or log in
3. Create a new app
4. Copy your API key
5. Add it to the `.env` file

#### Enabling OBS WebSocket

1. Open OBS Studio
2. Go to **Tools → WebSocket Server Settings**
3. Check **Enable WebSocket Server**
4. Note the **Server Port** (default: 4455)
5. Set a **Server Password** if desired
6. Add these values to your `.env` file

### 3. Configure OBS Browser Source

1. In OBS, add a **Browser Source** to your scene
2. Name it `CelebrationGIF` (or customize the `SOURCE_NAME` in [main.py:15](main.py#L15))
3. Set the initial URL to any GIF or leave it blank
4. Adjust width/height as needed

## Usage

### Running the Script

From the repository root:

```bash
python tools/display-giphy/main.py
```

Or from this directory:

```bash
cd tools/display-giphy
python main.py
```

### Customization

Edit [main.py](main.py) to customize behavior:

```python
GIPHY_TAG = "celebration"      # Line 14: Change the GIF search tag
SOURCE_NAME = "CelebrationGIF" # Line 15: Change the OBS source name
```

You can modify the `main()` function to accept command-line arguments for dynamic tag selection.

## How It Works

1. Connects to OBS via WebSocket
2. Fetches a random GIF URL from Giphy API using the specified tag
3. Retrieves current Browser Source settings
4. Updates the URL to the new GIF
5. Adds a timestamp comment to the CSS to force browser refresh
6. Applies the updated settings
7. Waits 4 seconds for the GIF to load
8. Disconnects from OBS

## Troubleshooting

### Connection Errors

**Error**: `Failed to connect to OBS WebSocket`

- Verify OBS is running
- Check WebSocket server is enabled in OBS
- Confirm `OBS_ADDRESS`, `OBS_PORT`, and `OBS_PASSWORD` in `.env` are correct

### Source Not Found

**Error**: `Failed to update source 'CelebrationGIF'`

- Verify the Browser Source exists in your current scene
- Check the source name matches `SOURCE_NAME` in [main.py:15](main.py#L15)
- Ensure the source is not locked or hidden

### Giphy API Errors

**Error**: `HTTP 401 Unauthorized` or `HTTP 403 Forbidden`

- Verify your `GIPHY_KEY` in `.env` is correct
- Check your API key hasn't exceeded rate limits
- Ensure the API key is active in your Giphy dashboard

### GIF Not Updating

If the GIF doesn't change in OBS:

- The Browser Source might be cached - try reloading it manually first
- Increase the sleep time in [main.py:58](main.py#L58) to allow more time for loading
- Check the OBS Browser Source URL is being updated in the source settings

## Integration Ideas

### Stream Deck

Create a Stream Deck button to trigger the script:

1. Add a **System → Open** action
2. Set the path to your Python executable
3. Set arguments to the full path of `main.py`

### Chat Bot Integration

Integrate with your chat bot (e.g., Nightbot, StreamElements) to run this script when viewers redeem channel points or use specific commands.

### Hotkey Trigger

Use a tool like AutoHotkey to bind a keyboard shortcut to run the script.

## Future Enhancements

- Command-line arguments for dynamic tag selection
- Multiple GIF sources with different tags
- Integration with Twitch/YouTube events
- Automatic GIF rotation on interval
- Support for multiple Browser Sources

## License

Free to use and modify as needed!
