import pygame
import random
import types

import os
import PyQt5.QtCore as qtc
from PyQt5.QtGui import QTransform

from source import screen
from source import graphics
from source import constants
from source import physics
from source import signal

from source import multiqtwindow
from source.components import c_animation
from source.components import c_statemachine

from game.components import c_wake_word

from game.windows import transparentwindow


# ============================================================ #

WINDOW_AREA = (100, 100)

SIT = ["Sit_1", "Sit_2"]
IDLE = ["Idle_1", "Idle_2"]
WALK = ["W_1", "W_2", "W_3"]
RUN = ["Run_1", "Run_2"]
REST = ["Rest_1", "Rest_2"]
DREAM = ["Dream"]
CREEP = ["Creep"]
CRAWL = ["Crawl"]

# sit down motion
SITUPDOWN = ["Sit_U_D"]
SITDOWN = ["Sit_D"]
SITUP = ["Sit_U"]
STOP = ["Stop"]
AGRESS = ["Agress"]

LOOK_AROUND = ["R_A_Right", "R_A_Left"]


JUMP = ["J_1", "J_2", "J_3"]
JUMPUPDOWN = ["J_U_D"]

BOWSIT = ["Bow_Sit"]
BOWSITIDK = ["B_S_1", "B_S_2"]

BOWIDLE = ["Bow_Idle"]
BOWIDLEIDK = ["B_I_1", "B_I_2"]

MAX_VELOCITY = 30
WEIGHT = 1

# ============================================================ #
# Assistant States
# ============================================================ #]


IDLE_STATE = "idle_state"
WALK_STATE = "walk_state"
RUN_STATE = "run_state"
RESTING_STATE = "resting_state"
LOOK_AROUND_STATE = "look_around_state"
LICK_PAW_STATE = "lick_paw_state"

SIT_STATE = "sit_state"
BOW_SIT_STATE = "bow_sit_state"
SLEEP_STATE = "sleep_state"
DIG_DIRT_STATE = "dig_dirt_state"
POOP_STATE = "poop_state"
HOLD_STATE = "hold_state"

SLEEP_TO_IDLE_TRANSITION_STATE = "sleep_to_idle_transition_state"
SIT_TO_IDLE_TRANSITION_STATE = "sit_to_idle_transition_state"
DIG_TO_POOP_TRANSITION_STATE = "dig_to_poop_transition_state"
IDLE_TO_SIT_TRANSITION_STATE = "idle_to_sit_transition_state"

# aggress related states
AGGRESS_STATE = "aggress_state"

# -------------------------------------------------------- #
# transitions
IDLE_TRANSITIONS = [
    WALK_STATE,
    RESTING_STATE,
    IDLE_STATE,
    LOOK_AROUND_STATE,
    LICK_PAW_STATE,
    IDLE_TO_SIT_TRANSITION_STATE,
    # AGGRESS_STATE,
]
WALK_TRANSITIONS = [IDLE_STATE]
REST_TRANSITIONS = [IDLE_STATE, SLEEP_STATE]
SLEEP_TRANSITIONS = [SLEEP_TO_IDLE_TRANSITION_STATE]
LOOK_AROUND_TRANSITIONS = [IDLE_STATE, DIG_DIRT_STATE]
DIG_DIRT_TRANSITIONS = [DIG_TO_POOP_TRANSITION_STATE]
DIG_TO_POOP_TRANSITION_TRANSITIONS = [POOP_STATE]
POOP_TRANSITIONS = [IDLE_STATE]
LICK_PAW_TRANSITIONS = [IDLE_STATE]
RUN_TRANSITIONS = [IDLE_STATE]

SIT_TO_IDLE_TRANSITION_TRANSITIONS = [IDLE_STATE]
IDLE_TO_SIT_TRANSITION_TRANSITIONS = [SIT_STATE]
SLEEP_TO_IDLE_TRANSITION_TRANSITIONS = [IDLE_STATE]
DIG_TO_POOP_TRANSITION_TRANSITIONS = [POOP_STATE]


