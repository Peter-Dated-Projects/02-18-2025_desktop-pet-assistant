import math

import os
import PyQt5.QtGui as qtg

from source import constants
from source import physics
from source import graphics

from source.components import c_animation


# ============================================================ #
# Assistant Class
# ============================================================ #

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


JUMP = ["J_1", "J_2", "J_3"]
JUMPUPDOWN = ["J_U_D"]

BOWSIT = ["Bow_Sit"]
BOWSITIDK = ["B_S_1", "B_S_2"]

BOWIDLE = ["Bow_Idle"]
BOWIDLEIDK = ["B_I_1", "B_I_2"]


class Assistant(physics.entity.Entity):

    def __init__(self):
        super().__init__(0, 0, constants.WINDOW_SIZE[0], constants.WINDOW_SIZE[1])

        # load animation
        spritesheet, animations = graphics.load_animations(
            os.path.join("assets", "catanimation.json")
        )
        # constants.RUNNING = False
        print(spritesheet, animations)

        # -------------------------------------------------------- #
        # components

        self._c_animation = self.add_component(
            c_animation.AnimationComponent(animations["Idle_1"])
        )

        # -------------------------------------------------------- #
        # configure components

        # scale all of animation frame sizes to 100x100
        for animation in animations.values():
            for sprite in animation._sprite_frames:
                sprite._qpixmap = sprite._qpixmap.scaled(100, 100)

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def update(self):
        temp = self.position.xy
        self.position.xy = (0, 0)
        super().update()
        self.position.xy = temp

        self.velocity.x = 20 if math.sin(constants.RUNTIME) > 0 else -20

        # update entity location with app location (because shared location)
        self.position.xy = constants.WINDOW_CONTEXT._rect.topleft
        self.rect.topleft = self.position.xy
        touching = self._world.move_entity(self)

        print("assistant update", *map(int, self.position))
        # abuse app location to move the window
        constants.WINDOW_CONTEXT._rect.topleft = self.position.xy
