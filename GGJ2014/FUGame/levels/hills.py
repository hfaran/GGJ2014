import pygame
import os
from pygame.locals import *

from FUGame.character import Character, Sprite
from FUGame.world import World
from FUGame.constants import *
from FUGame.utils import utils
from FUGame.levels.level import Level, BaseEventHandlerMixin
from datetime import datetime

from random import randint


class EventHandlerMixin(BaseEventHandlerMixin):
    def _use(self):
        if self.dead:
            self.credits.speed += 5

    @property
    def event_map(self):
        _event_map = dict(self._move_event_map)
        _event_map[K_SPACE] = [self._use, ()]
        return _event_map


class Hills(Level, EventHandlerMixin):
    def __init__(self, state=0):
        self.world = self.create_world()
        self.allow_move = True
        self.start_time = datetime.now()
        self.game_time = datetime.now() - self.start_time
        self.dead = False
        self.cmd = "Press 'SPACE' to Speed Up"
        self.display_cmd = False
        self.cmd_font = pygame.font.SysFont("verdana", 48)
        self.credits = self.Credits()
        pygame.mixer.music.load(os.path.join(FU_APATH, "music", "manicfrolic.wav"))
        pygame.mixer.music.set_volume(0.75)
        pygame.mixer.music.play(999)

    def create_world(self):
        chars = {
            "guy": Character(
                filename="main",
                x=120,
                y=260,
                z=0,
                col_pts=[],
                col_x_offset=50,
                col_y_offset=117,
                fps=10,
                speed=7
            ),
        }
        statics = {

        }
        world = World(
            level_id="hills",
            bg_filename="hills_bg",
            static=statics,
            NPCs=chars,
            col_pts=[(65, 420), (107, 406), (127, 367), (159, 336), (187, 306), (224, 288), (253, 271), (281, 254),
                     (310, 244), (386, 214), (437, 201), (472, 200), (539, 184), (619, 188), (621, 231), (617, 257),
                     (626, 292), (626, 332), (626, 356), (626, 404), (626, 429), (626, 461), (626, 501), (626, 557),
                     (626, 578), (626, 600), (626, 622), (626, 629), (626, 637)],
            x=0,
            y=0
        )

        world.NPCs["guy"].set_anim("F")
        return world

    def handle_events(self, event):
        keys = pygame.key.get_pressed()
        for key, l in self.event_map.iteritems():
            func, args = l
            if keys[key]:
                return bool(func(*args))
        else:
            self.world.NPCs["guy"].is_moving = False
            return False

    def update_loop(self, screen, game_clock):
        self._animate_sprites()
        self._move_npcs(game_clock)
        self.game_time = datetime.now() - self .start_time

        if self.game_time.total_seconds() >= 5:  # TODO make 30 dev: 5
            if not self.dead:
            # TODO play car cash
                self.dead = True
                pass
            else:
                self.cmd = "Press 'SPACE' to Speed Up"
                self.display_cmd = True
                self.credits.update_dt()
                if self.credits.dt.microseconds > 1.0 / self.credits.fps * 1000000:
                    self.credits.update_credits()
                if self.credits.end:
                    pygame.mixer.stop()
                    raise utils.NextLevelException("room", 0)


        # Blitting
        self._blit(screen)

    def _blit(self, screen):
        if not self.dead:
            screen.blit(self.world.bg, self.world.pos)
            for s in self.world.sprites:
                screen.blit(s.current_frame, s.pos)
        else:
            screen.fill((0, 0, 0))
            screen.blit(self.credits.rect, (0, 0))
            [screen.blit(self.credits.texts[i], self.credits.texts_pos[i]) for i in xrange(len(self.credits.texts))]


        if self.display_cmd:
            screen.blit(
                self.cmd_font.render(self.cmd, True, FU_CMD_COLOR), FU_CMD_POS)


