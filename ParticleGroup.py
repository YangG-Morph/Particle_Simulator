from Group import Group
from Particle import Particle

class ParticleGroup(Group):
    def __init__(self, *members):
        super().__init__(*members)
        self.members = [member for member in members]
        self.clicked = False
        self.time_frozen = False

    def events(self, mouse_pos, settings):
        [particle.events(mouse_pos, settings, self.time_frozen) for particle in self.members]

    def set_movement(self, settings):
        [particle.set_movement(settings) for particle in self.members]

    def collision(self, other_rects):
        [particle.handle_collision(other_rects) for particle in self.members]

    def create(self, amount):
        for _ in range(amount):
            self.append(Particle.create())






