import PIL

from . import c_component
from source import constants

from PyQt5.QtGui import QPixmap, QImage

# ============================================================ #
# Sprite Component
# ============================================================ #


class SpriteComponent(c_component.Component):
    def __init__(self, sprite_data: PIL.Image, metadata: dict = {}):
        super().__init__()
        self._raw_sprite = sprite_data
        self._metadata = metadata

        # convert + store data into a qpixmap
        self._raw_sprite = self._raw_sprite.convert("RGBA")
        data = self._raw_sprite.tobytes("raw", "RGBA")
        bytes_per_line = self._raw_sprite.width * 4

        # create pyqt related objects
        self._qimage = QImage(
            data,
            self._raw_sprite.width,
            self._raw_sprite.height,
            bytes_per_line,
            QImage.Format_RGBA8888,
        )
        self._qimage = self._qimage.convertToFormat(QImage.Format_ARGB32_Premultiplied)
        self._qpixmap = QPixmap.fromImage(self._qimage)

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def update(self, entity):
        # draw the pixmap onto the screen
        constants.WINDOW_CONTEXT._fb_painter.drawPixmap(
            entity.position.x, entity.position.y, self._qpixmap
        )

    # -------------------------------------------------------- #
    # special functions
    # -------------------------------------------------------- #

    def __getitem__(self, key):
        return self._metadata.get(key)

    def __setitem__(self, key, value):
        self._metadata[key] = value
