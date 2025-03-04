import os
import json
from PIL import Image

from source.components import c_sprite

from source import constants


# ============================================================ #
# Animation Class
# ============================================================ #


class Animation:
    CACHE = {}

    @classmethod
    def add_animation(cls, name, animation):
        cls.CACHE[name] = animation

    @classmethod
    def get_animation(cls, name):
        return cls.CACHE.get(name)

    # -------------------------------------------------------- #

    def __init__(self, frames: list):
        self._sprite_frames = [
            c_sprite.SpriteComponent(frame[0], metadata={"duration": frame[1]})
            for frame in frames
        ]
        self._frame_count = len(frames)

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def get_registry(self):
        return AnimationRegistry(self)


# ============================================================ #
# Animation Registry
# ============================================================ #


class AnimationRegistry:
    def __init__(self, parent):
        self._parent = parent
        self._current_animation = None
        self._frame = 0
        self._timer = 0
        self._finished = False
        self._hold_frame = False

    # -------------------------------------------------------- #
    # logic
    # -------------------------------------------------------- #

    def update(self):
        if self._hold_frame:
            return
        self._timer += constants.DELTA_TIME
        self._finished = (
            self._timer > self._parent._sprite_frames[self._frame]._metadata["duration"]
        )
        if self._finished:
            self._timer = 0
            self._frame += 1
            self._frame %= self._parent._frame_count

    def get_current_frame(self):
        return self._parent._sprite_frames[self._frame]

    def set_animation(self, name: str):
        self._current_animation = name
        self.reset()

    def reset(self):
        self._frame = 0
        self._timer = 0
        self._finished = False

    def set_hold_frame(self, hold: bool):
        self._hold_frame = hold


# ============================================================ #
# Animation Loader
# ============================================================ #


def load_animations(json_path: str):
    """
    Load animations from an Aseprite-exported JSON file.

    This function:
      • Parses the JSON file specified by json_path.
      • Loads the spritesheet image (the filename is expected to be in the JSON meta data under "image").
      • Iterates over each frame definition to extract sub-images from the spritesheet.
      • Checks for a 'rotated' flag (if true, the frame is rotated by -90 degrees).
      • Processes the "frameTags" in the meta section to group frames (using the inclusive indices 'from' and 'to')
        into a dictionary of animations.

    Args:
        json_path (str): Path to the JSON file exported from Aseprite.

    Returns:
        tuple: A tuple containing:
          - spritesheet (PIL.Image.Image): The loaded spritesheet image.
          - animations (dict): A dictionary mapping each tag (animation name) to a list of PIL.Image.Image objects
            representing the individual frames of that animation.
    """
    # Open and parse the JSON file
    with open(json_path, "r") as f:
        data = json.load(f)

    # Retrieve the meta data; the spritesheet image filename should be provided here.
    meta = data.get("meta", {})
    spritesheet_filename = meta.get("image")
    if not spritesheet_filename:
        raise ValueError(
            "The JSON meta data does not specify an 'image' key for the spritesheet."
        )

    # Construct the full path to the spritesheet image.
    json_dir = os.path.dirname(json_path)
    spritesheet_path = os.path.join(json_dir, spritesheet_filename)

    # Load the spritesheet as a PIL.Image object.
    spritesheet = Image.open(spritesheet_path).convert("RGBA")

    # Process the frames.
    # The JSON file is expected to have a "frames" key which is a list of frame definitions.
    frames_data = data.get("frames", [])
    frames = []
    for frame_info in frames_data:
        # Each frame has a "frame" dictionary with x, y, w, h values.
        frame_rect = frame_info.get("frame", {})
        x = frame_rect.get("x", 0)
        y = frame_rect.get("y", 0)
        w = frame_rect.get("w", 0)
        h = frame_rect.get("h", 0)

        # Extract the sprite frame from the spritesheet using crop.
        frame_surface = spritesheet.crop((x, y, x + w, y + h))

        # If the frame is marked as rotated (typically a 90° rotation by Aseprite),
        # rotate the image back by -90°.
        if frame_info.get("rotated", False):
            frame_surface = frame_surface.rotate(-90, expand=True)

        packet = [frame_surface, frame_info.get("duration", 100) / 1000]
        frames.append(packet)

    # Process the frameTags to group frames into animations.
    # Each tag has a "name", "from", and "to" field.
    animations = {}
    frame_tags = meta.get("frameTags", [])
    for tag in frame_tags:
        tag_name = tag.get("name")
        start_index = tag.get("from", 0)
        end_index = tag.get("to", 0)
        # The 'from' and 'to' indices are inclusive.
        animations[tag_name] = Animation(frames[start_index : end_index + 1])

        # cache animation
        Animation.add_animation(tag_name, animations[tag_name])

    return spritesheet, animations
