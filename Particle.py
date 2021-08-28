import pygame as pg
import Utils
from CONSTANTS import *
from Text import Text

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