# idle state
class IdleState(c_statemachine.State):

    def __init__(self):
        super().__init__()

        self._wait_time = 0
        self._counter = 0

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def enter(self):
        self._statemachine.entity._c_animation.set_animation(random.choice(IDLE))
        self._wait_time = random.random() * 5 + 1
        self._counter = 0
        self._statemachine.entity.velocity.x = 0

    def exit(self):
        pass

    def update(self):
        self._counter += constants.DELTA_TIME

        if self._counter > self._wait_time:
            # print("transitionng")
            self._statemachine.entity._c_statemachine.queue_state_change(
                random.choice(IDLE_TRANSITIONS)
            )


class LookAroundState(c_statemachine.State):
    def __init__(self):
        super().__init__()

        self._wait_time = 0
        self._counter = 0

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def enter(self):
        self._statemachine.entity._c_animation.set_animation(random.choice(LOOK_AROUND))

    def update(self):
        # check when animation finishes
        if self._statemachine.entity._c_animation.finished:
            # move onto next state
            self._statemachine.entity["holding_time"] = random.random() * 2 + 1
            self._statemachine.entity["holding_frame"] = (
                self._statemachine.entity._c_animation.get_current_frame()
            )
            self._statemachine.entity._c_statemachine.queue_state_change("hold_state")


class HoldFrameState(c_statemachine.State):
    def __init__(self):
        super().__init__()

        self._wait_time = 0
        self._counter = 0

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def enter(self):
        self._wait_time = self._statemachine.entity["holding_time"]
        self._counter = 0

    def update(self):
        self._counter += constants.DELTA_TIME
        if self._counter > self._wait_time:
            self._statemachine.entity._c_statemachine.queue_state_change(
                random.choice(LOOK_AROUND_TRANSITIONS)
            )


class WalkState(c_statemachine.State):

    def __init__(self):
        super().__init__()

        self._target_position = pygame.Vector2(0, 0)
        self._enter_run = False

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def enter(self):
        self._statemachine.entity._c_animation.set_animation(random.choice(WALK))
        self._target_position = self._generate_target_position()
        self._enter_run = random.choice([True, False, True])

        # extra info
        self._statemachine.entity["target_location"] = self._target_position

    def update(self):
        # print(
        #     f"CURRENT: WALK -- {self._target_position} | {self._statemachine.entity.position.xy}"
        # )

        # check distance
        t_distance = self._statemachine.entity.position.distance_to(
            self._target_position
        )

        # check if should run
        if self._enter_run and t_distance < 100:
            self._statemachine.entity._c_statemachine.queue_state_change(RUN_STATE)
            return
        # check if at target position
        if t_distance < 10:
            self._statemachine.entity._c_statemachine.queue_state_change(
                random.choice(WALK_TRANSITIONS)
            )
            return

        # move towards target position
        direction = self._target_position - self._statemachine.entity.position
        direction = direction.normalize() * MAX_VELOCITY
        self._statemachine.entity.velocity.xy = direction

    # -------------------------------------------------------- #
    # utils
    # -------------------------------------------------------- #

    def _generate_target_position(self):
        t_offset = [0, 0]
        t_position = [0, 0]

        # pick a monitor
        t_monitor = random.choice(screen.MonitorRetrieval.get_all_monitors())
        t_window = random.choice(
            [
                w
                for w in screen.WindowManager.get_all_windows()
                if t_monitor._rect.contains(w._rect)
            ]
        )
        t_position = t_window._rect.topleft

        return pygame.Vector2(t_offset[0] + t_position[0], t_offset[1] + t_position[1])


