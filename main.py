import pygame as pg
from data.ui.Text import Text
from data.Settings import Settings
from data.constants import *
from data.GroupEventHandler import GroupEventHandler
from data.group.TextGroup import TextGroup
from data.group.ParticleGroup import ParticleGroup

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.screen.set_alpha(None)
        self.running = True
        self.clock = pg.time.Clock()
        self.bg_color = pg.Color("black")

        self.text_group = TextGroup()
        self.display_only_group = TextGroup()
        self.particle_group = ParticleGroup()
        self.settings = Settings()

        self.text_group.create_text("speed", "Speed: ", bg_color=self.bg_color, max_width=MAX_SPEED,
                                    anchor_left=True, anchor_top=True)
        self.text_group.create_text("barrier_dist", "Barrier distance: ", bg_color=self.bg_color,
                                    max_width=MAX_BARRIER_DIST, anchor_left=True, anchor_top=True)
        self.text_group.create_text("repel_dist", "Repel distance: ", bg_color=self.bg_color,
                                    max_width=MAX_REPEL_DIST, anchor_left=True, anchor_top=True)
        self.text_group.create_text("repel_multiplier", "Repel multiplier: ", bg_color=self.bg_color,
                                    max_width=MAX_REPEL_MULTIPLIER, anchor_left=True, anchor_top=True)
        self.fps_text = Text(text="FPS: ", bg_color=self.bg_color, anchor_bottom=True, anchor_right=True)
        self.particle_text = Text(text=f"Particles: {MAX_PARTICLES:,d}",
                                  bg_color=self.bg_color,
                                  position=(0, SCREEN_SIZE[1]-50),
                                  anchor_left=True,
                                  anchor_bottom=True,
                                  )
        self.display_only_group.add(self.fps_text, self.particle_text)
        self.particle_group.create(MAX_PARTICLES)
        self.particle_group.butterfly_mode = False
        self.text_group.init(self.settings)
        self.display_only_group.update_position(pg.display.get_surface().get_size())
        self.event_handler = GroupEventHandler(self.text_group, self.display_only_group, self.particle_group, self.settings)

    def run(self):
        while self.running:
            if True:  # TODO Freeze screen refresh feature
                self.screen.fill(self.bg_color)
            events = pg.event.get()

            self.event_handler.handle_events(events)
            self.particle_group.handle_collision(self.particle_group.members)

            self.particle_group.update(self.settings)
            self.text_group.update(self.settings)
            self.particle_group.draw(self.screen)
            self.text_group.draw(self.screen)

            self.fps_text.set_value(int(self.clock.get_fps()))
            self.fps_text.update()
            self.fps_text.draw(self.screen)
            self.particle_text.draw(self.screen)

            pg.display.flip()

            self.clock.tick(FPS)


if __name__ == '__main__':
    pg.init()
    display = pg.display.set_mode(SCREEN_SIZE, flags=pg.RESIZABLE | pg.DOUBLEBUF | pg.HWSURFACE)
    pg.display.set_caption("Particle Simulator")

    Game(display).run()
