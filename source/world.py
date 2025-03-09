import pygame

from . import constants
from . import screen
from . import signal

from . import physics


# ============================================================ #
# World Class
# ============================================================ #


class World:
    def __init__(self):
        # store windows by their pid
        self._windows = {}
        self._windows_ref = set()

        # entities
        self._entites = {}

        # store the visible world in a list of rects
        # one rect for each monitor
        self._monitors = screen.MonitorRetrieval.get_all_monitors()
        self._visible_world_rect = pygame.Rect(0, 0, 0, 0)
        for monitor in self._monitors:
            self._visible_world_rect.union_ip(monitor._rect)
            print(monitor, self._visible_world_rect)
        # find min topleft corner
        self._visible_world_rect.topleft = (
            min([monitor._rect.topleft[0] for monitor in self._monitors]),
            min([-monitor._rect.topleft[1] for monitor in self._monitors]),
        )

        # initialize the signal for when entity exits world
        self._entity_exit_signal = constants.SIGNAL_HANDLER.register_signal(
            constants.ENTITY_EXIT_SIGNAL, [physics.entity.Entity]
        )

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def update(self):
        # -------------------------------------------------------- #
        # print monitors
        # print("-" * 40)
        # for monitor in screen.MonitorRetrieval.get_all_monitors():
        #     print(monitor)
        # -------------------------------------------------------- #
        # update windows
        # print("*" * 40)
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
        for c in changes:
            self.remove_window(c._window_id)

        # -------------------------------------------------------- #
        # update visible world
        # -------------------------------------------------------- #
        changes = []
        for entity in self._entites.values():
            entity.window_update()
            if entity.dead:
                changes.append(entity)
        for c in changes:
            self.remove_entity(c)

    def move_entity(self, entity):
        touching = {"left": False, "right": False, "top": False, "bottom": False}

        # forces
        # entity.velocity.y += constants.GRAVITY * constants.DELTA_TIME
        entity.position.xy += entity.velocity.xy * constants.DELTA_TIME

        # check if entity exits visible windows
        if not self.in_visible_world(entity.rect):
            # TODO - entity should not be moving at MACH 10 speed lol
            # find closest monitor
            closest_monitor = None
            for monitor in self._monitors:
                if monitor._rect.colliderect(entity.rect):
                    closest_monitor = monitor
                    break

            if not closest_monitor:
                # should just teleport entity back into screen
                print("ENTITY EXITED SCREEN")
            else:
                self._entity_exit_signal.emit(entity)

                # Update touching based on the closest monitor
                if entity.rect.left < closest_monitor._rect.left:
                    touching["left"] = True
                if entity.rect.right > closest_monitor._rect.right:
                    touching["right"] = True
                if entity.rect.top < closest_monitor._rect.top:
                    touching["top"] = True
                if entity.rect.bottom > closest_monitor._rect.bottom:
                    touching["bottom"] = True

        # only interact on y axis
        for rect in self.collide_windows(entity.rect):
            if entity.rect.colliderect(rect):
                if rect.top == entity.rect.bottom:
                    touching["bottom"] = True
                if rect.bottom == entity.rect.top:
                    touching["top"] = True
                entity.velocity.y = 0
                break

        return touching

    # -------------------------------------------------------- #

    def collide_windows(self, rect):
        for window in self._windows_ref:
            if window.is_inside(rect):
                if window._collision_lines[0].colliderect(rect):
                    yield window._collision_lines[0]
                if window._collision_lines[1].colliderect(rect):
                    yield window._collision_lines[1]

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

    def add_entity(self, entity):
        self._entites[id(entity)] = entity
        entity._world = self

    def remove_entity(self, entity):
        del self._entites[id(entity)]

    def get_entity(self, entity_id):
        return self._entites.get(entity_id)
