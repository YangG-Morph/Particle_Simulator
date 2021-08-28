import math
import random


def clamp(value, min, max):
    return min if value < min else max if value > max else value

def sub_pos(end_pos, start_pos):
    return end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]

def hypotenuse(ab):
    return math.hypot(ab[0], ab[1])

def normalize(ab, magnitude):
    if magnitude > 0:
        return ab[0] / magnitude, ab[1] / magnitude
    return 0, 0

def randint(min, max, size=1):
    """ Generate random integer number inclusively """
    width = max - min + 1
    if size > 1:
        return [math.floor(random.random() * width + min) for _ in range(size)]
    return math.floor(random.random() * width + min)

def randfloat(min, max, size=1):
    """ Generate random float number excludes max"""
    width = max - min
    if size > 1:
        return [random.random() * width + min for _ in range(size)]
    return random.random() * width + min

def rand_uniform(min, max, size=1):
    if size > 1:
        return [random.uniform(min, max) for _ in range(size)]
    return random.uniform(min, max)