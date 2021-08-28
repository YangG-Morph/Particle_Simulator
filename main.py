import pygame as pg
from ui.Text import Text
from data.Settings import Settings
from data.constants import *
from data.EventHandler import EventHandler
from group.TextGroup import TextGroup
from group.ParticleGroup import ParticleGroup


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen.set_alpha(None)
        self.running = True
        self.clock = pg.time.Clock()
        self.bg_color = pg.Color("black")

        self.text_group = TextGroup()
        self.particle_group = ParticleGroup()
        self.settings = Settings()

        self.text_group.create("speed", "Speed: ", bg_color=self.bg_color, max_width=MAX_SPEED)
        self.text_group.create("barrier_dist", "Barrier distance: ", bg_color=self.bg_color,
                               max_width=MAX_BARRIER_DIST)
        self.text_group.create("repel_dist", "Repel distance: ", bg_color=self.bg_color, max_width=MAX_REPEL_DIST)
        self.text_group.create("repel_multiplier", "Repel multiplier: ", bg_color=self.bg_color,
                               max_width=MAX_REPEL_MULTIPLIER)
        self.fps_text = Text(text="FPS: ", bg_color=self.bg_color, ignore=True)

        self.particle_group.create(MAX_PARTICLES)
        self.text_group.init(self.settings)
        self.fps_text.init(settings=None, idx=4)
        self.event_handler = EventHandler(self.text_group, self.particle_group, self.settings)

    def run(self):
        while self.running:
            if True:  # TODO Freeze screen refresh feature
                self.screen.fill(self.bg_color)

            self.event_handler.handle_events(pg.event.get())

            self.particle_group.update(self.settings)
            self.text_group.update(self.settings)
            self.particle_group.draw(self.screen)
            self.text_group.draw(self.screen)

            self.fps_text.set_value(int(self.clock.get_fps()))
            self.fps_text.update()
            self.fps_text.draw(self.screen)

            pg.display.flip()

            self.clock.tick(FPS)


if __name__ == '__main__':
    pg.init()
    display = pg.display.set_mode(SCREEN_SIZE, flags=pg.RESIZABLE | pg.DOUBLEBUF | pg.HWSURFACE)
    pg.display.set_caption("Particle Simulator")

    Game(display).run()
