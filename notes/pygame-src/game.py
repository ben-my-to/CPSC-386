#!/usr/bin/env python3


import pygame
from math import isclose


class Circle:
    def __init__(self, x, y, radius, velocity):
        self._center = pygame.Vector2(x, y)
        self._radius = radius
        self._velocity = velocity

    @property
    def center(self):
        return (self._center.x, self._center.y)

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


    def has_collided(self, field=None):
        vec = self.center - field.center
        dist = pygame.math.Vector2.magnitude(vec)
        return dist <= self.radius + field.radius


    def make_bounce(self):
        pass


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Bouncing Balls')
    white = (255, 255, 255)

    a = Circle(400.0, 400.0, radius=100.0, velocity=2.0)
    b = Circle(600.0, 300.0, radius=100.0, velocity=2.0)

    pygame.draw.circle(screen, white, a.center, a.radius)
    pygame.draw.circle(screen, white, b.center, b.radius)


    pygame.display.update()
    pygame.time.wait(3000)

    pygame.quit()

    #print(a.is_interior(b))
    #print(a.has_collided(b))
    #print(isclose(0.2 * 3, 0.6))


if __name__ == '__main__':
    main()
