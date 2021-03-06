import pygame
import os
from pygame.locals import *

from FUGame.character import Character, Sprite
from FUGame.world import World
from FUGame.constants import *
from FUGame.utils import utils
from FUGame.swagwords import SwagWord
from FUGame.levels.level import Level, BaseEventHandlerMixin
from datetime import datetime

from random import randint, choice


NUM_SWAG_WORDS = 30


class EventHandlerMixin(BaseEventHandlerMixin):

    def _use(self):
        if self.dead:
            self.credits.speed += 5
        self.world.NPCs["guy"].set_anim(
            "{}S".format(self.world.NPCs["guy"].direction))
        self.world.NPCs["guy"].set_anim(
            "{}S".format(self.world.NPCs["guy"].direction))
        for s in self.world.static.values():
            if s.use_func and s.sprite_rect.colliderect(self.world.NPCs["guy"].sprite_rect):
                s.use_func()
                break
            elif s.name == "bigShroom" and s.sprite_rect.colliderect(self.world.NPCs["guy"].sprite_rect):
                s.is_animating = True
                break
        for n, w in enumerate(self._swag_words[:]):
            if w.rect.colliderect(self.guy.sprite_rect):
                self._swag_words.remove(w)

    @property
    def event_map(self):
        _event_map = dict(self._move_event_map)
        _event_map[K_SPACE] = [self._use, ()]
        return _event_map


class SwagWord(object):

    def __init__(self, word):
        self._Y_BOUNDS = (200, 530)
        self._X_BOUNDS = (50, 500)
        self.word = word
        self.gen_new_rect()
        self.font = pygame.font.SysFont("comicsansms", 24)
        self.fc = 0
        self.freq = randint(3, 10)
        self.punch0 = pygame.mixer.Sound(
            os.path.join(FU_APATH, "soundFX", "punch_00.wav"))
        self.punch0.set_volume(0.15)
        self.punch1 = pygame.mixer.Sound(
            os.path.join(FU_APATH, "soundFX", "punch_01.wav"))
        self.punch1.set_volume(0.15)

    def gen_new_rect(self):
        self.rect = pygame.Rect(
            randint(*self._X_BOUNDS), randint(*self._Y_BOUNDS),
            150, 50)

    def draw(self, screen):
        self.fc = (self.fc + 1) % self.freq
        if self.fc < self.freq / 2:
            utils.drawText(
                screen,
                self.word,
                tuple([randint(0, 255) for i in xrange(3)]),
                self.rect,
                self.font,
                aa=True
            )


