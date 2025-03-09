import pygame

# ======================================================== #
# Entity Class
# ======================================================== #


class Entity:
    def __init__(self, x, y, width, height):
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

    def update_entity(self):
        for component in self.components:
            component.update()

    # -------------------------------------------------------- #
    # special functions
    # -------------------------------------------------------- #

    def __setitem__(self, key, value):
        self._extra[key] = value

    def __getitem__(self, key):
        return self._extra[key]
