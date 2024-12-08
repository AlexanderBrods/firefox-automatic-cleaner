from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
from pathlib import Path
import shutil
import threading
import time


def find_firefox_cache():
    """Locate the Firefox cache directory automatically."""
    home = Path.home()
    profiles_dir = home / "AppData/Local/Mozilla/Firefox/Profiles"  # Default path on Windows

    if not profiles_dir.exists():
        print("Couldn't find the Firefox profiles directory.")
        return None

    # Look for a profile folder containing a 'cache2' directory
    for profile in profiles_dir.iterdir():
        cache_path = profile / "cache2"
        if cache_path.exists():
            return cache_path

    print("No Firefox cache directory found.")
    return None


def clear_firefox_cache(cache_path):
    """Delete files from the Firefox cache."""
    if cache_path and cache_path.exists():
        try:
            for item in cache_path.iterdir():
                if item.name == "index":  # Leave the `index` file alone
                    continue

                if item.is_dir() and item.name == "entries":  # Handle the `entries` folder
                    locked_files = 0
                    deleted_files = 0
                    for sub_item in item.iterdir():
                        try:
                            sub_item.unlink()  # Remove files in `entries`
                            deleted_files += 1
                        except Exception:
                            locked_files += 1
                    print(f"Removed {deleted_files} files from 'entries' folder. Skipped {locked_files} locked files.")
                    continue

                try:
                    if item.is_file():
                        item.unlink()  # Remove standalone files
                    elif item.is_dir():
                        shutil.rmtree(item)  # Delete folders like `doomed`
                except Exception:
                    pass  # Skip over files that can't be deleted
            print("Cache cleared successfully.")
        except Exception as e:
            print(f"Error while clearing cache: {e}")
    else:
        print("Cache path doesn't exist or couldn't be located.")


def background_task():
    """Continuously clear the cache every 2 hours."""
    while True:
        cache_path = find_firefox_cache()
        if cache_path:
            print("Starting cache cleanup...")
            clear_firefox_cache(cache_path)
        else:
            print("No cache directory to clean.")
        time.sleep(2 * 60 * 60)  # Wait for 2 hours before running again


def create_image():
    """Generate a simple icon for the system tray."""
    # Create a 64x64 icon with alternating blue and white rectangles
    width = 64
    height = 64
    color1 = "blue"
    color2 = "white"
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    dc.rectangle((0, height // 2, width // 2, height), fill=color2)
    return image


def on_exit(icon, item):
    """Shut down the system tray program."""
    print("Exiting...")
    icon.stop()


def main():
    """Set up the system tray app."""
    # Build the tray menu
    menu = Menu(
        MenuItem("Exit", on_exit)
    )

    # Create the system tray icon
    icon = Icon("Firefox Cache Cleaner", create_image(), "Firefox Cache Cleaner", menu)

    # Start the background cache-clearing task in a separate thread
    thread = threading.Thread(target=background_task, daemon=True)
    thread.start()

    # Keep the tray icon running until manually exited
    icon.run()


if __name__ == "__main__":
    main()