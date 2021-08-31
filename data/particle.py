import pygame as pg
from data import utils
import math

class Particle:
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

    def handle_collision(self, other_particles):
        for particle in other_particles:
            if particle is not self and self.collided(particle):
                direction = utils.randfloat_sample(-10, 10, size=2)
                self.update(direction, 10)

    def collided(self, particle):
        direction = utils.sub_pos(particle.position, self.position)
        magnitude = math.hypot(direction[0], direction[1])
        if magnitude <= 100:
            return True

    def update(self, direction, multiplier=1):
        direction = (direction[0] * multiplier, direction[1] * multiplier)
        self.position = (self.position[0] + direction[0], self.position[1] + direction[1])

    def set_movement(self, settings):
        direction = utils.randfloat_sample(-settings.mouse_repel_dist, settings.mouse_repel_dist, size=2)
        self.update(direction, 15)

    def events(self, mouse_pos, settings, time_frozen, mouse_buttons):
        direction = utils.sub_pos(mouse_pos, self.position)
        magnitude = math.hypot(direction[0], direction[1])

        if magnitude < settings.barrier_dist:
            direction = utils.randfloat_sample(-settings.repel_dist, settings.repel_dist, size=2)
            self.update(direction, settings.repel_dist)
        elif not time_frozen and not mouse_buttons[0]:
            self.update(utils.normalize(direction, magnitude), settings.speed)

    def draw(self, surface):
        pg.draw.circle(surface, self.bg_color, self.position, self.size[1])

    @classmethod
    def create(cls):
        size = utils.randint_sample(1, 5, size=2)
        position = utils.randint_sample(0, 1000, size=2)
        color = utils.randint_sample(0, 255, size=3)
        kwargs = {
            "size": size,
            "position": position,
            "bg_color": color
        }
        return cls(**kwargs)



