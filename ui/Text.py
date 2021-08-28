import pygame as pg
from ui.Slider import Slider

class Text:
    margin_y = 3
    padding_y = 1

    def __init__(self,
                 name="",
                 text="",
                 bg_color=pg.Color("black"),
                 fg_color=pg.Color("grey"),
                 ignore=False,
                 max_width=500,
                 ):
        self.orig_text = text
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.name = name
        self.rendered_text = pg.font.SysFont("Calibri", 24).render(f"{self.orig_text}", True, self.fg_color)
        self.prev_value = self.rendered_text
        self.font = pg.font.SysFont("Calibri", 24)
        self.value = 0
        self.str_value = str(self.value)
        self.start_value = None
        self.collided = False
        self.prev_color = None
        self.prev_collided = False
        self.max_width = max_width
        self.ignore = ignore
        self.input_mode = False
        self.keying = False
        self.input_started = False
        self.index = -1
        self.position = (0, 0)
        self.slider = Slider(
            self.position,
            (self.rendered_text.get_width(), self.rendered_text.get_height()),
            max_width=max_width,
            bg_color=pg.Color("white"),
            fg_color=pg.Color("darkred"),
        )

    def init(self, settings, idx):
        if settings:
            self.value = getattr(settings, self.name)
            self.str_value = str(self.value)
            self.reset(settings)
        self.index = idx
        self.position = (
            0,
            idx *
            self.rendered_text.get_height() +
            self.margin_y +
            (self.index * self.padding_y)
        )
        self.slider.update(position=self.position,
                           size=(self.rendered_text.get_width(),
                                 self.rendered_text.get_height() + self.padding_y))

    def highlight(self):
        self.collided = True
        self.prev_color = self.fg_color
        self.fg_color = pg.Color("white")

    def set_focus(self):
        self.input_mode = True
        self.input_started = True
        self.fg_color = pg.Color("white")
        self.font.set_italic(True)
        self.rendered_text = self.font.render(f"{self.orig_text}{self.value}", True, self.fg_color)
        self.str_value = str(self.value)

    def handle_events(self, keys=None):
        if self.input_mode:
            if not self.keying:
                if keys[pg.K_BACKSPACE] and not self.keying:
                    self.keying = True
                    self.input_started = False
                    self.str_value = self.str_value[:-1]
                    self.rendered_text = self.font.render(f"{self.orig_text}{self.str_value}", True, self.fg_color)
                elif keys[pg.K_RETURN] or keys[pg.K_KP_ENTER]:
                    self.reset()

    def update(self, settings=None):
        if settings:
            if self.prev_value != getattr(settings, self.name) or self.prev_color != self.fg_color:
                self.value = getattr(settings, self.name)
                self.prev_value = self.value
                if not self.input_mode:
                    self.rendered_text = self.font.render(f"{self.orig_text}{self.value}", True, self.fg_color)
                else:
                    self.rendered_text = self.font.render(f"{self.orig_text}{self.str_value}", True, self.fg_color)

                size = (self.rendered_text.get_width(), self.rendered_text.get_height())
                self.slider.collision_rect.update(self.slider.collision_rect.topleft, size)
                self.slider.update(size=(self.value, 0))
        else:
            if self.prev_value != self.value:
                self.prev_value = self.value
                self.rendered_text = self.font.render(f"{self.orig_text}{self.value}", True, self.fg_color)

    def draw(self, surface):
        surface.blit(self.rendered_text, self.position)
        if self.prev_collided:
            self.slider.draw(surface)

    def set_value(self, value):
        self.value = value

    def set_str_value(self, value):
        self.str_value = value

    def get_prev_collide(self):
        return self.prev_collided

    def get_inputing(self):
        return self.input_mode

    def reset(self, settings):
        self.input_mode = False
        self.keying = False
        self.input_started = False
        self.prev_collided = False
        self.fg_color = pg.Color("grey")
        self.position = (0, self.position[1])
        temp_value = int(self.str_value) if int(self.str_value) != self.value else self.value
        setattr(settings, self.name, temp_value)
        self.value = getattr(settings, self.name)
        self.str_value = str(self.value)
        self.font.set_italic(False)
        self.rendered_text = self.font.render(f"{self.orig_text}{self.str_value}", True, self.fg_color)
        self.update(settings)

    def __str__(self):
        return self.name


