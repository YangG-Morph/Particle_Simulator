import math, random, sys
from functools import lru_cache

import pygame as pg
import value as value

""" Constants """
MAX_PARTICLES = 5000
SCREEN_SIZE = (1250, 750)
FPS = 60

MAX_SPEED = 500
MAX_BARRIER_DIST = 500
MAX_REPEL_DIST = 500
MAX_REPEL_MULTIPLIER = 200


class Utils:
    @staticmethod
    def clamp(value, min, max):
        return min if value < min else max if value > max else value

    @staticmethod
    def sub_pos(end_pos, start_pos):
        return end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]

    @staticmethod
    def hypotenuse(ab):
        return math.hypot(ab[0], ab[1])

    @staticmethod
    def normalize(ab, magnitude):
        if magnitude > 0:
            return ab[0] / magnitude, ab[1] / magnitude
        return 0, 0

    @staticmethod
    def randint(min, max, count=1):
        """ Max is inclusive """
        min = math.ceil(min)
        max = math.floor(max + 1)

        if count > 1:
            return [math.floor(random.random() * (max - min) + min) for _ in range(count)]
        return math.floor(random.random() * (max - min) + min)

    @staticmethod
    def randfloat(min, max, count=1):
        """ Max is exclusive"""
        if count > 1:
            return [random.random() * (max - min) + min for _ in range(count)]
        return random.random() * (max - min) + min


class Settings:
    def __init__(self):
        self._speed = 10
        self._barrier_dist = 20
        self._repel_dist = 10
        self._repel_multiplier = 2

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = Utils.clamp(value, 0, MAX_SPEED)

    @property
    def barrier_dist(self):
        return self._barrier_dist

    @barrier_dist.setter
    def barrier_dist(self, value):
        self._barrier_dist = Utils.clamp(value, 0, MAX_BARRIER_DIST)

    @property
    def repel_dist(self):
        return self._repel_dist

    @repel_dist.setter
    def repel_dist(self, value):
        self._repel_dist = Utils.clamp(value, 0, MAX_REPEL_DIST)

    @property
    def repel_multiplier(self):
        return self._repel_multiplier

    @repel_multiplier.setter
    def repel_multiplier(self, value):
        self._repel_multiplier = Utils.clamp(value, 0, MAX_REPEL_MULTIPLIER)

    def __str__(self):
        return f"speed: {self._speed}\n" \
               f"barrier dist: {self._barrier_dist}\n" \
               f"repel dist: {self._repel_dist}\n" \
               f"repel mult: {self._repel_multiplier}\n"

class Slider:
    def __init__(self,
                 position=(0, 0),
                 size=(1, 5),
                 bg_color=pg.Color("black"),
                 fg_color=pg.Color("white"),
                 max_width=500,
                 ):
        self.position = position
        self.size = size
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.start_pos = self.position
        self.max_width = max_width
        self.collision_rect = pg.Rect(self.position, (size[0], size[1]))
        self.bg_rect = pg.Rect(self.position, (max_width, size[1]))
        self.fg_rect = pg.Rect(self.position, (max_width, size[1]))

    def update(self, width):
        if width is not None:
            if self.max_width >= width >= 0:
                self.fg_rect.update(self.position, (width, self.size[1]))
            elif width > self.max_width:
                self.fg_rect.update(self.position, (self.max_width, self.size[1]))
            elif width < 0:
                self.fg_rect.update(self.position, (0, self.size[1]))

    def draw(self, surface):
        pg.draw.rect(surface, self.bg_color, self.bg_rect)
        pg.draw.rect(surface, self.fg_color, self.fg_rect)


