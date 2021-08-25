import math, random, sys
import pygame as pg

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

class Settings:
    def __init__(self):
        self._speed = 350
        self._barrier_dist = 330
        self._repel_dist = 1
        self._repel_multiplier = 200

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
                 fg_color=pg.Color("white"),
                 collision_ignore=False,
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
        self.start_value = None
        self.collided = False
        self.prev_collided = False
        self.max_width = max_width
        self.collision_ignore = collision_ignore
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

    def handle_events(self, mouse_pos, mouse_pressed, settings):
        _, _, right_button = mouse_pressed
        self.collided = self.slider.collision_rect.collidepoint(mouse_pos)

        if not self.collision_ignore and right_button and self.collided and not self.__class__.clicked:
            self.__class__.clicked = True
            self.prev_collided = True
            self.value = getattr(settings, self.name)
            self.start_value = getattr(settings, self.name)
            self.slider.start_pos = mouse_pos
            self.slider.update(self.value)
        elif right_button and self.prev_collided:
            self.prev_collided = True
            movement = (mouse_pos[0] - self.slider.start_pos[0]) + (self.slider.start_pos[1] - mouse_pos[1])
            setattr(settings, self.name, movement + self.start_value)
            self.value = getattr(settings, self.name)
            self.slider.update(self.value)
            self.position = (self.slider.max_width, self.position[1])
        elif not right_button:
            self.__class__.clicked = False
            self.prev_collided = False
            self.position = (0, self.position[1])

    def update(self):
        if self.prev_value != self.value:
            self.prev_value = self.value
            self.rendered_text = self.font.render(f"{self.orig_text}{self.value}", True, self.fg_color)

            size = (self.rendered_text.get_width(), self.rendered_text.get_height())
            self.slider.collision_rect.update(self.slider.collision_rect.topleft, size)
            self.slider.update(self.value)

    def draw(self, surface):
        self.update()
        surface.blit(self.rendered_text, self.position)
        if self.__class__.clicked and self.prev_collided and not self.collision_ignore:
            self.slider.draw(surface)

    def set_value(self, value):
        self.value = value

    @classmethod
    def group_events(cls, mouse_pos, mouse_pressed, settings):
        [text.handle_events(mouse_pos, mouse_pressed, settings) for text in cls.all_text]

    @classmethod
    def group_draw(cls, surface):
        [text.draw(surface) for text in cls.all_text]

    @classmethod
    def set_values(cls, settings):
        [cls.all_text[i].set_value(getattr(settings, cls.all_text[i].name)) for i in range(len(cls.all_text) - 1)]

class Particle:
    all_particles = []

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
        self.clicked = False
        #self.direction = 0, 0
        self.__class__.all_particles.append(self)

    def handle_collision(self, other_rects):
        for rect in other_rects:
            if self.rect.colliderect(rect):
                pass  # self.position =

    def _handle_movement(self, movement, multiplier=None):
        if multiplier:
            movement = (movement[0] * multiplier, movement[1] * multiplier)
            self.position = (self.position[0] + movement[0], self.position[1] + movement[1])

    @staticmethod
    def _random(min, max, counts=1, as_int=False):  # TODO random.random() instead?
        if True:
            if counts > 1:
                return [random.randint(min, max) for i in range(counts)]
            return random.randint(min, max)
        """ random.uniform is faster but produces different results """
        if counts > 1:
            if as_int:
                return [int(random.uniform(min, max)) for i in range(counts)]
            return [random.uniform(min, max) for i in range(counts)]
        elif as_int:
            return int(random.uniform(min, max))
        return random.uniform(min, max)

    def handle_events(self, mouse_pos, mouse_pressed, settings):
        left_button, middle_button, _, = mouse_pressed
        direction = Utils.sub_pos(mouse_pos, self.position)
        magnitude = Utils.hypotenuse(direction)

        if left_button and not self.clicked:
            self.clicked = True
            movement = Particle._random(-settings.repel_dist, settings.repel_dist, counts=2)
            self._handle_movement(movement, 10)
        elif middle_button and not self.clicked:
            self.clicked = True
            settings.speed = Particle._random(0, MAX_SPEED, as_int=True)
            settings.barrier_dist = Particle._random(0, MAX_BARRIER_DIST, as_int=True)
            settings.repel_dist = Particle._random(0, MAX_REPEL_DIST, as_int=True)
            settings.repel_multiplier = Particle._random(0, MAX_REPEL_MULTIPLIER, as_int=True)
        elif not middle_button:
            self.clicked = False

        if magnitude < settings.barrier_dist:
            movement = Particle._random(-settings.repel_dist, settings.repel_dist, counts=2)
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
            size = Particle._random(1, 5, counts=2, as_int=True)
            position = Particle._random(0, 1000, counts=2, as_int=True)
            color = Particle._random(0, 255, counts=3, as_int=True)
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
    def group_events(cls, mouse_pos, mouse_pressed, settings):
        [particle.handle_events(mouse_pos, mouse_pressed, settings) for particle in cls.all_particles]

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
        self.barrier_text = Text("barrier_dist", "Barrier distance: ", bg_color=self.bg_color, max_width=MAX_BARRIER_DIST)
        self.repel_text = Text("repel_dist", "Repel distance: ", bg_color=self.bg_color, max_width=MAX_REPEL_DIST)
        self.repel_mult_text = Text("repel_multiplier", "Repel multiplier: ", bg_color=self.bg_color, max_width=MAX_REPEL_MULTIPLIER)
        self.fps_text = Text(text="FPS: ", bg_color=self.bg_color, collision_ignore=True)
        Particle.create(MAX_PARTICLES)

    def handle_quit(self):
        for event in pg.event.get():
            if event.type in [pg.QUIT] or event.type in [pg.KEYDOWN] and event.key in [pg.K_ESCAPE]:
                pg.quit()
                sys.exit()

    def run(self):
        while self.running:
            self.handle_quit()
            self.screen.fill(self.bg_color)

            mouse_pos = pg.mouse.get_pos()
            mouse_buttons = pg.mouse.get_pressed()

            Particle.group_events(mouse_pos, mouse_buttons, self.settings)
            Particle.group_draw(self.screen)

            Text.set_values(self.settings)
            Text.group_events(mouse_pos, mouse_buttons, self.settings)
            Text.group_draw(self.screen)

            self.clock.tick(FPS)
            self.fps_text.set_value(int(self.clock.get_fps()))
            pg.display.update()


if __name__ == '__main__':
    pg.init()
    display = pg.display.set_mode(SCREEN_SIZE, flags=pg.RESIZABLE | pg.DOUBLEBUF)
    pg.display.set_caption("Particle Simulator")

    Game(display).run()
