import pygame
import sys

from . import constants


# ============================================================ #
# Window Class
# ============================================================ #


class Window:
    def __init__(
        self,
        window_id: int,
        name: str,
        rect: pygame.FRect,
        title: str,
        pid: int,
        zlevel: int,
        onscreen: bool,
    ):
        self._window_id = window_id
        self._name = name
        self._rect = pygame.FRect(rect) if type(rect) is pygame.Rect else rect
        self._title = title
        self._pid = pid
        self._zlevel = zlevel
        self._onscreen = onscreen

        # last time window was alive
        self._last_alive = 0

        self._collision_lines = [
            pygame.Rect(rect.topleft, (rect.width, 1)),
            pygame.Rect(rect.bottomleft, (rect.width, 1)),
        ]

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def is_inside(self, rect: pygame.Rect):
        return self._rect.contains(rect)

    def update_info(self, window):
        self._name = window._name
        self._rect = window._rect
        self._title = window._title
        self._pid = window._pid
        self._zlevel = window._zlevel
        self._onscreen = window._onscreen

        # udpate collision lines
        self._collision_lines = [
            pygame.Rect(self._rect.topleft, (self._rect.width, 1)),
            pygame.Rect(self._rect.bottomleft, (self._rect.width, 1)),
        ]

    # -------------------------------------------------------- #
    # utils
    # -------------------------------------------------------- #

    def __str__(self):
        return f"Window: {self._window_id:8} | {self._name:20} | {self._title:15} ({self._pid:7}) | {self._zlevel:5} | {self._onscreen:1} | {self._rect}"


# ============================================================ #
# Monitor Info
# ============================================================ #


class MonitorInfo:
    def __init__(self, identifier, rect: pygame.Rect):
        self._identifier = identifier
        self._rect = rect

    # -------------------------------------------------------- #
    # utils
    # -------------------------------------------------------- #

    def __repr__(self):
        return f"Monitor: {self._identifier} ({self._rect})"


# ============================================================ #
# Monitor Information Retrieval
# ============================================================ #


if sys.platform == "darwin":
    from AppKit import NSScreen

    from Quartz import (
        kCGWindowListOptionOnScreenOnly,
        kCGNullWindowID,
        CGWindowListCopyWindowInfo,
    )

    class MonitorRetrieval:
        @classmethod
        def get_all_monitors(cls):
            monitors = []
            screens = NSScreen.screens()
            if not screens:
                raise Exception("No screens found!")

            for idx, screen in enumerate(screens):
                frame = screen.frame()
                # Convert NSRect (frame) to a pygame.Rect.
                # NSRect values are in points.
                global_rect = pygame.Rect(
                    int(frame.origin.x),
                    -int(frame.origin.y),
                    int(frame.size.width),
                    int(frame.size.height),
                )
                monitors.append(MonitorInfo(idx, global_rect))
            return monitors

    class WindowManager:
        @classmethod
        def get_all_windows(cls):
            windows = []

            options = kCGWindowListOptionOnScreenOnly
            window_list = CGWindowListCopyWindowInfo(options, kCGNullWindowID)

            for window in window_list:
                window_number = window.get("kCGWindowNumber", "No ID")
                rect = window["kCGWindowBounds"]
                title = window.get("kCGWindowName", "Unknown")
                pid = window["kCGWindowOwnerPID"]
                zlevel = window.get("kCGWindowLayer", 0)
                onscreen = not window.get("kCGWindowIsMiniaturized", False)
                name = window.get("kCGWindowOwnerName", "Unknown")

                if name in constants.ILLEGAL_WINDOWS:
                    continue
                if (
                    rect["Width"] < constants.MINIMUM_WIDTH
                    or rect["Height"] < constants.MINIMUM_HEIGHT
                ):
                    onscreen = False
                if zlevel < 0:
                    onscreen = False

                windows.append(
                    Window(
                        window_number,
                        name,
                        pygame.Rect(
                            rect["X"], rect["Y"], rect["Width"], rect["Height"]
                        ),
                        title,
                        pid,
                        zlevel,
                        onscreen,
                    )
                )

            return windows

elif sys.platform == "win32":
    import win32api
    import win32gui
    import win32process
    import win32con

    import psutil

    class MonitorRetrieval:
        MAX_DISPLAYS = 16

        @classmethod
        def get_all_monitors(cls):
            result = []
            monitors = win32api.EnumDisplayMonitors()
            for monitor in monitors:
                rect = monitor[2]
                result.append(MonitorInfo(len(result), pygame.Rect(rect)))

            return result

    class WindowManager:
        @classmethod
        def get_all_windows(cls):
            windows = []

            def win_callback(hwnd, window):
                w_number = hwnd
                w_name = psutil.Process(
                    win32process.GetWindowThreadProcessId(hwnd)[1]
                ).name()
                w_title = win32gui.GetWindowText(hwnd)
                w_rect = win32gui.GetWindowRect(hwnd)
                w_pid = win32process.GetWindowThreadProcessId(hwnd)[1]
                w_zlevel = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                w_onscreen = win32gui.IsWindowVisible(hwnd)

                # currently no filters
                if w_name in constants.ILLEGAL_WINDOWS:
                    return
                # if no area
                if (
                    w_rect[2] < constants.MINIMUM_WIDTH
                    or w_rect[3] < constants.MINIMUM_HEIGHT
                ):
                    return
                if w_zlevel < 0:
                    return

                # add to array
                windows.append(
                    Window(
                        w_number,
                        w_name,
                        pygame.Rect(w_rect),
                        w_title,
                        w_pid,
                        w_zlevel,
                        w_onscreen,
                    )
                )

            win32gui.EnumWindows(win_callback, windows)
            return windows
