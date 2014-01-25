import pygame
from pygame.locals import *

from FUGame.character import Character, Sprite
from FUGame.world import World
from FUGame.constants import *
from random import randint
from datetime import datetime


class EventHandlerMixin:

    def _move_character(self, direction):
        self.world.NPCs["guy"].is_moving = True
        self.world.NPCs["guy"].direction = direction

    def _snooze(self):
        if self.display_cmd:
            self.display_cmd = False
            self.snooze_time = datetime.now()

    @property
    def event_map(self):
        _event_map = {
            K_LEFT: [self._move_character, ("L",)],
            K_RIGHT: [self._move_character, ("R",)],
            K_UP: [self._move_character, ("B",)],
            K_DOWN: [self._move_character, ("F",)],
            K_SPACE: [self._snooze, ()]
        }
        return _event_map


class Room(object, EventHandlerMixin):
    cloud_min_x = 200
    cloud_max_x = 300
    cloud_min_y = 0
    cloud_max_y = 150

    def __init__(self):
        self.world = self.create_world()
        self.clock_font = pygame.font.SysFont("comicsansms", 16)
        self.cmd_font = pygame.font.SysFont("arial", 48)
        self.cmd = "Press 'SPACE' to Snooze"
        self.display_cmd = False

        self.sky = Sprite(
            filename="sky",
            x=515,
            y=40,
            z=0,
            col_pts=[],
            col_x_offset=None,
            col_y_offset=None
        )

        self.clouds = [
            Sprite(
                filename="cloud"+str(i),
                x=randint(470, 800),
                y=randint(self.cloud_min_y, self.cloud_max_y),
                z=0,
                col_pts=[],
                col_x_offset=None,
                col_y_offset=None,
                fps=10
            ) for i in xrange(1, 5)
        ]

        self.snooze_time = datetime.now()
        self.start_time = datetime.now()
        self.game_time = datetime.now() - self.start_time
        self.clock_time = self.seconds_to_time(self.game_time.total_seconds())
        self.clock_text = self.clock_font.render(self.clock_time, True, (0, 255, 0))

    def seconds_to_time(self, secs):
        secs = secs + 51 + 5*60
        hours = int(secs / 60)
        mins = int(secs % 60)

        return "{}:{}".format(hours, str(mins).zfill(2))

    def create_world(self):
        # Create objects
        chars = {
            "guy": Character(
                filename="main",
                x=560,
                y=190,
                z=0,
                col_pts=[],
                col_x_offset=7,
                col_y_offset=92,
                fps=10,
                speed=5
            ),
        }
        statics = {
            "desk": Sprite(
                filename="desk",
                x=1075,
                y=210,
                z=0,
                col_pts=[(4, 61), (17, 120), (27, 171), (40, 221), (56, 294), (69, 56), (120, 293), (182, 293),
                         (131, 56)],
                col_x_offset=None,
                col_y_offset=None
            ),
            "chair": Sprite(
                filename="chair",
                x=950,
                y=330,
                z=0,
                col_pts=[(5, 80), (36, 112), (75, 120), (110, 105), (110, 70), (85, 30), (25, 55), (50, 30)],
                col_x_offset=None,
                col_y_offset=None
            ),
            "sideTable": Sprite(
                filename="sideTable",
                x=420,
                y=169,
                z=0,
                col_pts=[(20, 110), (65, 110), (115, 110), (105, 40), (20, 40), (15, 55)],
                col_x_offset=None,
                col_y_offset=None
            ),
            "alarmClock": Sprite(
                filename="alarmClock",
                x=440,
                y=180,
                z=100,
                col_pts=[],
                col_x_offset=None,
                col_y_offset=None
            ),
            "bed": Sprite(
                filename="bed",
                x=545,
                y=170,
                z=0,
                col_pts=[(30, 310), (80, 310), (130, 310), (180, 310), (230, 310), (250, 310), (5, 265), (65, 265),
                         (125, 265), (185, 265), (245, 265), (270, 265), (0, 100), (65, 100),
                         (125, 100), (185, 100), (245, 100), (270, 100), (10, 60), (235, 60)],
                col_x_offset=15,
                col_y_offset=15
            ),
            "blanket": Sprite(
                filename="blanket",
                x=535,
                y=240,
                z=0,
                col_pts=[],
                col_x_offset=None,
                col_y_offset=None
            ),
            "pillows": Sprite(
                filename="pillows",
                x=545,
                y=160,
                z=0,
                col_pts=[],
                col_x_offset=None,
                col_y_offset=None
            ),
            "door": Sprite(
                filename="door",
                x=40,
                y=60,
                z=0,
                col_pts=[(70, 325), (125, 300), (180, 275)],
                col_x_offset=None,
                col_y_offset=None
            )
        }

        world = World(
            level_id="room",
            bg_filename="room_bg",
            static=statics,
            NPCs=chars,
            col_pts=[(49, 630), (63, 555), (75, 500), (48, 464), (95, 370), (65, 305), (49, 267), (115, 280),
                     (130, 210), (195, 210), (260, 210), (325, 210), (390, 210), (455, 210), (520, 210), (585, 210),
                     (650, 210), (715, 210), (780, 210), (845, 210), (910, 210), (975, 210), (1040, 210), (1105, 210),
                     (1170, 210), (1200, 210), (1210, 265), (1220, 305), (1255, 500), (1270, 560), (1280, 630)],
            x=0,
            y=0
        )

        world.NPCs["guy"].set_anim("L")

        world.static["pillows"].set_z(world.static["bed"].z_index + 1
                                      - world.static["pillows"].pos[1]
                                      - world.static["pillows"].current_frame.get_height())

        return world

    def handle_events(self, event):
        keys = pygame.key.get_pressed()
        for key, l in self.event_map.iteritems():
            func, args = l
            if keys[key]:
                func(*args)
                return True
        else:
            self.world.NPCs["guy"].is_moving = False
            return False

    def char_in_bed(self):
        sprite_rect = self.world.NPCs["guy"].col_image.get_rect()
        sprite_rect.x, sprite_rect.y = self.world.NPCs["guy"].col_pos

        bed_rect = self.world.static["bed"].col_image.get_rect()
        bed_rect.x, bed_rect.y = self.world.static["bed"].col_pos

        if bed_rect.colliderect(sprite_rect):
            return True

    def update_loop(self, screen):
        for s in self.world.NPCs.values():
            # Movement
            if s.is_moving:
                if not self.world.check_colliding(s):
                    s.move()
                else:
                    s.set_pos(*s.old_pos)
                self._animate(s)

        if self.char_in_bed():
            self.world.NPCs["guy"].set_z(self.world.static["bed"].z_index + 1
                                         - self.world.NPCs["guy"].pos[1]
                                         - self.world.NPCs["guy"].current_frame.get_height())
        else:
            self.world.NPCs["guy"].set_z(0)

        self.game_time = datetime.now() - self.start_time
        self.clock_time = self.seconds_to_time(self.game_time.total_seconds())
        self.clock_text = self.clock_font.render(self.clock_time, True, (0, 255, 0))

        self.update_clouds()

        # Blitting
        screen.blit(self.sky.current_frame, self.sky.pos)

        for c in sorted(self.clouds, key=lambda x: x.pos[1]):
            screen.blit(c.current_frame, c.pos)

        screen.blit(self.world.bg, self.world.pos)

        for s in self.world.sprites:
            screen.blit(s.current_frame, s.pos)
            if s.name == "alarmClock":
                screen.blit(self.clock_text, (s.pos[0] + 25, s.pos[1] + 20))

        if (datetime.now() - self.snooze_time).total_seconds() >= 9:
            self.display_cmd = True
            self.cmd = "Press 'SPACE' to Snooze"

        if self.display_cmd:
            screen.blit(self.cmd_font.render(self.cmd, True, (255, 255, 255)), FU_CMD_POS)

    def update_clouds(self):
        for c in self.clouds:
            if c.pos[0] > 880:
                c.set_pos(randint(self.cloud_min_x, self.cloud_max_x), randint(self.cloud_min_y, self.cloud_max_y))
            else:
                c.set_pos(c.pos[0] + randint(1,4), c.pos[1])


    def _animate(self, s):
        # Animation
        s.update_dt()
        if s.dt.microseconds > 1.0 / s.fps * 1000000:
            s.next_frame()
