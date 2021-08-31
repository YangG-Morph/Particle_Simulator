from data import utils
from data.constants import *

class Settings:
    def __init__(self):
        self._speed = 10
        self._barrier_dist = 20
        self._repel_dist = 2
        self._mouse_repel_dist = 10

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = utils.clamp(value, 0, MAX_SPEED)

    @property
    def barrier_dist(self):
        return self._barrier_dist

    @barrier_dist.setter
    def barrier_dist(self, value):
        self._barrier_dist = utils.clamp(value, 0, MAX_BARRIER_DIST)

    @property
    def repel_dist(self):
        return self._repel_dist

    @repel_dist.setter
    def repel_dist(self, value):
        self._repel_dist = utils.clamp(value, 0, MAX_REPEL_DIST)

    @property
    def mouse_repel_dist(self):
        return self._mouse_repel_dist

    @mouse_repel_dist.setter
    def mouse_repel_dist(self, value):
        self._mouse_repel_dist = utils.clamp(value, 0, MAX_MOUSE_DIST)



    def __str__(self):
        return f"speed: {self._speed}\n" \
               f"barrier dist: {self._barrier_dist}\n" \
               f"repel dist: {self._mouse_repel_dist}\n" \
               f"repel mult: {self._repel_dist}\n"

