import sys


DELTA_TIME = 0
START_TIME = 0
END_TIME = 0

FPS = 16

# ============================================================ #


WINDOW_SIZE = (100, 100)
WINDOW_TITLE = "Stella"

MINIMUM_WIDTH = 200
MINIMUM_HEIGHT = 200

# ============================================================ #


if sys.platform == "darwin":
    ILLEGAL_WINDOWS = [
        "Dock",
        "Control Center",
        "TextInputMenuAgent",
        "Screenshot",
        "Window Server",
        "Notification Center",
        "Dock",
        "Wallpaper",
    ]
elif sys.platform == "win32":
    pass
