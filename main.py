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

--- Grouped ---
speed = 407
barrier_dist = 273
repel_dist = 3
repel_multiplier = 20

--- Fish scale --- 
speed = 350
barrier_dist = 330
repel_dist = 1
repel_multiplier = 20

--- Crystal ball ---
speed = 150
barrier_dist = 1
repel_dist = 288
repel_multiplier = 20

--- Three X's ---
speed = 18
barrier_dist = 10
repel_dist = 1
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

"""
speed = 5
barrier_dist = 40
repel_dist = 50
repel_multiplier = 20

MAX_PARTICLES = 3000

class Text:
    all_text = []

    def __init__(self, text="", color=pg.Color("white")):
        self.orig_text = text
        self.color = color
        self.rendered_text = pg.font.SysFont("Calibri", 24).render(f"{self.orig_text}", True, self.color)
        self.position = (0, 0)
        self.__class__.all_text.append(self)

    def update(self):
        global speed
        global barrier_dist
        global repel_dist
        global repel_multiplier

        try:
            settings = [speed, barrier_dist, repel_dist, repel_multiplier, self.fps]
        except AttributeError:
            settings = [speed, barrier_dist, repel_dist, repel_multiplier, None]

        for i, text in enumerate(self.__class__.all_text):
            if text == self:
                self.position = (0, i * self.rendered_text.get_height())
                font = pg.font.SysFont("Calibri", 24)
                self.rendered_text = font.render(f"{self.orig_text}{settings[i]}", True, self.color)

    def draw(self, screen):
        self.update()
        screen.blit(self.rendered_text, self.position)

    @classmethod
    def group_draw(cls, screen):
        for text in cls.all_text:
            text.draw(screen)

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
        self.clicked = False
        self.__class__.all_particles.append(self)

    def handle_collision(self, other_rects):
        for other_rect in other_rects:
            if self.rect.colliderect(other_rect):
                self.position = (self.position[0], other_rect.y - self.rect.height)

    def _handle_movement(self, movement, multiplier=1):
        if multiplier > 1:
            movement = tuple(i * multiplier for i in movement)
        self.position = tuple(i + j for i, j in zip(self.position, movement))

    def _hypotenuse(self, other_pos):
        a, b = tuple(i - j for i, j in zip(other_pos, self.position))
        return (a ** 2 + b ** 2) ** 0.5

    def _normalize(self, other_pos):
        a, b = tuple(i - j for i, j in zip(other_pos, self.position))
        magnitude = (a ** 2 + b ** 2) ** 0.5
        normalized = (0, 0)

        if magnitude > 0:
            normalized = (a / magnitude, b / magnitude)

        return normalized

    def handle_events(self):
        global speed
        global barrier_dist
        global repel_dist
        global repel_multiplier

        mouse_pos = pg.mouse.get_pos()
        left_button, _, right_button = pg.mouse.get_pressed()

        magnitude = self._hypotenuse(mouse_pos)
        movement = self._normalize(mouse_pos)

        if left_button and not self.clicked:
            self.clicked = True
            self._handle_movement(random.SystemRandom().sample(range(-repel_dist, repel_dist), 2), 10)
        elif right_button and not self.clicked:
            self.clicked = True
            speed = random.SystemRandom().randint(1, 500)
            barrier_dist = random.SystemRandom().randint(1, 300)
            repel_dist = random.SystemRandom().randint(1, 500)
            repel_multiplier = random.SystemRandom().randint(1, 20)
        elif not left_button and not right_button:
            self.clicked = False

        if magnitude < barrier_dist:
            self._handle_movement(random.SystemRandom().sample(range(-repel_dist, repel_dist), 2), repel_multiplier)
        else:
            self._handle_movement(movement, speed)

    def update(self):
        self.surface.fill(self.bg_color)
        self.rect.center = self.position

    def draw(self, screen):
        self.update()
        center = (self.position[0] - self.size[0] / 2, self.position[1] - self.size[1] / 2)
        screen.blit(self.surface, center)
        #pg.draw.rect(screen, self.fg_color, self.rect)

    @classmethod
    def create(cls, amount=0):
        for i in range(amount):
            size = random.SystemRandom().sample(range(1, 5), 2)
            position = random.SystemRandom().sample(range(0, 1000), 2)
            color = random.SystemRandom().sample(range(0, 255), 3)
            args = {
                "size": size,
                "position": position,
                "bg_color": color
            }
            cls(**args)

    @classmethod
    def group_draw(cls, screen):
        for particle in cls.all_particles:
            particle.draw(screen)

    @classmethod
    def group_events(cls):
        for particle in cls.all_particles:
            particle.handle_events()

    @classmethod
    def group_collision(cls, other_rects):
        for particle in cls.all_particles:
            particle.handle_collision(other_rects)



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

            Particle.group_events()
            Particle.group_draw(self.screen)
            Text.group_draw(self.screen)

            self.clock.tick(FPS)
            self.fps_text.fps = int(self.clock.get_fps())
            pg.display.update()


if __name__ == '__main__':
    pg.init()
    screen_size = (750, 750)
    display = pg.display.set_mode(screen_size, flags=0)

    Game(display).run()


