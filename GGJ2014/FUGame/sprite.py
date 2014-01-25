import pygame
import os
from datetime import datetime

from FUGame.constants import *
from FUGame.utils import utils


class Sprite(object):

    """Sprite class"""

    def __init__(self, filename, x, y, z, col_x_offset=None, col_y_offset=None,
                 fps=FU_FRAME_RATE):
        # self.image = utils.convert_white_to_transparent(
        #     pygame.image.load(
        #         "assets/sprites/{}/{}.png".format(filename, filename)
        #     )
        # )
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

        self.mask = pygame.mask.from_surface(self.current_frame)

        if all([col_y_offset is not None, col_x_offset is not None]):
            self.col_x_offset = col_x_offset
            self.col_y_offset = col_y_offset
            self.col_image = pygame.image.load(os.path.join(
                FU_APATH, "collision", filename + ".png")
            )

    @property
    def col_pos(self):
        """Position of the collision box of the sprite"""
        return self._x + self.col_x_offset, self._y + self.col_y_offset

    @property
    def pos(self):
        """Get position of Sprite"""
        return self._x, self._y

    def set_pos(self, x, y):
        """Set position of Sprite"""
        self._x = x
        self._y = y

    @property
    def z_index(self):
        return self._y + self.current_frame.get_height() + self._z

    def update_dt(self):
        self.dt = datetime.now() - self.lastdt

    def next_frame(self):
        self.lastdt = datetime.now()
        self.current_frame_num = (
            self.current_frame_num + 1) % len(self.anims[self.current_anim]
                                              )
        self.current_frame = self.anims[
            self.current_anim][self.current_frame_num]

    def load_frames(self):
        path = os.path.join("assets", "sprites", self.name)
        l = os.listdir(path)
        d = {
            folder_name: [pygame.image.load(
                os.path.join(path, folder_name, image)
            ) for image in os.listdir(
                os.path.join(path, folder_name))] for folder_name in l
        }
        # print(d)
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