class RestingState(c_statemachine.State):

    def __init__(self):
        super().__init__()

        self._wait_time = 0
        self._counter = 0

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def enter(self):
        self._statemachine.entity._c_animation.set_animation(random.choice(REST))
        self._wait_time = random.random() * 5 + 1
        self._counter = 0
        self._statemachine.entity.velocity.x = 0

    def update(self):
        # print(
        #     f"CURRENT: REST -- {self._wait_time:5.2f} | Counter: {self._counter:5.2f}"
        # )
        self._counter += constants.DELTA_TIME
        if self._counter > self._wait_time:
            self._statemachine.entity._c_statemachine.queue_state_change(
                random.choice(REST_TRANSITIONS)
            )


class LickPawState(c_statemachine.State):
    def __init__(self):
        super().__init__()

        self._wait_time = 0
        self._counter = 0

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def enter(self):
        self._statemachine.entity._c_animation.set_animation(random.choice(REST))
        self._wait_time = random.random() * 5 + 1
        self._counter = 0
        self._statemachine.entity.velocity.x = 0

    def update(self):
        # print(
        #     f"CURRENT: REST -- {self._wait_time:5.2f} | Counter: {self._counter:5.2f}"
        # )
        self._counter += constants.DELTA_TIME
        if self._counter > self._wait_time:
            self._statemachine.entity._c_statemachine.queue_state_change(
                random.choice(LICK_PAW_TRANSITIONS)
            )


class RunState(c_statemachine.State):
    def __init__(self):
        super().__init__()
        self._target_position = pygame.Vector2(0, 0)
        # Increase speed relative to walking (e.g., 2x the max velocity)
        self._run_speed = MAX_VELOCITY * 2

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def enter(self):
        # Set a running animation chosen from the RUN array.
        self._statemachine.entity._c_animation.set_animation(random.choice(RUN))
        # Generate a target position using similar logic to WalkState.
        self._target_position = self._statemachine.entity["target_location"]
        # print(f"[RunState] Entered: target_position set to {self._target_position}")

    def update(self):
        # print(
        #     f"[RunState] Updating: Current position {self._statemachine.entity.position.xy}, Target: {self._target_position}"
        # )

        t_distance = self._statemachine.entity.position.distance_to(
            self._target_position
        )

        # Check if the entity is close enough to the target.
        if t_distance < 10:
            # go back to idle
            self._statemachine.entity._c_statemachine.queue_state_change(
                random.choice(RUN_TRANSITIONS)
            )
            return

        # Calculate the normalized direction vector and scale it to run speed.
        direction = self._target_position - self._statemachine.entity.position
        direction = direction.normalize() * self._run_speed
        self._statemachine.entity.velocity.xy = direction


class SitState(c_statemachine.State):
    def __init__(self):
        super().__init__()
        self._wait_time = 0
        self._counter = 0

    def enter(self):
        # Set one of the sitting animations.
        self._statemachine.entity._c_animation.set_animation(random.choice(SIT))
        # Define a sitting duration between 2 and 5 seconds.
        self._wait_time = random.random() * 3 + 2
        self._counter = 0
        self._statemachine.entity.velocity.x = 0
        # print(f"[SitState] Entered: waiting for {self._wait_time:.2f} seconds.")

    def update(self):
        # print(f"[SitState] Updating: Counter {self._counter:.2f}/{self._wait_time:.2f}")
        self._counter += constants.DELTA_TIME
        # Once the sitting duration is over, transition via the designated transition state.
        if self._counter > self._wait_time:
            self._statemachine.entity._c_statemachine.queue_state_change(
                random.choice(SIT_TO_IDLE_TRANSITION_TRANSITIONS)
            )


