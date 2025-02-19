from source import constants
from source import physics

import PyQt5.QtGui as qtg

# ============================================================ #
# Assistant Class
# ============================================================ #


class Assistant(physics.entity.Entity):
    def __init__(self):
        super().__init__(0, 0, constants.WINDOW_SIZE[0], constants.WINDOW_SIZE[1])

        self.velocity.x = -100

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def update(self):
        super().update()

        # update entity location with app location (because shared location)
        self.position.xy = constants.WINDOW_CONTEXT._rect.topleft
        self.rect.topleft = self.position.xy

        constants.WINDOW_CONTEXT._framebuffer.fill(qtg.QColor(255, 192, 203))
        touching = self._world.move_entity(self)

        print("assistant update", *map(int, self.position))
        # abuse app location to move the window
        constants.WINDOW_CONTEXT._rect.topleft = self.position.xy