class Text:
    all_text = []
    margin_y = 3
    padding_y = 1
    clicked = False

    def __init__(self,
                 name="",
                 text="",
                 bg_color=pg.Color("black"),
                 fg_color=pg.Color("grey"),
                 ignore_collision=False,
                 max_width=500,
                 ):
        self.orig_text = text
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.name = name
        self.rendered_text = pg.font.SysFont("Calibri", 24).render(f"{self.orig_text}", True, self.fg_color)
        self.prev_value = self.rendered_text
        self.font = pg.font.SysFont("Calibri", 24)
        self.value = None
        self.value_str = str(self.value)
        self.start_value = None
        self.collided = False
        self.prev_color = None
        self.prev_collided = False
        self.max_width = max_width
        self.ignore_collision = ignore_collision
        self.input_mode = False
        self.keying = False
        self.input_started = False
        self.__class__.all_text.append(self)
        self.index = Text.all_text.index(self)
        self.position = (
            0,
            Text.all_text.index(self) *
            self.rendered_text.get_height() +
            self.margin_y +
            (self.index * self.padding_y)
        )
        self.slider = Slider(
            self.position,
            (self.rendered_text.get_width(), self.rendered_text.get_height()),
            max_width=max_width,
            bg_color=pg.Color("white"),
            fg_color=pg.Color("darkred"),
        )

    def handle_events(self, mouse_pos, mouse_pressed, settings, keys=None):
        _, _, right_button = mouse_pressed
        self.collided = self.slider.collision_rect.collidepoint(mouse_pos)

        if self.collided and not self.ignore_collision and not [t for t in Text.all_text if t.input_mode]:
            self.prev_color = self.fg_color
            self.fg_color = pg.Color("white")
        elif not self.input_mode:
            self.prev_color = self.fg_color
            self.fg_color = pg.Color("grey")

        if not self.ignore_collision and right_button and self.collided and not self.__class__.clicked:
            self.__class__.clicked = True
            self.prev_collided = True
            self.value = getattr(settings, self.name)
            self.start_value = getattr(settings, self.name)
            self.slider.start_pos = mouse_pos
            self.slider.update(self.value)
        elif right_button and self.prev_collided:
            self.prev_collided = True
            Text.update_settings(settings)
            movement = (mouse_pos[0] - self.slider.start_pos[0]) + (self.slider.start_pos[1] - mouse_pos[1])
            setattr(settings, self.name, movement + self.start_value)
            self.value = getattr(settings, self.name)
            self.slider.update(self.value)
            self.position = (self.slider.max_width, self.position[1])
        elif not right_button:
            self.__class__.clicked = False
            self.prev_collided = False
            self.position = (0, self.position[1])

        if self.input_mode:
            if not self.keying:
                if keys[pg.K_BACKSPACE] and not self.keying:
                    self.keying = True
                    self.input_started = False
                    self.value_str = self.value_str[:-1]
                    self.rendered_text = self.font.render(f"{self.orig_text}{self.value_str}", True, self.fg_color)
                elif keys[pg.K_RETURN] or keys[pg.K_KP_ENTER]:
                    Text.update_settings(settings)

    def update(self):
        if self.prev_value != self.value or self.prev_color != self.fg_color:
            self.prev_value = self.value
            if not self.input_mode:
                self.rendered_text = self.font.render(f"{self.orig_text}{self.value}", True, self.fg_color)
            else:
                self.rendered_text = self.font.render(f"{self.orig_text}{self.value_str}", True, self.fg_color)

            size = (self.rendered_text.get_width(), self.rendered_text.get_height())
            self.slider.collision_rect.update(self.slider.collision_rect.topleft, size)
            self.slider.update(self.value)

    def draw(self, surface):
        self.update()
        surface.blit(self.rendered_text, self.position)
        if self.__class__.clicked and self.prev_collided and not self.ignore_collision:
            self.slider.draw(surface)

    def set_value(self, value):
        self.value = value

    @classmethod
    def update_settings(cls, settings):
        for t in Text.all_text:
            if t.input_mode:
                t.input_mode = False
                t.keying = False
                t.input_started = False
                t.fg_color = pg.Color("grey")
                t.prev_value = -1
                t.value = int(t.value_str) if len(t.value_str) > 0 else 0
                setattr(settings, t.name, t.value)
                t.rendered_text = t.font.render(f"{t.orig_text}{t.value_str}", True, t.fg_color)

    @classmethod
    def group_events(cls, mouse_pos, mouse_pressed, settings, keys=None):
        [text.handle_events(mouse_pos, mouse_pressed, settings, keys) for text in cls.all_text]

    @classmethod
    def group_draw(cls, surface):
        [text.draw(surface) for text in cls.all_text]

    @classmethod
    def set_values(cls, settings):
        [cls.all_text[i].set_value(getattr(settings, cls.all_text[i].name)) for i in range(len(cls.all_text) - 1)]

    @classmethod
    @lru_cache()
    def text_collision(cls, mouse_pos):
        return [t for t in cls.all_text if not t.ignore_collision and t.slider.bg_rect.collidepoint(mouse_pos)]