class BowSitState(c_statemachine.State):
    def __init__(self):
        super().__init__()
        self._wait_time = 0
        self._counter = 0

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def enter(self):
        # Choose a bow-sit animation (using BOWSIT here; alternatively, BOWSITIDK could be used).
        self._statemachine.entity._c_animation.set_animation(random.choice(BOWSIT))
        # Hold the bow-sit for a random duration (e.g., 2 to 5 seconds).
        self._wait_time = random.random() * 3 + 2
        self._counter = 0
        self._statemachine.entity.velocity.x = 0
        # print(f"[BowSitState] Entered: waiting for {self._wait_time:.2f} seconds.")

    def update(self):
        # print(
        #     f"[BowSitState] Updating: Counter {self._counter:.2f}/{self._wait_time:.2f}"
        # )
        self._counter += constants.DELTA_TIME
        if self._counter > self._wait_time:
            # Transition back to idle after bow-sitting.
            self._statemachine.entity._c_statemachine.queue_state_change(
                random.choice(SIT_TO_IDLE_TRANSITION_TRANSITIONS)
            )


class SleepState(c_statemachine.State):
    def __init__(self):
        super().__init__()
        self._sleep_time = 0
        self._counter = 0

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def enter(self):
        # Use the "DREAM" animation array to simulate sleep.
        self._statemachine.entity._c_animation.set_animation(random.choice(DREAM))
        # Define a sleep duration between 5 and 10 seconds.
        self._sleep_time = random.random() * 5 + 5
        self._counter = 0
        self._statemachine.entity.velocity.x = 0
        # print(f"[SleepState] Entered: sleeping for {self._sleep_time:.2f} seconds.")

    def update(self):
        # print(
        #     f"[SleepState] Updating: Counter {self._counter:.2f}/{self._sleep_time:.2f}"
        # )
        self._counter += constants.DELTA_TIME
        if self._counter > self._sleep_time:
            # Transition to the sleep-to-idle transition state.
            self._statemachine.entity._c_statemachine.queue_state_change(
                random.choice(SLEEP_TRANSITIONS)
            )


class DigDirtState(c_statemachine.State):
    def __init__(self):
        super().__init__()

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def enter(self):
        # Assume an animation named "Dig_Dirt" exists for the digging action.
        self._statemachine.entity._c_animation.set_animation("Dig_Dirt")
        self._statemachine.entity.velocity.x = 0
        # print("[DigDirtState] Entered: starting to dig dirt.")

    def update(self):
        # print("[DigDirtState] Updating: checking if dig animation is finished.")
        # Wait until the digging animation is flagged as finished.
        if self._statemachine.entity._c_animation.finished:
            # Transition to the dig-to-poop state.
            self._statemachine.entity._c_statemachine.queue_state_change(
                random.choice(DIG_DIRT_TRANSITIONS)
            )


class PoopState(c_statemachine.State):
    def __init__(self):
        super().__init__()
        self._wait_time = 0
        self._counter = 0

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def enter(self):
        # Set an animation for pooping; we assume a "Poop" animation exists.
        self._statemachine.entity._c_animation.set_animation("Poop")
        # Set a short duration for the pooping action (1 to 3 seconds).
        self._wait_time = random.random() * 2 + 1
        self._counter = 0
        self._statemachine.entity.velocity.x = 0
        # print(f"[PoopState] Entered: pooping for {self._wait_time:.2f} seconds.")

    def update(self):
        # print(
        #     f"[PoopState] Updating: Counter {self._counter:.2f}/{self._wait_time:.2f}"
        # )
        self._counter += constants.DELTA_TIME
        if self._counter > self._wait_time:
            # Transition back to idle after the pooping action.
            self._statemachine.entity._c_statemachine.queue_state_change(
                random.choice(POOP_TRANSITIONS)
            )


class SleepToIdleTransitionState(c_statemachine.State):
    def __init__(self):
        super().__init__()
        # Define a brief transition period (e.g., 0.5 seconds)
        self._transition_time = 0.5
        self._counter = 0

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def enter(self):
        self._counter = 0
        self._statemachine.entity.velocity.x = 0
        # print(
        # "[SleepToIdleTransitionState] Entered: preparing to transition from sleep to idle."
        # )

    def update(self):
        # print(
        #     f"[SleepToIdleTransitionState] Updating: Counter {self._counter:.2f}/{self._transition_time:.2f}"
        # )
        self._counter += constants.DELTA_TIME
        if self._counter > self._transition_time:
            # After the brief delay, move to the idle state.
            self._statemachine.entity._c_statemachine.queue_state_change(
                random.choice(SLEEP_TO_IDLE_TRANSITION_TRANSITIONS)
            )


