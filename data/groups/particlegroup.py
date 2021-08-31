from data.groups.group import Group
from data.particle import Particle

class ParticleGroup(Group):
    def __init__(self, *members):
        super().__init__(*members)
        self.members = [member for member in members]
        self.clicked = False
        self.time_frozen = False
        self.butterfly_mode = False

    def events(self, mouse_pos, settings, mouse_buttons):
        [particle.events(mouse_pos, settings, self.time_frozen, mouse_buttons) for particle in self.members]

    def set_movement(self, settings):
        [particle.set_movement(settings) for particle in self.members]

    def handle_collision(self, other_particles):
        if self.butterfly_mode:
            [particle.handle_collision(other_particles) for particle in self.members]

    def update(self, direction, multiplier=1):
        pass

    def create(self, amount):
        for _ in range(amount):
            self.append(Particle.create())







