import pygame

from . import constants
from . import screen


# ============================================================ #
# World Class
# ============================================================ #


class World:
    def __init__(self):
        # store windows by their pid
        self._windows = {}
        self._windows_ref = set()

        # store the visible world in a list of rects
        # one rect for each monitor
        self._monitors = screen.MonitorRetrieval.get_all_monitors()
        self._visible_world_rect = pygame.Rect(0, 0, 0, 0)
        for monitor in self._monitors:
            self._visible_world_rect.union_ip(monitor._rect)
        # find min topleft corner
        self._visible_world_rect.topleft = (
            min([monitor._rect.topleft[0] for monitor in self._monitors]),
            min([monitor._rect.topleft[1] for monitor in self._monitors]),
        )

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def update(self):

        print("-" * 40)
        for window in screen.WindowManager.get_all_windows():
            # print(window)
            if window._window_id not in self._windows:
                self.add_window(window)
            else:
                # update information
                self._windows[window._window_id].update_info(window)
            self._windows[window._window_id]._last_alive = 0

        changes = []
        for window in self._windows_ref:
            # death counter
            window._last_alive += 1
            if window._last_alive > constants.FPS:
                changes.append(window)
            # check if onscreen or not
            if not window._onscreen:
                continue
            print(window)
        for c in changes:
            self.remove_window(c._window_id)

    # -------------------------------------------------------- #
    # utils
    # -------------------------------------------------------- #

    def add_window(self, window: screen.Window):
        self._windows[window._window_id] = window
        self._windows_ref.add(window)

    def get_window(self, window_id: int):
        return self._windows.get(window_id)

    def remove_window(self, window_id):
        if window_id in self._windows:
            self._windows_ref.remove(self._windows[window_id])
            del self._windows[window_id]

    def get_all_windows(self):
        return list(self._windows_ref)

    def in_visible_world(self, rect: pygame.Rect):
        for monitor in self._monitors:
            if monitor._rect.contains(rect):
                return True
        return False
