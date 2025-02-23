from source.components import c_component


# ============================================================ #
# State Component
# ============================================================ #


class State:
    def __init__(self):
        self._statemachine = None

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass


# ============================================================ #
# Statemachine Component
# ============================================================ #


class StateMachineComponent(c_component.Component):

    def __init__(self, initial_state: str = None, states: dict[str, State] = {}):
        super().__init__()
        self._states = states
        self._current_state = initial_state

        self._next_state: str = None
        self._prev_state: str = None

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def update(self):
        if not self._current_state:
            if self._next_state:
                self._prev_state = self._current_state
                self._current_state = self._next_state
                self._states[self._current_state].enter()
                self._next_state = None
            return

        # update state machine
        self._states[self._current_state].update()

        # check if next state required
        if self._next_state is not None:
            self._states[self._current_state].exit()
            self._prev_state = self._current_state
            self._current_state = self._next_state
            self._states[self._current_state].enter()
            self._next_state = None

    def queue_state_change(self, state: str):
        self._next_state = state

    def add_state(self, statename: str, state: State):
        self._states[statename] = state
        if not self._current_state:
            self._next_state = statename
        self._states[statename]._statemachine = self
