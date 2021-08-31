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

def randint(min, max):
    """ Generate random integer number inclusively """
    width = max - min + 1
    return math.floor(random.random() * width + min)

def randint_sample(min, max, size):
    """ Generate sample of random integers number inclusively """
    width = max - min + 1
    return [math.floor(random.random() * width + min) for _ in range(size)]

def randfloat(min, max):
    """ Generate random float number excludes max """
    width = max - min
    return random.random() * width + min

def randfloat_sample(min, max, size):
    """ Generate sample of random float numbers excludes max """
    width = max - min
    return [random.random() * width + min for _ in range(size)]


