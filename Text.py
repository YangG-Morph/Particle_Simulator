import pygame as pg
from functools import lru_cache
from Slider import Slider

class Text:
    all_text = []
    margin_y = 3
    padding_y = 1
    clicked = False
    settings = None

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
        self.value = getattr(Text.settings, self.name) if not ignore else None
        self.value_str = str(self.value)
        self.start_value = None
        self.collided = False
        self.prev_color = None
        self.prev_collided = False
        self.max_width = max_width
        self.ignore = ignore
        self.input_mode = False
        self.keying = False
        self.input_started = False
        Text.all_text.append(self)
        self.index = Text.all_text.index(self)
        self.position = (
            0,
            Text.all_text.index(self) *
            self.rendered_text.get_height() +
            self.margin_y +
            (self.index * self.padding_y)
        )
        self.slider = Slider(
            self.position,
            (self.rendered_text.get_width(), self.rendered_text.get_height()),
            max_width=max_width,
            bg_color=pg.Color("white"),
            fg_color=pg.Color("darkred"),
        )

    def handle_events(self, mouse_pos, mouse_pressed, keys=None):
        left_button, _, right_button = mouse_pressed
        self.collided = self.slider.collision_rect.collidepoint(mouse_pos)

        # TODO limit amount of checks
        if self.collided and not self.ignore and not [t for t in Text.all_text if t.input_mode]:
            self.prev_color = self.fg_color
            self.fg_color = pg.Color("white")
        elif not self.input_mode:
            self.prev_color = self.fg_color
            self.fg_color = pg.Color("grey")

        if left_button and not Text.clicked:
            if not self.ignore and self.slider.collision_rect.collidepoint(mouse_pos):
                Text.clicked = True
                self.input_mode = True
                self.input_started = True
                self.fg_color = pg.Color("white")
                self.font.set_italic(True)
                self.rendered_text = self.font.render(f"{self.orig_text}{self.value}", True, self.fg_color)
                self.value_str = str(self.value)
                for t in Text.all_text:
                    if t is not self and not t.ignore:
                        t.input_mode = False
                        t.keying = False
                        t.input_started = False
                        t.fg_color = pg.Color("grey")
                        t.prev_value = -1
                        t.value = int(t.value_str) if t.value_str.isnumeric() and t.value_str == t.value else t.value # Here bug
                        setattr(Text.settings, t.name, t.value)
            elif self.input_mode:  # TODO Repel Multiplier not setting when clicked after input mode set
                Text.reset(Text.all_text)
        elif right_button and self.collided and not self.ignore and not Text.clicked and not Particle.freeze_time:
            Text.clicked = True
            texts = [t for t in Text.all_text if t.prev_collided]
            if texts:
                Text.reset(texts)
            self.prev_collided = True
            self.value = getattr(Text.settings, self.name)
            self.start_value = getattr(Text.settings, self.name)
            self.slider.start_pos = mouse_pos
            self.slider.update(self.value)
        elif right_button and self.prev_collided:
            self.prev_collided = True
            movement = (mouse_pos[0] - self.slider.start_pos[0]) + (self.slider.start_pos[1] - mouse_pos[1])
            setattr(Text.settings, self.name, movement + self.start_value)
            self.value = getattr(Text.settings, self.name)
            self.slider.update(self.value)
            self.position = (self.slider.max_width, self.position[1])
        elif right_button and not self.prev_collided and self.input_mode:
            Text.reset(Text.all_text)
        elif not right_button and not left_button:
            Text.clicked = False
            if self.prev_collided:
                self.prev_collided = False
            self.position = (0, self.position[1])

        if self.input_mode:
            if not self.keying:
                if keys[pg.K_BACKSPACE] and not self.keying:
                    self.keying = True
                    self.input_started = False
                    self.value_str = self.value_str[:-1]
                    self.rendered_text = self.font.render(f"{self.orig_text}{self.value_str}", True, self.fg_color)
                elif keys[pg.K_RETURN] or keys[pg.K_KP_ENTER]:
                    Text.reset(Text.all_text)

    def update(self):
        if self.name:
            if self.prev_value != getattr(Text.settings, self.name) or self.prev_color != self.fg_color:
                self.value = getattr(Text.settings, self.name)
                self.prev_value = self.value
                if not self.input_mode:
                    self.rendered_text = self.font.render(f"{self.orig_text}{self.value}", True, self.fg_color)
                else:
                    self.rendered_text = self.font.render(f"{self.orig_text}{self.value_str}", True, self.fg_color)

                size = (self.rendered_text.get_width(), self.rendered_text.get_height())
                self.slider.collision_rect.update(self.slider.collision_rect.topleft, size)
                self.slider.update(self.value)
        else:
            if self.prev_value != self.value:
                self.prev_value = self.value
                self.rendered_text = self.font.render(f"{self.orig_text}{self.value}", True, self.fg_color)

    def draw(self, surface):
        self.update()
        surface.blit(self.rendered_text, self.position)
        if Text.clicked and self.prev_collided and not self.ignore:
            self.slider.draw(surface)

    def set_value(self, value):
        self.value = value

    @classmethod
    def reset(cls, texts):
        for t in texts: # TODO Not reseting repel multiplier
            if t.input_mode:
                t.input_mode = False
                t.keying = False
                t.input_started = False
                t.prev_collided = False
                t.fg_color = pg.Color("grey")
                t.prev_value = -1
                t.value = int(t.value_str) if len(t.value_str) > 0 else 0
                setattr(cls.settings, t.name, t.value)
                t.font.set_italic(False)
                t.rendered_text = t.font.render(f"{t.orig_text}{t.value_str}", True, t.fg_color)

    @classmethod
    def group_events(cls, mouse_pos, mouse_pressed, keys=None):
        [text.handle_events(mouse_pos, mouse_pressed, keys) for text in cls.all_text]

    @classmethod
    def group_draw(cls, surface):
        [text.draw(surface) for text in cls.all_text]

    @classmethod
    def set_values(cls, settings):
        [cls.all_text[i].set_value(getattr(settings, cls.all_text[i].name)) for i in range(len(cls.all_text) - 1)]

    @classmethod
    @lru_cache()
    def text_collision(cls, mouse_pos):
        return [t for t in cls.all_text if not t.ignore and t.slider.bg_rect.collidepoint(mouse_pos)]