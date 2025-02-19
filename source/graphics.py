# ============================================================ #
# Animation Handler
# ============================================================ #


class AnimationHandler:
    CACHE = {}

    @classmethod
    def add_animation(cls, name, animation):
        cls.CACHE[name] = animation

    @classmethod
    def get_animation(cls, name):
        return cls.CACHE.get(name)

    @classmethod
    def remove_animation(cls, name):
        if name in cls.CACHE:
            del cls.CACHE[name]


# ============================================================ #
# Animation Class
# ============================================================ #


class Animation:
    def __init__(self):
        pass


# ============================================================ #
# Animation Registry
# ============================================================ #


class AnimationRegistry:
    def __init__(self, parent):
        self._parent = parent
        self._current_animation = None
        self._frame = 0
        self._timer = 0

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #
