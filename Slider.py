import pygame as pg


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