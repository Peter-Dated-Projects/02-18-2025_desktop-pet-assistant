import pygame


class World:
    def __init__(self):
        pass


# ============================================================ #
# Window Class
# ============================================================ #


class Window:
    def __init__(self, rect: pygame.Rect, title: str, pid: int):
        self._rect = rect
        self._title = title
        self._pid = pid

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    # -------------------------------------------------------- #
    # utils
    # -------------------------------------------------------- #

    def __str__(self):
        return f"Window: {self._title} ({self._pid})"
