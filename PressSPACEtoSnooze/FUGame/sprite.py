import pygame
import os
from datetime import datetime

from FUGame.constants import *
from FUGame.utils import utils


class Sprite(object):

    """Sprite class"""

    def __init__(self, filename, x, y, z, col_pts, col_x_offset=None,
                 col_y_offset=None, fps=FU_FRAME_RATE, use_func=None):
        self.name = filename

        self._x = x
        self._y = y
        self._z = z

        self._v_x = 0
        self._v_y = 0

        self.fps = fps
        self.lastdt = datetime.now()
        self.update_dt()

        self.anims = self.load_frames()
        self.current_anim = list(self.anims.iteritems())[0][0]
        self.current_frame_num = 0
        self.current_frame = self.anims[
            self.current_anim][self.current_frame_num]
        self.is_moving = False
        self.is_animating = False

        self.mask = pygame.mask.from_surface(self.current_frame)

        self.col_pts = col_pts
        self.col_image = None

        if all([col_y_offset is not None, col_x_offset is not None]):
            self.col_x_offset = col_x_offset
            self.col_y_offset = col_y_offset
            self.col_image = pygame.image.load(os.path.join(
                FU_APATH, "collision", filename + ".png")
            )

        self.use_func = use_func

    @property
    def col_rect(self):
        """:returns: Rect used for Sprite collision"""
        if self.col_image:
            _col_rect = self.col_image.get_rect()
            _col_rect.x, _col_rect.y = self.col_pos
            return _col_rect
        return None

    @property
    def sprite_rect(self):
        """:returns: Rect of full Sprite"""
        _sprite_rect = self.current_frame.get_rect()
        _sprite_rect.x, _sprite_rect.y = self.pos
        return _sprite_rect

    @property
    def col_pos(self):
        """Position of the collision box of the sprite"""
        return self._x + self.col_x_offset, self._y + self.col_y_offset

    def set_anim(self, anim):
        """Sets the animation state of Sprite to the start of `anim`

        :param anim: Name of animation
        :type  anim: str
        """
        self.current_anim = anim
        self.current_frame_num = 0
        self.current_frame = self.anims[
            self.current_anim][self.current_frame_num]

    @property
    def pos(self):
        """Get position of Sprite"""
        return self._x, self._y

    def set_pos(self, x, y):
        """Set position of Sprite"""
        self._x = x
        self._y = y

    def nudge(self, x, y):
        """Move sprite `(x, y)` pixels to bottom-right"""
        self._x += x
        self._y += y

    def set_z(self, z):
        """Set z"""
        self._z = z

    @property
    def z_index(self):
        """:returns: z-index of Sprite"""
        return self._y + self.current_frame.get_height() + self._z

    def update_dt(self):
        """Update `dt` time variable for Sprite"""
        self.dt = datetime.now() - self.lastdt

    def next_frame(self):
        """Move Sprite's current_frame to the next frame"""
        self.lastdt = datetime.now()
        self.current_frame_num = (
            self.current_frame_num + 1) % len(self.anims[self.current_anim]
                                              )
        self.current_frame = self.anims[
            self.current_anim][self.current_frame_num]

        # return True if anim'd more than once
        if self.current_frame_num == 0:
            return True

    def load_frames(self):
        """Load frames from assets for Sprite"""
        path = os.path.join("assets", "sprites", self.name)
        l = sorted(
            [p for p in os.listdir(path) if os.path.isdir(
                os.path.join(path, p))]
        )
        d = {
            folder_name: [pygame.image.load(
                os.path.join(path, folder_name, image)
            ) for image in sorted(os.listdir(
                os.path.join(path, folder_name)))] for folder_name in l
        }
        return d

    def point_collision(self, pos):
        """Test if `pos` collides with Sprite

        :type  pos: (int, int)
        :param pos: Coordinates to test collision with Sprite at
        :rtype: bool
        :returns: bool indicating if collision occurred
        """
        try:
            return self.mask.get_at(pos)
        except IndexError:
            return False

    def set_frame(self, frame):
        """Set the frame of animation of the sprite to the given frame

        :type frame: int
        """
        self.current_frame_num = frame
        self.current_frame = self.anims[
            self.current_anim][self.current_frame_num]
