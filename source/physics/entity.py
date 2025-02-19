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
        self.rect = pygame.Rect(x, y, width, height)
        self.components = []

        self.dead = False

        # world reference
        self._world = None

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def add_component(self, component):
        self.components.append(component)

    def update(self):
        for component in self.components:
            component.update(self)