class Hills(Level, EventHandlerMixin):

    def __init__(self, state=0):
        self.world = self.create_world()
        self.guy = self.world.NPCs["guy"]
        self.allow_move = True
        self.start_time = datetime.now()
        self.game_time = datetime.now() - self.start_time
        self.dead = False
        self.cmd = "Press 'SPACE' to Speed Up"
        self.display_cmd = False
        self.cmd_font = pygame.font.SysFont("verdana", 48)
        self.credits = self.Credits()
        self.punch0 = pygame.mixer.Sound(
            os.path.join(FU_APATH, "soundFX", "punch_00.wav"))
        self.punch0.set_volume(0.15)
        self.punch1 = pygame.mixer.Sound(
            os.path.join(FU_APATH, "soundFX", "punch_01.wav"))
        self.punch1.set_volume(0.15)
        pygame.mixer.music.load(
            os.path.join(FU_APATH, "music", "manicfrolic.ogg"))
        pygame.mixer.music.set_volume(0.75)
        pygame.mixer.music.play(999)
        self.crash = pygame.mixer.Sound(
            os.path.join(FU_APATH, "soundFX", "crash.wav"))

        self._swag_word_list = FU_SWAG_WORDS[:]

        self._swag_words = [SwagWord(choice(self._swag_word_list))
                            for i in xrange(NUM_SWAG_WORDS)]

    def create_world(self):
        chars = {
            "guy": Character(
                filename="main",
                x=120,
                y=260,
                z=1,
                col_pts=[],
                col_x_offset=50,
                col_y_offset=117,
                fps=10,
                speed=7
            ),
        }
        statics = {
            "arrowKeys": Sprite(
                filename="arrowKeys",
                x=827,
                y=600,
                z=50,
                col_pts=[],
            ),
            "spaceBar": Sprite(
                filename="spaceBar",
                x=373,
                y=712,
                z=50,
                col_pts=[],
            ),
            "smallShroom": Sprite(
                filename="smallShroom",
                x=277,
                y=510,
                z=0,
                col_pts=[
                    (12, 56), (31, 64), (54, 67), (77, 68), (95, 65),
                    (115, 60), (127, 54), (128, 43), (17, 42),
                    (64, 68), (64, 82), (65, 95), (79, 96), (76, 79), (74, 66)
                ],
                col_x_offset=None,
                col_y_offset=None
            ),
            "bigShroom": Sprite(
                filename="bigShroom",
                x=325,
                y=458,
                z=100,
                col_pts=[
                    (31, 95), (59, 107), (107, 115), (160, 117),
                    (202, 109), (234, 97), (264, 79), (271, 73),
                    (258, 45), (217, 49), (172, 50), (120, 53),
                    (97, 51), (72, 48), (64, 44), (48, 63)
                ],
                col_x_offset=None,
                col_y_offset=None,
                fps=15
            ),
            "hellGate": Sprite(
                filename="hellGate",
                x=60,
                y=115,
                z=-100,
                col_pts=[(
                    50, 234), (
                    73, 230), (
                    87, 225), (
                    120, 217), (
                    152, 201), (
                    176, 190), (203, 171), (200, 158),
                    (190, 133), (42, 175)
                ],
                col_x_offset=None,
                col_y_offset=None,
                fps=10
            ),
            "sunFace": Sprite(
                filename="sunFace",
                x=355,
                y=68,
                z=-2500,
                col_pts=[],
                col_x_offset=None,
                col_y_offset=None,
                fps=10
            ),
            "unicornMan": Sprite(
                filename="unicornMan",
                x=500,
                y=200,
                z=0,
                col_pts=[],
                col_x_offset=None,
                col_y_offset=None,
                fps=100
            ),
            "mountain": Sprite(
                filename="mountain",
                x=0,
                y=0,
                z=-1000,
                col_pts=[],
                col_x_offset=None,
                col_y_offset=None,
            ),
            "rainbowFoam": Sprite(
                filename="rainbowFoam",
                x=0,
                y=0,
                z=0,
                col_pts=[],
                col_x_offset=None,
                col_y_offset=None,
                fps=5
            ),
            "shine": Sprite(
                filename="shine",
                x=0,
                y=0,
                z=0,
                col_pts=[],
                col_x_offset=None,
                col_y_offset=None,
                fps=5
            ),
            "flowers": Sprite(
                filename="flowers",
                x=0,
                y=0,
                z=-300,
                col_pts=[],
                col_x_offset=None,
                col_y_offset=None,
                fps=8
            )
        }
        world = World(
            level_id="hills",
            bg_filename="happyHills_bg",
            static=statics,
            NPCs=chars,
            col_pts=[(
                65, 420), (
                107, 406), (
                127, 367), (
                159, 336), (
                187, 306), (224, 288), (253, 271), (281, 254),
                (310, 244), (386, 214), (437, 201), (472, 200), (539,
                                                                 184), (
                    619, 188), (
                    621, 231), (
                    617, 257),
                (626, 292), (626, 332), (626, 356), (626, 404), (626,
                                                                 429), (
                    626, 461), (
                    626, 501), (
                    626, 557),
                (626, 578), (626, 600), (626, 622), (626, 629), (626,
                                                                 637), (
                    340, 606), (
                    340, 580), (
                    359, 580),
                (357, 606), (451, 607), (457, 575), (456, 595), (483,
                                                                 576), (
                    486, 584), (
                    491, 603), (
                    468, 618),
                (459, 573), (482, 572), (469, 552)],
            x=0,
            y=0
        )

        world.NPCs["guy"].set_anim("F")
        world.static["hellGate"].is_animating = True
        world.static["smallShroom"].is_animating = True
        world.static["unicornMan"].is_animating = True
        world.static["sunFace"].is_animating = True
        world.static["rainbowFoam"].is_animating = True
        world.static["shine"].is_animating = True
        world.static["flowers"].is_animating = True
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

        # If player wants to exit back to office
        if any(
            map(
                self.guy.col_rect.collidepoint,
                [(200, 326), (160, 344), (190, 328), (223, 319)]
            )
        ):
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            raise utils.NextLevelException(
                "office",
                1 if len(self._swag_words) < NUM_SWAG_WORDS else 0)
                # ^ If got any swag words, go to "middle-ground" office

        if self.game_time.total_seconds() >= 30:  # TODO make 30 dev: 5
            if not self.dead:
                self.crash.play()
                pygame.mixer.music.set_volume(.3)
                self.dead = True
                pass
            else:
                self.cmd = "Tap 'SPACE' to Speed Up"
                self.display_cmd = True
                self.credits.update_dt()
                if self.credits.dt.microseconds > 1.0 / self.credits.fps * 1000000:
                    self.credits.update_credits()
                if self.credits.end:
                    pygame.mixer.music.stop()
                    pygame.mixer.stop()
                    raise utils.NextLevelException("instructions", 0)

        if self.world.static["flowers"].current_frame_num == 3 or self.world.static["flowers"].current_frame_num == 9:
            self.punch0.play()

        if self.world.static["flowers"].current_frame_num == 7:
            self.punch1.play()

        # Blitting
        self._blit(screen)

    def _test_key_pressable_prompts(self, s):
        keyc = {
            "arrowKeys": True,
            "spaceBar": any([
                self.world.static["bigShroom"].sprite_rect.colliderect(
                    self.guy.sprite_rect),
                any(
                    w.rect.colliderect(self.guy.sprite_rect) for w in self._swag_words
                ),
            ])
        }
        condition = keyc[s.name]
        if condition:
            s.set_anim("I")
        else:
            s.set_anim("X")

    def _blit(self, screen):
        if not self.dead:
            screen.blit(self.world.bg, self.world.pos)
            for s in self.world.sprites:
                if s.name in ["arrowKeys", "spaceBar"]:
                    self._test_key_pressable_prompts(s)
                screen.blit(s.current_frame, s.pos)
            for w in self._swag_words:
                w.draw(screen)
        else:
            screen.fill((0, 0, 0))
            screen.blit(self.credits.rect, (0, 0))
            [screen.blit(self.credits.texts[i], self.credits.texts_pos[i])
             for i in xrange(len(self.credits.texts))]

        if self.display_cmd:
            screen.blit(
                self.cmd_font.render(self.cmd, True, FU_CMD_COLOR), FU_CMD_POS)
