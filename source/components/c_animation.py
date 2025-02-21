from . import c_component

from source import graphics
from source import constants

# ============================================================ #
# Animation Component
# ============================================================ #


class AnimationComponent(c_component.Component):
    def __init__(self, animation: graphics.Animation):
        super().__init__()
        self._animation = animation.get_registry()

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def update(self):
        self._animation.update()

        # render the current frame
        sprite = self._animation.get_current_frame()
        constants.WINDOW_CONTEXT._fb_painter.drawPixmap(
            int(self.entity.position.x), int(self.entity.position.y), sprite._qpixmap
        )
