import pygame as pg
from data.groups.group import Group
from functools import lru_cache
from data.ui.text import Text

class TextGroup(Group):
    def __init__(self, *members):
        super().__init__(*members)
        self.members = [member for member in members]
        self.clicked = False

    def create_text(self, *args, **kwargs):
        self.append(Text(*args, **kwargs))

    def add(self, *member):
        if isinstance(member, (list, tuple)):
            for m in member:
                self.members.append(m)
        else:
            self.members.append(member)

    def keying(self):
        if [text for text in self.members if text.input_mode]:
            return True
        return False

    def set_hover(self, collided):
        if collided and not self.keying():
            collided.highlight()
            for text in self.members:
                if text != collided:
                    text.dim()
        else:
            for text in self.members:
                if not text.input_mode:
                    text.dim()


    def check_collision(self, mouse_pos):
        for text in self.members:
            if text.slider.collision_rect.collidepoint(mouse_pos):
                return text

    def events(self, keys=None):
        [text.handle_events(keys) for text in self.members]

    def set_values(self, settings):
        [text.set_value(getattr(settings, text.name)) for text in self.members]

    def reset(self, settings):
        [text.reset(settings) for text in self.members]

    def get_prev_collide(self):
        for text in self.members:
            if text.prev_collided:
                return text

    def update_position(self, screen_size):
        [text.update_position(screen_size) for text in self.members]

    def set_value(self, settings):
        [text.set_value(getattr(settings, text.name)) for text in self.members]

    def set_str_value(self, settings):
        [text.set_str_value(getattr(settings, text.name)) for text in self.members]

    def had_collided(self):
        if [text for text in self.members if text.prev_collided]:
            return True
        return False

    def init(self, settings):
        [text.init(settings, idx) for idx, text in enumerate(self.members)]

    @lru_cache()
    def text_collision(self, mouse_pos):
        return [text for text in self.members if text.slider.bg_rect.collidepoint(mouse_pos)]