class Particle:
    all_particles = []
    clicked = False

    def __init__(self,
                 size=(50, 50),
                 position=(0, 0),
                 bg_color=pg.Color("lightblue"),
                 fg_color=pg.Color("white"),
                 ):
        self.size = size
        self.position = position
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.rect = pg.Rect(position, size)
        self.surface = pg.Surface(size)
        self.surface.fill(self.bg_color)
        self.prev_pos = None
        self.__class__.all_particles.append(self)

    def handle_collision(self, other_rects):
        for rect in other_rects:
            if self.rect.colliderect(rect):
                pass  # self.position =

    def _handle_movement(self, movement, multiplier=None):
        if multiplier:
            movement = (movement[0] * multiplier, movement[1] * multiplier)
            self.position = (self.position[0] + movement[0], self.position[1] + movement[1])

    def handle_events(self, mouse_pos, mouse_pressed, settings, keys=None):
        left_button, middle_button, right_button = mouse_pressed
        direction = Utils.sub_pos(mouse_pos, self.position)
        magnitude = Utils.hypotenuse(direction)

        if left_button and not self.__class__.clicked:
            if not Text.clicked: # TODO move out of Particle to Text
                text = Text.text_collision(mouse_pos)
                if text:
                    Text.clicked = True
                    text = text[0]
                    text.input_mode = True
                    text.input_started = True
                    text.fg_color = pg.Color("white")
                    text.rendered_text = text.font.render(f"{text.orig_text}{text.value}", True, text.fg_color)
                    text.value_str = str(text.value)
                    for t in Text.all_text:
                        if t is not text:
                            t.input_mode = False
                            t.keying = False
                            t.input_started = False
                            t.fg_color = pg.Color("grey")
                            t.prev_value = -1
                            t.value = int(t.value_str) if t.value_str.isnumeric() else t.value
                            setattr(settings, t.name, t.value)
                else:
                    Text.clicked = False
                    Text.update_settings(settings)
                    movement = Utils.randfloat(-settings.repel_dist, settings.repel_dist, count=2)
                    self._handle_movement(movement, 15)
            else:
                self.__class__.clicked = True
        elif middle_button and not self.__class__.clicked:
            self.__class__.clicked = True
            settings.speed = Utils.randint(0, MAX_SPEED)
            settings.barrier_dist = Utils.randint(0, MAX_BARRIER_DIST)
            settings.repel_dist = Utils.randint(0, MAX_REPEL_DIST)
            settings.repel_multiplier = Utils.randint(0, MAX_REPEL_MULTIPLIER)
        elif right_button and not self.__class__.clicked:
            Text.update_settings(settings)
        elif not middle_button and not left_button and not right_button:
            self.__class__.clicked = False

        if magnitude < settings.barrier_dist:
            movement = Utils.randfloat(-settings.repel_dist, settings.repel_dist, count=2)
            self._handle_movement(movement, settings.repel_multiplier)
        else:
            self._handle_movement(Utils.normalize(direction, magnitude), settings.speed)

    def update(self):
        self.rect.center = self.position

    def draw(self, surface):
        self.update()
        surface.blit(self.surface, self.rect.topleft)
        # pg.draw.rect(surface, self.bg_color, self.rect)
        # pg.draw.circle(surface, self.bg_color, self.rect.center, self.size[0])

    @classmethod
    def create(cls, amount=0):
        for i in range(amount):
            size = Utils.randint(1, 5, count=2)
            position = Utils.randint(0, 1000, count=2)
            color = Utils.randint(0, 255, count=3)
            kwargs = {
                "size": size,
                "position": position,
                "bg_color": color
            }
            cls(**kwargs)

    @classmethod
    def group_draw(cls, surface):
        [particle.draw(surface) for particle in cls.all_particles]

    @classmethod
    def group_events(cls, mouse_pos, mouse_pressed, settings, keys=None):
        [particle.handle_events(mouse_pos, mouse_pressed, settings, keys) for particle in cls.all_particles]

    @classmethod
    def group_collision(cls, other_rects):
        [particle.handle_collision(other_rects) for particle in cls.all_particles]


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pg.time.Clock()
        self.bg_color = pg.Color("black")
        self.settings = Settings()
        self.speed_text = Text("speed", "Speed: ", bg_color=self.bg_color, max_width=MAX_SPEED)
        self.barrier_text = Text("barrier_dist", "Barrier distance: ", bg_color=self.bg_color,
                                 max_width=MAX_BARRIER_DIST)
        self.repel_text = Text("repel_dist", "Repel distance: ", bg_color=self.bg_color, max_width=MAX_REPEL_DIST)
        self.repel_mult_text = Text("repel_multiplier", "Repel multiplier: ", bg_color=self.bg_color,
                                    max_width=MAX_REPEL_MULTIPLIER)
        self.fps_text = Text(text="FPS: ", bg_color=self.bg_color, ignore_collision=True)
        Particle.create(MAX_PARTICLES)

    def handle_quit(self, event):
        if event.type in [pg.QUIT] or event.type in [pg.KEYDOWN] and event.key in [pg.K_ESCAPE]:
            pg.quit()
            sys.exit()

    def run(self):
        pg.key.set_repeat(0)

        while self.running:
            self.screen.fill(self.bg_color)  # TODO Cool effect if delayed?

            for event in pg.event.get():
                self.handle_quit(event)
                if event.type in [pg.KEYUP]:
                    for text in Text.all_text:
                        text.keying = False
                elif event.type in [pg.KEYDOWN]:
                    text = [t for t in Text.all_text if t.input_mode]
                    if event.unicode.isdigit() and text:
                        text = text[0]
                        if text.input_started:
                            text.value_str = event.unicode
                            text.input_started = False
                        else:
                            text.value_str += event.unicode
                        text.rendered_text = text.font.render(f"{text.orig_text}{text.value_str}", True, text.fg_color)

            mouse_pos = pg.mouse.get_pos()
            mouse_buttons = pg.mouse.get_pressed()
            keys = pg.key.get_pressed()

            Particle.group_events(mouse_pos, mouse_buttons, self.settings)
            Particle.group_draw(self.screen)

            Text.set_values(self.settings)
            Text.group_events(mouse_pos, mouse_buttons, self.settings, keys)
            Text.group_draw(self.screen)

            self.clock.tick(FPS)
            self.fps_text.set_value(int(self.clock.get_fps()))
            pg.display.update()


if __name__ == '__main__':
    pg.init()
    display = pg.display.set_mode(SCREEN_SIZE, flags=pg.RESIZABLE | pg.DOUBLEBUF)
    pg.display.set_caption("Particle Simulator")

    Game(display).run()
