firefox-automatic-cleaner

A lightweight tool that runs in the system tray and clears Firefox cache every 2 hours to improve browsing performance.

Features

Automatically detects and clears Firefox cache every 2 hours.

Runs silently in the system tray.

Skips locked files to avoid interruptions.

Improves browser performance by managing cache size.

Requirements

Python 3.7 or newer

Libraries:

pystray

pillow

Installation

Clone this repository:

git clone https://github.com/AlexanderBrods/firefox-automatic-cleaner.git
cd firefox-automatic-cleaner

Install the required dependencies:

pip install pystray pillow

Run the script:

python Firefox_cleaner_auto.py

How It Works

When you run the script, it creates a system tray icon.

The script continuously monitors and clears the Firefox cache every 2 hours.

You can exit the script by right-clicking the tray icon and selecting "Exit."
