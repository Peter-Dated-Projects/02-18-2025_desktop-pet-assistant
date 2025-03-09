from . import c_component

from source import graphics
from source import constants

from PyQt5.QtGui import QTransform

# ============================================================ #
# Animation Component
# ============================================================ #


class AnimationComponent(c_component.Component):
    def __init__(self, animation: graphics.Animation):
        super().__init__()
        self._animation = animation
        self._registry = self._animation.get_registry()

        self._x_flip = False
        self._y_flip = False

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def update(self):
        self._registry.update()
        # render the current frame
        sprite = self._registry.get_current_frame()
        if self._x_flip:
            sprite = sprite.transformed(QTransform().scale(-1, 1))
        if self._y_flip:
            sprite = sprite.transformed(QTransform().scale(1, -1))

        self.entity._fb_painter.drawPixmap(
            int(self.entity.position.x), int(self.entity.position.y), sprite
        )

    def set_animation(self, name: str):
        self._animation = graphics.Animation.get_animation(name)
        if self._animation is None:
            return
        self._registry = self._animation.get_registry()

    def get_current_frame(self):
        return self._registry.get_current_frame()

    # -------------------------------------------------------- #
    # special functions
    # -------------------------------------------------------- #

    @property
    def finished(self):
        if not self._registry:
            return True
        return self._registry._finished

    @property
    def xflipped(self):
        return self._x_flip

    @property
    def yflipped(self):
        return self._y_flip

    @xflipped.setter
    def xflipped(self, value):
        self._x_flip = value

    @yflipped.setter
    def yflipped(self, value):
        self._y_flip = value
