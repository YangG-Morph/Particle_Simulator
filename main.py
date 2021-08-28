import sys
import pygame as pg
from pygame import gfxdraw  # Unstable avoid
from Text import Text
from Particle import Particle
from Settings import Settings
from CONSTANTS import *

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen.set_alpha(None)
        self.running = True
        self.clock = pg.time.Clock()
        self.bg_color = pg.Color("black")
        self.settings = Settings()
        Text.settings = self.settings # TODO better way to pass settings around, maybe a controller class,
        Particle.settings = self.settings # TODO Class methods! Class variables! then object no longer needed

        self.speed_text = Text("speed", "Speed: ", bg_color=self.bg_color, max_width=MAX_SPEED)
        self.barrier_text = Text("barrier_dist", "Barrier distance: ", bg_color=self.bg_color,
                                 max_width=MAX_BARRIER_DIST)
        self.repel_text = Text("repel_dist", "Repel distance: ", bg_color=self.bg_color, max_width=MAX_REPEL_DIST)
        self.repel_mult_text = Text("repel_multiplier", "Repel multiplier: ", bg_color=self.bg_color,
                                    max_width=MAX_REPEL_MULTIPLIER)
        self.fps_text = Text(text="FPS: ", bg_color=self.bg_color, ignore=True)
        Particle.create(MAX_PARTICLES)

    def handle_events(self, events):
        for event in events:
            if event.type in [pg.QUIT] or event.type in [pg.KEYDOWN] and event.key in [pg.K_ESCAPE]:
                pg.quit()
                sys.exit()
            elif event.type in [pg.KEYUP]:
                for text in Text.all_text:
                    text.keying = False
            elif event.type in [pg.KEYDOWN]:
                text = [t for t in Text.all_text if t.input_mode]
                if event.unicode.isdigit() and text:
                    text = text[0]
                    if text.input_started:
                        text.value_str = event.unicode
                        text.input_started = False
                    else:
                        text.value_str += event.unicode
                    text.rendered_text = text.font.render(f"{text.orig_text}{text.value_str}", True, text.fg_color)

        mouse_pos = pg.mouse.get_pos()
        mouse_buttons = pg.mouse.get_pressed(num_buttons=3)
        keys = pg.key.get_pressed()

        Text.group_events(mouse_pos, mouse_buttons, keys) # TODO Event Controller to handle events between classes
        Particle.group_events(mouse_pos, mouse_buttons)  # TODO pass in dt?

    def run(self):
        while self.running:
            if True:
                self.screen.fill(self.bg_color)
            self.handle_events(pg.event.get())

            Particle.group_draw(self.screen)
            Text.group_draw(self.screen)

            self.fps_text.set_value(int(self.clock.get_fps()))
            pg.display.update()

            self.clock.tick(FPS)

if __name__ == '__main__':
    pg.init()
    display = pg.display.set_mode(SCREEN_SIZE, flags=pg.RESIZABLE | pg.DOUBLEBUF | pg.HWSURFACE)
    pg.display.set_caption("Particle Simulator")

    Game(display).run()
