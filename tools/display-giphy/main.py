import os
import requests
from dotenv import load_dotenv
from obswebsocket import obsws, requests as obsreq
import time
from pathlib import Path

# Load .env from repository root (two levels up from this file)
repo_root = Path(__file__).resolve().parent.parent.parent
load_dotenv(dotenv_path=repo_root / '.env')

OBS_ADDRESS = os.getenv("OBS_ADDRESS", "localhost")
OBS_PORT = int(os.getenv("OBS_PORT", 4455))
OBS_PASSWORD = os.getenv("OBS_PASSWORD", "")
GIPHY_KEY = os.getenv("GIPHY_KEY")
GIPHY_TAG = "celebration"
SOURCE_NAME = "CelebrationGIF"

def get_gif_url(tag):
    """Fetch a random GIF URL from Giphy."""
    url = f"https://api.giphy.com/v1/gifs/random?api_key={GIPHY_KEY}&tag={tag}"
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()["data"]["images"]["original"]["url"]

def update_browser_source(ws, source_name, gif_url):
    """Update Browser Source using OBS WebSocket v5 request objects."""
    try:
        # Fetch current input settings
        resp = ws.call(obsreq.GetInputSettings(inputName=source_name))
        settings = resp.datain["inputSettings"]
        settings["url"] = gif_url
        original_css = settings.get("css", "") or ""
        # Add a trivial comment with a timestamp to force the browser source to detect a change
        settings["css"] = original_css + f"\n/* trigger update: {int(time.time()*1000)} */"

        # Apply updated settings
        ws.call(obsreq.SetInputSettings(
            inputName=source_name,
            inputSettings=settings,
            overlay=True
        ))
        print(f"🖼️ Updated '{source_name}' with GIF: {gif_url}")

    except Exception as e:
        print(f"❌ Failed to update source '{source_name}': {e}")

def main():
    ws = obsws(OBS_ADDRESS, OBS_PORT, OBS_PASSWORD)
    try:
        print("🔌 Connecting to OBS WebSocket...")
        ws.connect()
        print("✅ Connected to OBS")
        # Fetch GIF from Giphy
        gif_url = get_gif_url(GIPHY_TAG)
        print(f"\n🎞️ Fetched GIF URL: {gif_url}")

        # Update Browser Source
        update_browser_source(ws, SOURCE_NAME, gif_url)
        time.sleep(4)
    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        ws.disconnect()
        print("🔒 Disconnected from OBS")

if __name__ == "__main__":
    main()