class SitToIdleTransitionState(c_statemachine.State):
    def __init__(self):
        super().__init__()
        self._transition_time = 0.5  # short pause before idle
        self._counter = 0

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def enter(self):
        self._counter = 0
        self._statemachine.entity.velocity.x = 0
        # print("[SitToIdleTransitionState] Entered: transitioning from sit to idle.")

    def update(self):
        # print(
        #     f"[SitToIdleTransitionState] Updating: Counter {self._counter:.2f}/{self._transition_time:.2f}"
        # )
        self._counter += constants.DELTA_TIME
        if self._counter > self._transition_time:
            self._statemachine.entity._c_statemachine.queue_state_change(
                random.choice(SIT_TO_IDLE_TRANSITION_TRANSITIONS)
            )


class IdleToSitTransitionState(c_statemachine.State):
    def __init__(self):
        super().__init__()
        self._transition_time = 0.5  # brief transition period
        self._counter = 0

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def enter(self):
        self._counter = 0
        self._statemachine.entity.velocity.x = 0
        # print("[IdleToSitTransitionState] Entered: preparing to sit from idle.")

    def update(self):
        # print(
        #     f"[IdleToSitTransitionState] Updating: Counter {self._counter:.2f}/{self._transition_time:.2f}"
        # )
        self._counter += constants.DELTA_TIME
        if self._counter > self._transition_time:
            # Transition into the SitState.
            self._statemachine.entity._c_statemachine.queue_state_change(
                random.choice(IDLE_TO_SIT_TRANSITION_TRANSITIONS)
            )


class DigToPoopTransitionState(c_statemachine.State):
    def __init__(self):
        super().__init__()
        self._transition_time = 0.5  # short delay before pooping
        self._counter = 0

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def enter(self):
        self._counter = 0
        self._statemachine.entity.velocity.x = 0
        # print(
        #     "[DigToPoopTransitionState] Entered: transitioning from digging to pooping."
        # )

    def update(self):
        # print(
        #     f"[DigToPoopTransitionState] Updating: Counter {self._counter:.2f}/{self._transition_time:.2f}"
        # )
        self._counter += constants.DELTA_TIME
        if self._counter > self._transition_time:
            self._statemachine.entity._c_statemachine.queue_state_change(
                random.choice(DIG_TO_POOP_TRANSITION_TRANSITIONS)
            )


class AggressState(c_statemachine.State):
    def __init__(self):
        super().__init__()
        self._aggress_time = 0
        self._counter = 0

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def enter(self):
        # Choose an aggressive animation from the AGRESS array.
        self._statemachine.entity._c_animation.set_animation(random.choice(AGRESS))
        # Define an aggressive period between 1 and 4 seconds.
        self._aggress_time = random.random() * 3 + 1
        self._counter = 0
        # print(
        #     f"[AggressState] Entered: aggressive behavior for {self._aggress_time:.2f} seconds."
        # )

    def update(self):
        # print(
        #     f"[AggressState] Updating: Counter {self._counter:.2f}/{self._aggress_time:.2f}"
        # )
        self._counter += constants.DELTA_TIME
        # print("counter:", self._counter)
        if self._counter > self._aggress_time:
            # print("transitioning")
            # Once the aggressive period ends, transition back to idle.
            self._statemachine.queue_state_change(IDLE_STATE)


# ============================================================ #
# Assistant Class
# ============================================================ #


def _c_anim_update(self):
    self._registry.update()

    sprite = self._registry.get_current_frame()._qpixmap.copy()

    if self._x_flip:
        sprite = sprite.transformed(QTransform().scale(-1, 1))
    if self._y_flip:
        sprite = sprite.transformed(QTransform().scale(1, -1))

    # render current frame
    self.entity._fb_painter.drawPixmap(0, 0, sprite)


