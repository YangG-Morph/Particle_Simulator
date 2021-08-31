import pygame as pg
from data import Utils
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
        self.randoms_mouse = (Utils.randfloat(-20, 20, size=2) for i in range(100_000))
        self.randoms_repel = (Utils.randfloat(-20, 20, size=2) for i in range(100_000))

    def handle_collision(self, other_particles):
        for particle in other_particles:
            if particle is not self and self.collided(particle):
                movement = Utils.randfloat(-1, 1, size=2)
                self.update(movement, 10)

    def collided(self, particle):
        direction = Utils.sub_pos(particle.position, self.position)
        magnitude = math.hypot(direction[0], direction[1])

        if magnitude <= 100:
            return True

    def update(self, direction, multiplier=1):
        direction = (direction[0] * multiplier, direction[1] * multiplier)
        self.position = (self.position[0] + direction[0], self.position[1] + direction[1])

    def set_movement(self, settings):
        try:
            direction = next(self.randoms_mouse)
        except StopIteration:
            self.randoms_mouse = (Utils.randfloat(-20, 20, size=2) for i in range(100_000_000))
            direction = Utils.randfloat(-settings.mouse_repel_dist, settings.mouse_repel_dist, size=2)
        #direction = Utils.randfloat(-settings.mouse_repel_dist, settings.mouse_repel_dist, size=2)
        self.update(direction, 15)

    def events(self, mouse_pos, settings, time_frozen, mouse_buttons):
        direction = Utils.sub_pos(mouse_pos, self.position)
        magnitude = math.hypot(direction[0], direction[1])

        if magnitude < settings.barrier_dist:
            try:
                direction = next(self.randoms_repel)
            except StopIteration:
                self.randoms_repel = (Utils.randfloat(-20, 20, size=2) for i in range(100_000_000))
                direction = Utils.randfloat(-settings.repel_dist, settings.repel_dist, size=2)
            #direction = Utils.randfloat(-settings.repel_dist, settings.repel_dist, size=2)
            self.update(direction, settings.repel_dist)
        elif not time_frozen and not mouse_buttons[0]:
            self.update(Utils.normalize(direction, magnitude), settings.speed)

    def draw(self, surface):
        pg.draw.circle(surface, self.bg_color, self.position, self.size[1])

    @classmethod
    def create(cls):
        size = Utils.randint(1, 5, size=2)
        position = Utils.randint(0, 1000, size=2)
        color = Utils.randint(0, 255, size=3)
        kwargs = {
            "size": size,
            "position": position,
            "bg_color": color
        }
        return cls(**kwargs)



