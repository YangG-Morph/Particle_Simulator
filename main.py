import random
import pygame as pg
import sys

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

--- Dancing stars ---
speed = 350
barrier_dist = 330
repel_dist = 1
repel_multiplier = 200

--- Snowflake ---
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
"""
speed = 5
barrier_dist = 40
repel_dist = 50
repel_multiplier = 20

MAX_PARTICLES = 5_000
SCREEN_SIZE = (1250, 750)

class Text:
    all_text = []

    def __init__(self, text="", color=pg.Color("white")):
        self.orig_text = text
        self.color = color
        self.rendered_text = pg.font.SysFont("Calibri", 24).render(f"{self.orig_text}", True, self.color)
        self.prev_value = self.rendered_text
        self.position = (0, 0)
        self.font = pg.font.SysFont("Calibri", 24)
        self.__class__.all_text.append(self)

    def update(self):
        global speed
        global barrier_dist
        global repel_dist
        global repel_multiplier

        margin_y = 3
        text_values = [speed, barrier_dist, repel_dist, repel_multiplier]

        try:
            text_values.append(self.fps)
        except AttributeError:
            text_values.append(None)

        for i, text in enumerate(self.__class__.all_text):
            if text == self and self.prev_value != text_values[i]:
                self.position = (0, i * self.rendered_text.get_height() + margin_y)
                self.prev_value = text_values[i]
                self.rendered_text = self.font.render(f"{self.orig_text}{text_values[i]}", True, self.color)
                break

    def draw(self, screen):
        self.update()
        screen.blit(self.rendered_text, self.position)

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
        if multiplier is not None:
            movement = (movement[0] * multiplier, movement[1] * multiplier)
        self.position = (self.position[0] + movement[0], self.position[1] + movement[1])

    def _hypotenuse(self, other_pos):
        self.a, self.b = other_pos[0] - self.position[0], other_pos[1] - self.position[1]
        return (self.a ** 2 + self.b ** 2) ** 0.5

    def _normalize(self, magnitude):
        normalized = (0, 0)
        if magnitude > 0:
            normalized = (self.a / magnitude, self.b / magnitude)
        return normalized

    @staticmethod
    def _random(min, max, counts=1, as_int=False):
        if True:
            if counts > 1:
                return [random.randint(min, max) for i in range(counts)]
            return random.randint(min, max)

        if counts > 1 and not as_int:
            return [random.uniform(min, max) for i in range(counts)]
        elif counts > 1 and as_int:
            return [int(random.uniform(min, max)) for i in range(counts)]
        elif as_int:
            return int(random.uniform(min, max))
        else:
            return random.uniform(min, max)

    def handle_events(self, mouse_pos, mouse_pressed):
        global speed
        global barrier_dist
        global repel_dist
        global repel_multiplier

        left_button, _, right_button = mouse_pressed
        magnitude = self._hypotenuse(mouse_pos)

        if left_button and not self.clicked:
            self.clicked = True
            movement = Particle._random(-repel_dist, repel_dist, counts=2)
            self._handle_movement(movement, 10)
        elif right_button and not self.clicked:
            self.clicked = True
            speed = Particle._random(0, 500, as_int=True)
            barrier_dist = Particle._random(0, 300, as_int=True)
            repel_dist = Particle._random(0, 500, as_int=True)
            repel_multiplier = Particle._random(0, 50, as_int=True)
        elif not right_button:
            self.clicked = False

        if magnitude < barrier_dist:
            movement = Particle._random(-repel_dist, repel_dist, counts=2)
            self._handle_movement(movement, repel_multiplier)
        else:
            self._handle_movement(self._normalize(magnitude), speed)

    def update(self):
        self.rect.center = self.position

    def draw(self, screen):
        self.update()
        screen.blit(self.surface, self.rect.topleft)
        #pg.draw.rect(screen, self.bg_color, self.rect)
        #pg.draw.circle(screen, self.bg_color, self.rect.center, self.size[0])

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
    def group_events(cls, mouse_pos, mouse_pressed):
        [particle.handle_events(mouse_pos, mouse_pressed) for particle in cls.all_particles]

    @classmethod
    def group_collision(cls, other_rects):
        [particle.handle_collision(other_rects) for particle in cls.all_particles]


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.clock = pg.time.Clock()
        Particle.create(MAX_PARTICLES)
        self.speed_text = Text("Speed: ")
        self.barrier_text = Text("Barrier distance: ")
        self.repel_text = Text("Repel distance: ")
        self.repel_mult_text = Text("Repel mult: ")
        self.fps_text = Text("FPS: ")

    def run(self):
        FPS = 60

        while self.running:
            self.screen.fill("black")
            for event in pg.event.get():
                if event.type in [pg.QUIT]:
                    pg.quit()
                    sys.exit()

            Particle.group_events(pg.mouse.get_pos(), pg.mouse.get_pressed())
            Particle.group_draw(self.screen)
            Text.group_draw(self.screen)

            self.clock.tick(FPS)
            self.fps_text.fps = int(self.clock.get_fps())
            pg.display.update()


if __name__ == '__main__':
    pg.init()
    display = pg.display.set_mode(SCREEN_SIZE, flags=pg.RESIZABLE)
    pg.display.set_caption("Particle Simulator")

    Game(display).run()


