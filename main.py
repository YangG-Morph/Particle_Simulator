import math, random, sys
import pygame as pg

""" 
--- Jello ---
speed = 5
barrier_dist = 40
repel_dist = 50
repel_multiplier = 20

--- Big Donut ---
speed = 300
barrier_dist = 100
repel_dist = 140
repel_multiplier = 20

--- Small donut ---
speed = 75
barrier_dist = 17
repel_dist = 435
repel_multiplier = 2

--- Ring ---
speed = 150
barrier_dist = 70
repel_dist = 160
repel_multiplier = 20

--- Black hole, Space travel ---
speed = 25
barrier_dist = 100
repel_dist = 400
repel_multiplier = 20

--- Swarm ---
speed = 407
barrier_dist = 273
repel_dist = 3
repel_multiplier = 20

--- Fish scale --- 
speed = 350
barrier_dist = 330
repel_dist = 1
repel_multiplier = 20

--- Dancing stars (randint)---
speed = 350
barrier_dist = 330
repel_dist = 1
repel_multiplier = 200

--- Snowflake (randint)---
speed = 18
barrier_dist = 10
repel_dist = 1
repel_multiplier = 50

--- Crystal ball ---
speed = 150
barrier_dist = 1
repel_dist = 288
repel_multiplier = 20

--- Magic square ---
speed = 10
barrier_dist = 10
repel_dist = 5
repel_multiplier = 20

--- Black sun ---
speed = 136
barrier_dist = 203
repel_dist = 50
repel_multiplier = 20

--- Ball of Energy ---
speed = 21
barrier_dist = 4
repel_dist = 130
repel_multiplier = 4

--- Sucked in ---
speed = 8
barrier_dist = 10
repel_dist = 359
repel_multiplier = 2

--- Disco ball ---
speed = 179
barrier_dist = 88
repel_dist = 5
repel_multiplier = 2

--- Huge planet ---
speed = 34
barrier_dist = 267
repel_dist = 61
repel_multiplier = 5

--- Butterflies ---
speed = 21
barrier_dist = 118
repel_dist = 1
repel_multiplier = 2

--- School of fish (random.uniform) ---
speed = 392
barrier_dist = 284
repel_dist = 2
repel_multiplier = 5
"""

MAX_PARTICLES = 5_000
SCREEN_SIZE = (1250, 750)

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
        self._speed = value

    @property
    def barrier_dist(self):
        return self._barrier_dist

    @barrier_dist.setter
    def barrier_dist(self, value):
        self._barrier_dist = value

    @property
    def repel_dist(self):
        return self._repel_dist

    @repel_dist.setter
    def repel_dist(self, value):
        self._repel_dist = value

    @property
    def repel_multiplier(self):
        return self._repel_multiplier

    @repel_multiplier.setter
    def repel_multiplier(self, value):
        self._repel_multiplier = value

class Text:
    all_text = []
    margin_y = 3

    def __init__(self, name="", text="", color=pg.Color("white")):
        self.orig_text = text
        self.color = color
        self.name = name
        self.rendered_text = pg.font.SysFont("Calibri", 24).render(f"{self.orig_text}", True, self.color)
        self.prev_value = self.rendered_text
        self.position = (0, 0)
        self.font = pg.font.SysFont("Calibri", 24)
        self.value = None
        self.__class__.all_text.append(self)

    def update(self):
        if self.prev_value != self.value:
            self.position = (0, Text.all_text.index(self) * self.rendered_text.get_height() + self.margin_y)
            self.prev_value = self.value
            self.rendered_text = self.font.render(f"{self.orig_text}{self.value}", True, self.color)

    def draw(self, screen):
        self.update()
        screen.blit(self.rendered_text, self.position)

    def set_value(self, value):
        self.value = value

    @classmethod
    def set_values(cls, settings):
        [cls.all_text[i].set_value(settings.__getattribute__(cls.all_text[i].name)) for i in range(len((cls.all_text)) - 1)]

    @classmethod
    def group_draw(cls, screen):
        [text.draw(screen) for text in cls.all_text]


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
        self.a, self.b = 0, 0
        self.__class__.all_particles.append(self)

    def handle_collision(self, other_rects):
        for other_rect in other_rects:
            if self.rect.colliderect(other_rect):
                pass  # self.position = (self.position[0], other_rect.y - self.rect.height)

    def _handle_movement(self, movement, multiplier=None):
        if multiplier:
            movement = (movement[0] * multiplier, movement[1] * multiplier)
            self.position = (self.position[0] + movement[0], self.position[1] + movement[1])

    def _hypotenuse(self, other_pos):
        self.a, self.b = other_pos[0] - self.position[0], other_pos[1] - self.position[1]
        return math.hypot(self.a, self.b)

    def _normalize(self, magnitude):
        if magnitude > 0:
            normalized = (self.a / magnitude, self.b / magnitude)
            return normalized
        return 0, 0

    @staticmethod
    def _random(min, max, counts=1, as_int=False):  # TODO random.random() instead?
        if False:
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
        left_button, _, right_button = mouse_pressed
        magnitude = self._hypotenuse(mouse_pos)

        if left_button and not self.clicked:
            self.clicked = True
            movement = Particle._random(-settings.repel_dist, settings.repel_dist, counts=2)
            self._handle_movement(movement, 10)
        elif right_button and not self.clicked:
            self.clicked = True
            settings.speed = Particle._random(0, 500, as_int=True)
            settings.barrier_dist = Particle._random(0, 300, as_int=True)
            settings.repel_dist = Particle._random(0, 500, as_int=True)
            settings.repel_multiplier = Particle._random(0, 50, as_int=True)
        elif not right_button:
            self.clicked = False

        if magnitude < settings.barrier_dist:
            movement = Particle._random(-settings.repel_dist, settings.repel_dist, counts=2)
            self._handle_movement(movement, settings.repel_multiplier)
        else:
            self._handle_movement(self._normalize(magnitude), settings.speed)

    def update(self):
        self.rect.center = self.position

    def draw(self, screen):
        self.update()
        screen.blit(self.surface, self.rect.topleft)
        # pg.draw.rect(screen, self.bg_color, self.rect)
        # pg.draw.circle(screen, self.bg_color, self.rect.center, self.size[0])

    def set_value(self, value):
        pass

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
    def group_draw(cls, screen):
        [particle.draw(screen) for particle in cls.all_particles]

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
        Particle.create(MAX_PARTICLES)
        self.settings = Settings()
        self.speed_text = Text("speed", "Speed: ")
        self.barrier_text = Text("barrier_dist", "Barrier distance: ")
        self.repel_text = Text("repel_dist", "Repel distance: ")
        self.repel_mult_text = Text("repel_multiplier", "Repel multiplier: ")
        self.fps_text = Text(text="FPS: ")

    def run(self):
        FPS = 60

        while self.running:
            self.screen.fill("black")
            for event in pg.event.get():
                if event.type in [pg.QUIT]:
                    pg.quit()
                    sys.exit()

            Particle.group_events(pg.mouse.get_pos(), pg.mouse.get_pressed(), self.settings)
            Particle.group_draw(self.screen)
            Text.set_values(self.settings)
            Text.group_draw(self.screen)

            self.clock.tick(FPS)
            self.fps_text.set_value(int(self.clock.get_fps()))
            pg.display.update()


if __name__ == '__main__':
    pg.init()
    display = pg.display.set_mode(SCREEN_SIZE, flags=pg.RESIZABLE | pg.DOUBLEBUF)
    pg.display.set_caption("Particle Simulator")

    Game(display).run()



