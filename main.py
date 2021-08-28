import math, random, sys
from functools import lru_cache
import pygame as pg
from pygame import gfxdraw  # Unstable avoid

""" Constants """
MAX_PARTICLES = 5_000
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
    def randint(min, max, size=1):
        """ Generate random integer number inclusively """
        width = max - min + 1
        if size > 1:
            return [math.floor(random.random() * width + min) for _ in range(size)]
        return math.floor(random.random() * width + min)

    @staticmethod
    def randfloat(min, max, size=1):
        """ Generate random float number excludes max"""
        width = max - min
        if size > 1:
            return [random.random() * width + min for _ in range(size)]
        return random.random() * width + min

    @staticmethod
    def rand_uniform(min, max, size=1):
        if size > 1:
            return [random.uniform(min, max) for _ in range(size)]
        return random.uniform(min, max)


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
    settings = None

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
        self.value = getattr(Text.settings, self.name) if not ignore_collision else None
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
        Text.all_text.append(self)
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

    def handle_events(self, mouse_pos, mouse_pressed, keys=None):
        left_button, _, right_button = mouse_pressed
        self.collided = self.slider.collision_rect.collidepoint(mouse_pos)

        # TODO limit amount of checks
        if self.collided and not self.ignore_collision and not [t for t in Text.all_text if t.input_mode]:
            self.prev_color = self.fg_color
            self.fg_color = pg.Color("white")
        elif not self.input_mode:
            self.prev_color = self.fg_color
            self.fg_color = pg.Color("grey")

        if left_button and not Text.clicked:
            if not self.ignore_collision and self.slider.collision_rect.collidepoint(mouse_pos):
                Text.clicked = True
                self.input_mode = True
                self.input_started = True
                self.fg_color = pg.Color("white")
                self.font.set_italic(True)
                self.rendered_text = self.font.render(f"{self.orig_text}{self.value}", True, self.fg_color)
                self.value_str = str(self.value)
                for t in Text.all_text:
                    if t is not self and not t.ignore_collision:
                        t.input_mode = False
                        t.keying = False
                        t.input_started = False
                        t.fg_color = pg.Color("grey")
                        t.prev_value = -1
                        t.value = int(t.value_str) if t.value_str.isnumeric() and t.value_str == t.value else t.value # Here bug
                        setattr(Text.settings, t.name, t.value)
            elif self.input_mode:  # TODO Repel Multiplier not setting when clicked after input mode set
                Text.reset(Text.all_text)
        elif right_button and self.collided and not self.ignore_collision and not Text.clicked and not Particle.freeze_time:
            Text.clicked = True
            texts = [t for t in Text.all_text if t.prev_collided]
            if texts:
                Text.reset(texts)
            self.prev_collided = True
            self.value = getattr(Text.settings, self.name)
            self.start_value = getattr(Text.settings, self.name)
            self.slider.start_pos = mouse_pos
            self.slider.update(self.value)
        elif right_button and self.prev_collided:
            self.prev_collided = True
            movement = (mouse_pos[0] - self.slider.start_pos[0]) + (self.slider.start_pos[1] - mouse_pos[1])
            setattr(Text.settings, self.name, movement + self.start_value)
            self.value = getattr(Text.settings, self.name)
            self.slider.update(self.value)
            self.position = (self.slider.max_width, self.position[1])
        elif right_button and not self.prev_collided and self.input_mode:
            Text.reset(Text.all_text)
        elif not right_button and not left_button:
            Text.clicked = False
            if self.prev_collided:
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
                    Text.reset(Text.all_text)

    def update(self):
        if self.name:
            if self.prev_value != getattr(Text.settings, self.name) or self.prev_color != self.fg_color:
                self.value = getattr(Text.settings, self.name)
                self.prev_value = self.value
                if not self.input_mode:
                    self.rendered_text = self.font.render(f"{self.orig_text}{self.value}", True, self.fg_color)
                else:
                    self.rendered_text = self.font.render(f"{self.orig_text}{self.value_str}", True, self.fg_color)

                size = (self.rendered_text.get_width(), self.rendered_text.get_height())
                self.slider.collision_rect.update(self.slider.collision_rect.topleft, size)
                self.slider.update(self.value)
        else:
            if self.prev_value != self.value:
                self.prev_value = self.value
                self.rendered_text = self.font.render(f"{self.orig_text}{self.value}", True, self.fg_color)

    def draw(self, surface):
        self.update()
        surface.blit(self.rendered_text, self.position)
        if Text.clicked and self.prev_collided and not self.ignore_collision:
            self.slider.draw(surface)

    def set_value(self, value):
        self.value = value

    @classmethod
    def reset(cls, texts):
        for t in texts: # TODO Not reseting repel multiplier
            if t.input_mode:
                t.input_mode = False
                t.keying = False
                t.input_started = False
                t.prev_collided = False
                t.fg_color = pg.Color("grey")
                t.prev_value = -1
                t.value = int(t.value_str) if len(t.value_str) > 0 else 0
                setattr(cls.settings, t.name, t.value)
                t.font.set_italic(False)
                t.rendered_text = t.font.render(f"{t.orig_text}{t.value_str}", True, t.fg_color)

    @classmethod
    def group_events(cls, mouse_pos, mouse_pressed, keys=None):
        [text.handle_events(mouse_pos, mouse_pressed, keys) for text in cls.all_text]

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
    settings = None
    freeze_time = False

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
        Particle.all_particles.append(self)

    def handle_collision(self, other_rects):
        for rect in other_rects:
            if self.rect.colliderect(rect):
                pass  # self.position =

    def _handle_movement(self, movement, multiplier=1):
        movement = (movement[0] * multiplier, movement[1] * multiplier)
        self.position = (self.position[0] + movement[0], self.position[1] + movement[1])

    def handle_events(self, mouse_pos, mouse_pressed, keys=None):
        left_button, middle_button, right_button = mouse_pressed
        direction = Utils.sub_pos(mouse_pos, self.position)
        magnitude = Utils.hypotenuse(direction)

        if left_button and not Particle.clicked:
            if not Text.clicked:
                movement = Utils.randfloat(-Particle.settings.repel_dist, Particle.settings.repel_dist, size=2)
                self._handle_movement(movement, 15)
            else:
                Particle.clicked = True
        elif middle_button and not Particle.clicked:
            Particle.clicked = True
            Text.reset(Text.all_text)
            Particle.settings.speed = Utils.randint(0, MAX_SPEED)
            Particle.settings.barrier_dist = Utils.randint(0, MAX_BARRIER_DIST)
            Particle.settings.repel_dist = Utils.randint(0, MAX_REPEL_DIST)
            Particle.settings.repel_multiplier = Utils.randint(0, MAX_REPEL_MULTIPLIER)
        elif right_button and not Particle.clicked and not Text.clicked:
            Particle.freeze_time = True
        elif not middle_button:
            Particle.clicked = False
            Particle.freeze_time = False

        if not Particle.freeze_time:
            self._handle_movement(Utils.normalize(direction, magnitude), Particle.settings.speed)

        if magnitude < Particle.settings.barrier_dist:
            movement = Utils.randfloat(-Particle.settings.repel_dist, Particle.settings.repel_dist, size=2)
            self._handle_movement(movement, Particle.settings.repel_multiplier)

    def update(self):
        self.rect.center = self.position

    def draw(self, surface):
        self.update()
        #surface.blit(self.surface, self.rect.topleft)
        #pg.draw.rect(surface, self.bg_color, self.rect)
        pg.draw.circle(surface, self.bg_color, self.rect.center, self.size[1])
        #gfxdraw.box(surface, self.rect, self.bg_color)
        #gfxdraw.filled_circle(surface, self.rect.center[0], self.rect.center[1], self.size[1], self.bg_color)

    @classmethod
    def create(cls, amount=0):
        for i in range(amount):
            size = Utils.randint(1, 5, size=2)
            position = Utils.randint(0, 1000, size=2)
            color = Utils.randint(0, 255, size=3)
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
    def group_events(cls, mouse_pos, mouse_pressed, keys=None):
        [particle.handle_events(mouse_pos, mouse_pressed, keys) for particle in cls.all_particles]

    @classmethod
    def group_collision(cls, other_rects):
        [particle.handle_collision(other_rects) for particle in cls.all_particles]


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen.set_alpha(None)
        self.running = True
        self.clock = pg.time.Clock()
        self.bg_color = pg.Color("black")
        self.settings = Settings()
        Text.settings = self.settings # TODO better way to pass settings around, maybe a controller class,
        Particle.settings = self.settings # TODO Class methods! Class variables! then object no longer needed

        self.speed_text = Text("speed", "Speed: ", bg_color=self.bg_color, max_width=MAX_SPEED)
        self.barrier_text = Text("barrier_dist", "Barrier distance: ", bg_color=self.bg_color,
                                 max_width=MAX_BARRIER_DIST)
        self.repel_text = Text("repel_dist", "Repel distance: ", bg_color=self.bg_color, max_width=MAX_REPEL_DIST)
        self.repel_mult_text = Text("repel_multiplier", "Repel multiplier: ", bg_color=self.bg_color,
                                    max_width=MAX_REPEL_MULTIPLIER)
        self.fps_text = Text(text="FPS: ", bg_color=self.bg_color, ignore_collision=True)
        Particle.create(MAX_PARTICLES)

    def handle_events(self, events):
        for event in events:
            if event.type in [pg.QUIT] or event.type in [pg.KEYDOWN] and event.key in [pg.K_ESCAPE]:
                pg.quit()
                sys.exit()
            elif event.type in [pg.KEYUP]:
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
        mouse_buttons = pg.mouse.get_pressed(num_buttons=3)
        keys = pg.key.get_pressed()

        Text.group_events(mouse_pos, mouse_buttons, keys) # TODO Event Controller to handle events between classes
        Particle.group_events(mouse_pos, mouse_buttons)  # TODO pass in dt?

    def run(self):
        while self.running:
            if True:
                self.screen.fill(self.bg_color)
            self.handle_events(pg.event.get())

            Particle.group_draw(self.screen)
            Text.group_draw(self.screen)

            self.fps_text.set_value(int(self.clock.get_fps()))
            pg.display.update()

            self.clock.tick(FPS)

if __name__ == '__main__':
    pg.init()
    display = pg.display.set_mode(SCREEN_SIZE, flags=pg.RESIZABLE | pg.DOUBLEBUF | pg.HWSURFACE)
    pg.display.set_caption("Particle Simulator")

    Game(display).run()
