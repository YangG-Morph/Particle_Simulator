import pygame as pg
from data import Utils


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
        self.rect = pg.Rect(position, size)
        self.surface = pg.Surface(size)
        self.surface.fill(self.bg_color)
        self.prev_pos = None

    def handle_collision(self, other_rects):
        for rect in other_rects:
            if self.rect.colliderect(rect):
                pass  # self.position =

    def handle_movement(self, movement, multiplier=1):
        movement = (movement[0] * multiplier, movement[1] * multiplier)
        self.position = (self.position[0] + movement[0], self.position[1] + movement[1])

    def set_movement(self, settings):
        movement = Utils.randfloat(-settings.repel_dist, settings.repel_dist, size=2)
        self.handle_movement(movement, 15)

    def events(self, mouse_pos, settings, time_frozen, mouse_buttons):
        direction = Utils.sub_pos(mouse_pos, self.position)
        magnitude = Utils.hypotenuse(direction)

        if magnitude < settings.barrier_dist:
            movement = Utils.randfloat(-settings.repel_dist, settings.repel_dist, size=2)
            self.handle_movement(movement, settings.repel_multiplier)
        elif not time_frozen and not mouse_buttons[0]:
            self.handle_movement(Utils.normalize(direction, magnitude), settings.speed)

    def update(self, settings):
        self.rect.center = self.position

    def draw(self, surface):
        #surface.blit(self.surface, self.rect.topleft)
        #pg.draw.rect(surface, self.bg_color, self.rect)
        pg.draw.circle(surface, self.bg_color, self.rect.center, self.size[1])
        #gfxdraw.box(surface, self.rect, self.bg_color)
        #gfxdraw.filled_circle(surface, self.rect.center[0], self.rect.center[1], self.size[1], self.bg_color)

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



