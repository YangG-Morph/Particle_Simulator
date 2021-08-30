import pygame as pg
import os
from data.constants import DEFAULT_FONT, DEFAULT_FONT_BOLD
from data.assets.paths import FONTS_DIR

class Font:
    def __init__(self):
        self.font_name = DEFAULT_FONT
        self.size = 24
        self.font_path = os.path.join(FONTS_DIR, self.font_name)
        self.font = pg.font.Font(self.font_path, self.size)

    def set_size(self, size):
        self.size = size
        self.font = pg.font.Font(self.font_path, self.size)

    def get_font_size(self):
        return self.size

    def get_rendered_size(self, text):
        return self.font.size(text)

    def get_height(self):
        return self.font.get_height()

    def set_italic(self, is_on):
        self.font.set_italic(is_on)

    def set_bold(self, is_on):
        if self.font_name == DEFAULT_FONT:
            if is_on:
                self.font_path = os.path.join(FONTS_DIR, DEFAULT_FONT_BOLD)
                self.font = pg.font.Font(self.font_path, self.size)
            else:
                self.font_path = os.path.join(FONTS_DIR, self.font_name)
                self.font = pg.font.Font(self.font_path, self.size)
        else:
            self.font.set_bold(is_on)

    def render(self, text, color):
        return self.font.render(text, True, color)
