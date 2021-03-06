import sys
import pygame as pg
from data import utils
from data.constants import *

class GroupEventHandler:
    def __init__(self, text_group, display_only_group, particle_group, settings):
        self.text_group = text_group
        self.display_only_group = display_only_group
        self.particle_group = particle_group
        self.settings = settings

    def handle_particle(self, mouse_pressed):
        left_button, middle_button, right_button = mouse_pressed

        if left_button and not self.particle_group.clicked and not self.text_group.clicked:
            self.particle_group.clicked = True
            self.particle_group.set_movement(self.settings)
        elif middle_button and not self.particle_group.clicked:
            self.particle_group.clicked = True
            setattr(self.settings, "speed", utils.randint(0, MAX_SPEED))
            setattr(self.settings, "barrier_dist", utils.randint(0, MAX_BARRIER_DIST))
            setattr(self.settings, "repel_dist", utils.randint(0, MAX_MOUSE_DIST))
            setattr(self.settings, "mouse_repel_dist", utils.randint(0, MAX_REPEL_DIST))
            self.text_group.set_str_value(self.settings)
        elif right_button and not self.particle_group.clicked and not self.text_group.clicked:
            self.particle_group.time_frozen = True
        elif not middle_button and not right_button:
            self.particle_group.clicked = False
            self.particle_group.time_frozen = False

    def handle_text(self, mouse_pos, mouse_pressed):
        left_button, middle_button, right_button = mouse_pressed
        collided = self.text_group.check_collision(mouse_pos)
        self.text_group.set_hover(collided)

        if left_button and collided:
            self.text_group.clicked = True
            collided.set_focus()
            for t in self.text_group.members:
                if t != collided:
                    t.reset(self.settings)
        elif left_button or middle_button and not collided:
            self.text_group.reset(self.settings)
        elif right_button and collided and not self.text_group.clicked and not self.particle_group.time_frozen:
            self.text_group.clicked = True
            collided.prev_collided = True
            collided.value = getattr(self.settings, collided.name)
            collided.start_value = getattr(self.settings, collided.name)
            collided.slider.start_pos = mouse_pos
            collided.slider.update(size=(collided.value, 0))
        elif right_button and self.text_group.had_collided():
            text = self.text_group.get_prev_collide()
            movement = (mouse_pos[0] - text.slider.start_pos[0]) + (text.slider.start_pos[1] - mouse_pos[1])
            setattr(self.settings, text.name, movement + text.start_value)
            text.value = getattr(self.settings, text.name)
            text.slider.update(size=(text.value, 0))
            text.set_pos((text.slider.max_width + text.padding_left, text.position[1]))
        elif right_button and not self.text_group.had_collided():
            self.text_group.reset(self.settings)

    def handle_events(self, events):
        for event in events:
            if event.type in [pg.QUIT] or event.type in [pg.KEYDOWN] and event.key in [pg.K_ESCAPE]:
                pg.quit()
                sys.exit()
            elif event.type in [pg.KEYUP]:
                for text in self.text_group.members:
                    text.keying = False
            elif event.type in [pg.KEYDOWN]:
                text_clicked = [t for t in self.text_group.members if t.input_mode]
                if text_clicked:
                    text = text_clicked[0]
                    if event.unicode.isdigit():
                        if text.input_started:
                            text.str_value = event.unicode
                            text.input_started = False
                        else:
                            text.str_value += event.unicode
                    if event.key in [pg.K_BACKSPACE]:
                        text.keying = True
                        text.input_started = False
                        text.str_value = text.str_value[:-1]
                    elif event.key in [pg.K_RETURN, pg.K_KP_ENTER]:
                        text.reset(self.settings)
                    text.rendered_text = text.font.render(f"{text.orig_text}{text.str_value}", text.fg_color)
            elif event.type in [pg.MOUSEBUTTONUP]:
                self.text_group.clicked = False
                if self.text_group.had_collided():
                    self.text_group.set_str_value(self.settings)
                    self.text_group.reset(self.settings)
            elif event.type in [pg.WINDOWRESIZED]:
                screen_size = pg.display.get_surface().get_size()
                self.text_group.update_position(screen_size)
                self.display_only_group.update_position(screen_size)

        mouse_pos = pg.mouse.get_pos()
        mouse_buttons = pg.mouse.get_pressed(num_buttons=3)

        self.handle_text(mouse_pos, mouse_buttons)
        self.handle_particle(mouse_buttons)
        self.particle_group.events(mouse_pos, self.settings, mouse_buttons)




