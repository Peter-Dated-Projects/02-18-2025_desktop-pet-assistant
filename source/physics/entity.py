import pygame
from PyQt5.QtWidgets import QWidget

from source import constants

# ======================================================== #
# Entity Class
# ======================================================== #


class Entity(QWidget):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.rect = pygame.FRect(x, y, width, height)
        self.components = []

        self.dead = False
        self._extra = {}

        # world reference
        self._world = None

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def add_component(self, component):
        self.components.append(component)
        component.entity = self
        component.__post_init__()

        return component

    def update(self):
        for component in self.components:
            component.update()
            # print("updating comp", component)

    # -------------------------------------------------------- #
    # special functions
    # -------------------------------------------------------- #

    def __setitem__(self, key, value):
        self._extra[key] = value

    def __getitem__(self, key):
        return self._extra[key]
