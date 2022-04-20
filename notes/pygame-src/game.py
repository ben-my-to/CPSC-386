#!/usr/bin/env python3


import pygame
from itertools import product
from math import isclose


class Circle:
    def __init__(self, x, y, radius, velocity):
        self._center = pygame.Vector2(x, y)
        self._radius = radius
        self._velocity = velocity

    @property
    def center(self):
        return self._center

    @property
    def radius(self):
        return self._radius

    @property
    def velocity(self):
        return self._velocity

    @property
    def bound(self):
        return sum(
            list(
                map(lambda c: [c - self._radius, c + self._radius], [self._center.x, self._center.y])
            ), []
        )


    def is_interior(self, field=None):
        print(self.bound, field.bound)
        ax_min, ax_max, ay_min, ay_max = self.bound
        bx_min, bx_max, by_min, by_max = field.bound

        return ax_min >= bx_min and ax_min <= bx_max and \
               ax_max >= bx_min and ax_max <= bx_max and \
               ay_min >= by_min and ay_min <= by_max and \
               ay_max >= by_min and ay_max <= by_max

        #return all(l[0] > l[1] if pos % 2 else l[0] < l[1] \
        #           for pos, l in enumerate(zip(self.bound, field.bound)))


    def has_collided(self, field=None):
        vec = self.center - field.center
        dist = pygame.math.Vector2.magnitude(vec)
        return dist <= self.radius + field.radius


    def make_bounce(self):
        pass


def main():
    pygame.display.init()
    pygame.display.set_mode(size=(800, 800))
    pygame.display.set_caption('Hello World')

    a = Circle(10.0, 5.0, radius=5.0, velocity=2.0)
    b = Circle(20.0, 5.0, radius=10.0, velocity=2.0)

    print(a.is_interior(b))
    print(a.has_collided(b))
    print(isclose(0.2 * 3, 0.6))

    pygame.display.quit()


if __name__ == '__main__':
    main()
