#!/usr/bin/env python3


import pygame
from math import isclose


class Circle:
    def __init__(self, x, y, radius):
        self._center = pygame.Vector2(x, y)
        self._radius = radius

    @property
    def center(self):
        return self._center

    @property
    def radius(self):
        return self._radius

    def has_collide(self, other_circle):
        v = self.center - other_circle.center
        return len(d) <= self.radius + other_circle.radius



print(isclose(0.2 * 3, 0.6))

























