
class Group(list):
    def __init__(self, *members):
        super().__init__(*members)
        self.members = [member for member in members]
        self.clicked = False

    def get(self, member_value):
        members = [member for member in self.members if getattr(member, member_value) is not None]
        if members:
            return members

    def append(self, *members):
        for member in members:
            self.members.append(member)

    def events(self, *inputs):
        raise NotImplementedError

    def update(self, settings):
        [member.update(settings) for member in self.members]

    def draw(self, surface):
        [member.draw(surface) for member in self.members]