class Assistant(transparentwindow.HiddenWindowWrapper):

    def __init__(self, name: str = "stella.ai"):
        super().__init__(
            name,
            pygame.Rect(0, 0, WINDOW_AREA[0], WINDOW_AREA[1]),
        )

        # load animation
        spritesheet, animations = graphics.load_animations(
            os.path.join("assets", "catanimation.json")
        )

        # -------------------------------------------------------- #
        # components
        # -------------------------------------------------------- #

        self._c_animation = self.add_component(
            c_animation.AnimationComponent(animations["Idle_1"])
        )
        self._c_statemachine = self.add_component(
            c_statemachine.StateMachineComponent()
        )

        # configure components
        # scale all of animation frame sizes to 100x100
        for animation in animations.values():
            for sprite in animation._sprite_frames:
                sprite._qpixmap = sprite._qpixmap.scaled(100, 100)

        # inject new code
        self._c_animation.update = types.MethodType(_c_anim_update, self._c_animation)

        self["holding_time"] = 0
        self["holding_frame"] = None
        self._c_statemachine.entity["target_location"] = pygame.Vector2(0)

        # create states
        self._c_statemachine.add_state(IDLE_STATE, IdleState())
        self._c_statemachine.add_state(WALK_STATE, WalkState())
        self._c_statemachine.add_state(RESTING_STATE, RestingState())
        self._c_statemachine.add_state(LOOK_AROUND_STATE, LookAroundState())
        self._c_statemachine.add_state(HOLD_STATE, HoldFrameState())
        self._c_statemachine.add_state(RUN_STATE, RunState())
        self._c_statemachine.add_state(SIT_STATE, SitState())
        self._c_statemachine.add_state(LICK_PAW_STATE, LickPawState())
        self._c_statemachine.add_state(BOW_SIT_STATE, BowSitState())
        self._c_statemachine.add_state(SLEEP_STATE, SleepState())
        self._c_statemachine.add_state(DIG_DIRT_STATE, DigDirtState())
        self._c_statemachine.add_state(POOP_STATE, PoopState())
        self._c_statemachine.add_state(
            SLEEP_TO_IDLE_TRANSITION_STATE, SleepToIdleTransitionState()
        )
        self._c_statemachine.add_state(
            SIT_TO_IDLE_TRANSITION_STATE, SitToIdleTransitionState()
        )
        self._c_statemachine.add_state(
            IDLE_TO_SIT_TRANSITION_STATE, IdleToSitTransitionState()
        )
        self._c_statemachine.add_state(
            DIG_TO_POOP_TRANSITION_STATE, DigToPoopTransitionState()
        )
        self._c_statemachine.add_state(AGGRESS_STATE, AggressState())

        # -------------------------------------------------------- #
        # events handler
        # --------------------------------------------------------- #

        self._state_changed_event = constants.SIGNAL_HANDLER.get_signal(
            "voice_activated"
        )

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def widget_update(self):
        self._c_animation.xflipped = self.velocity.x < 0
        super().widget_update()

        # update entity location with app location (because shared location)
        touching = self._world.move_entity(self)
        # print(self.position, self.velocity, self._c_statemachine._current_state)

        # print("assistant update", *map(int, self.position))
        # abuse app location to move the window
        self._window_rect.topleft = self.position.xy
        self._fb_rect.setWidth(self._window_rect.width)
        self._fb_rect.setHeight(self._window_rect.height)

    # -------------------------------------------------------- #
    # pyqt logic
    # -------------------------------------------------------- #

    def mousePressEvent(self, event):
        if event.button() == qtc.Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == qtc.Qt.LeftButton:
            new_pos = event.globalPos() - self.drag_position
            self.position.xy = (new_pos.x(), new_pos.y())
            self.move(new_pos)
            event.accept()
