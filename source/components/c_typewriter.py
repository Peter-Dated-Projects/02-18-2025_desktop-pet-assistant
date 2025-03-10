from source import constants

from source.components import c_component

# ============================================================ #
# Typewriter
# ============================================================ #


class TypewriterComponent(c_component.Component):
    def __init__(self):
        super().__init__()
        self._total_string = ""
        self._step_speed = 10  # in characters per second
        self._timer = 0

        self._oversized = False

        # for optimization
        self._last_char = 0

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def update(self):
        if self._timer * self._step_speed >= len(self._total_string):
            self._oversized = True
            return
        self._timer += constants.DELTA_TIME

    def get_next_token(self):
        if self._oversized:
            return None

        _cur_char = int(self._timer * self._step_speed)
        if _cur_char > self._last_char:
            _result = self._total_string[self._last_char : _cur_char]
            self._last_char = _cur_char
            return _result
        return None

    def get_current_tokens(self):
        if self._oversized:
            return self._total_string
        return self._total_string[: int(self._timer * self._step_speed)]

    def set_string(self, string: str):
        self._total_string = string
        self._timer = 0
        self._oversized = False

    def set_speed(self, speed: int):
        self._step_speed = speed

    def is_finished(self):
        return self._oversized
