import sys


DELTA_TIME = 0
START_TIME = 0
END_TIME = 0
RUNTIME = 0

FPS = 16

RUNNING = True

# ============================================================ #


WINDOW_SIZE = (100, 100)
WINDOW_TITLE = "Stella"


APP_CONTEXT = None
WINDOW_CONTEXT = None

MINIMUM_WIDTH = 200
MINIMUM_HEIGHT = 200

SIGNAL_HANDLER = None
ASYNC_TASK_HANDLER = None

ENTITY_EXIT_SIGNAL = "entity_exit"

# ============================================================ #


if sys.platform == "darwin":
    ILLEGAL_WINDOWS = {
        "Dock",
        "Control Center",
        "TextInputMenuAgent",
        "Screenshot",
        "Window Server",
        "Notification Center",
        "Dock",
        "Wallpaper",
    }
elif sys.platform == "win32":
    ILLEGAL_WINDOWS = {
        "explorer.exe",
        "NVDisplay.Container.exe",
        "explorer.exe",
        "TextInputHost.exe",
    }


# ============================================================ #
# env variables

GRAVITY = 9.8
