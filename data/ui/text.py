import pygame as pg
from data.ui.slider import Slider
from data.ui.font import Font

class Text:
    margin_top = 5
    padding_top = 5
    margin_left = 5
    margin_right = 5
    padding_left = 8
    text_spacing = 1

    def __init__(self,
                 name="",
                 text="",
                 bg_color=pg.Color("black"),
                 fg_color=pg.Color("grey"),
                 max_width=500,
                 position=(0, 0),
                 anchor_top=False,
                 anchor_bottom=False,
                 anchor_left=False,
                 anchor_right=False,
                 ):
        self.orig_text = text.upper()
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.name = name
        self.font = Font()
        self.rendered_text = self.font.render(f"{self.orig_text}", self.fg_color)
        self.prev_value = self.rendered_text
        self.value = 0
        self.str_value = str(self.value)
        self.start_value = None
        self.collided = False
        self.prev_color = None
        self.prev_collided = False
        self.max_width = max_width
        self.input_mode = False
        self.keying = False
        self.input_started = False
        self.index = -1
        self.position = position
        self.anchor_top = anchor_top
        self.anchor_bottom = anchor_bottom
        self.anchor_left = anchor_left
        self.anchor_right = anchor_right
        self.slider = Slider(
            self.position,
            (self.rendered_text.get_width(), self.rendered_text.get_height()),
            max_width=max_width,
            bg_color=pg.Color("white"),
            fg_color=pg.Color("darkred"),
        )

    def init(self, settings=None, idx=None):
        if settings:
            self.value = getattr(settings, self.name)
            self.str_value = str(self.value)
            self.reset(settings)
        self.index = idx
        self.update_position(pg.display.get_surface().get_size())


    def highlight(self):
        self.collided = True
        self.prev_color = self.fg_color
        self.fg_color = pg.Color("white")
        self.font.set_bold(True)

    def dim(self):
        if not self.prev_collided:
            self.prev_color = self.fg_color
            self.fg_color = pg.Color("grey")
            self.font.set_bold(False)

    def set_focus(self):
        self.input_mode = True
        self.input_started = True
        self.fg_color = pg.Color("white")
        self.font.set_italic(True)
        self.font.set_bold(True)
        self.rendered_text = self.font.render(f"{self.orig_text}{self.value}", self.fg_color)
        self.str_value = str(self.value)

    def update(self, settings=None):
        if settings:
            if self.prev_value != getattr(settings, self.name) or self.prev_color != self.fg_color:
                self.value = getattr(settings, self.name)
                self.prev_value = self.value
                if not self.input_mode:
                    self.rendered_text = self.font.render(f"{self.orig_text}{self.value}", self.fg_color)
                else:
                    self.rendered_text = self.font.render(f"{self.orig_text}{self.str_value}", self.fg_color)

                size = (self.rendered_text.get_width(), self.rendered_text.get_height())
                self.slider.collision_rect.update(self.slider.collision_rect.topleft, size)
                self.slider.update(size=(self.value, 0))
        else:
            if self.prev_value != self.value:
                self.prev_value = self.value
                self.rendered_text = self.font.render(f"{self.orig_text}{self.value}", self.fg_color)

    def update_position(self, screen_size):
        x, y = self.position

        if self.anchor_left:
            x = 0 + self.margin_left
        if self.anchor_bottom:
            y = screen_size[1] - self.rendered_text.get_height()
        if self.anchor_top:
            y = self.rendered_text.get_height() * self.index + self.margin_top
        if self.anchor_right:
            size = self.font.get_rendered_size(f"{self.orig_text}{self.value:02}")
            x = screen_size[0] - (size[0] + self.margin_right)
        self.position = x, y
        self.slider.update(position=self.position,
                           size=(self.rendered_text.get_width(),
                                 self.rendered_text.get_height() + self.margin_top))

    def draw(self, surface):
        surface.blit(self.rendered_text, self.position)
        if self.prev_collided:
            self.slider.draw(surface)

    def set_value(self, value):
        self.value = value

    def set_str_value(self, value):
        self.str_value = value

    def set_pos(self, pos):
        self.position = pos

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
        if self.str_value:
            temp_value = int(self.str_value) if int(self.str_value) != self.value else self.value
        else:
            temp_value = 0
        setattr(settings, self.name, temp_value)
        self.value = getattr(settings, self.name)
        self.str_value = str(self.value)
        self.font.set_italic(False)
        self.font.set_bold(False)
        self.rendered_text = self.font.render(f"{self.orig_text}{self.str_value}", self.fg_color)
        self.update(settings)
        self.update_position(pg.display.get_surface().get_size())

    def __str__(self):
        return self.name


