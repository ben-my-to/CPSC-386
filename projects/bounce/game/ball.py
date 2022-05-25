# Jason Duong
# CPSC 386-03
# 2022-05-09
# reddkingdom@csu.fullerton.edu
# @duong-jason
#
# Lab 05-00
#
# A Ball Class
#


"""A Ball class for the bouncing ball demo."""


from random import randint, uniform, choice
import os.path
import pygame
from game import rgbcolors


def random_velocity(min_val=1, max_val=3):
    """Generate a random velocity in a plane, return it as a Vector2"""
    return pygame.Vector2(
        choice([-1, 1]) * uniform(min_val, max_val),
        choice([-1, 1]) * uniform(min_val, max_val),
    )


def random_color():
    """Return a random color."""
    return pygame.Color(randint(1, 255), randint(1, 255), randint(1, 255))


class Circle:
    """Class representing a circle with a bounding rect."""

    def __init__(self, center_x, center_y, radius=25):
        self._center = pygame.Vector2(center_x, center_y)
        self._radius = radius

    @property
    def center(self):
        """Return the circle's center."""
        return self._center

    @property
    def radius(self):
        """Return the circle's radius"""
        return self._radius

    @property
    def rect(self):
        """Return bounding Rect; calculate it and create a new Rect instance"""
        return pygame.Rect(
            self._center.x - self._radius,
            self._center.y - self._radius,
            self._radius * 2,
            self._radius * 2,
        )

    @property
    def width(self):
        """Return the width of the bounding box the circle is in."""
        return self.rect.width

    @property
    def height(self):
        """Return the height of the bounding box the circle is in."""
        return self.rect.height

    def get_rect(self):
        """Return the left, right, top, bottom of a Circle object"""
        return [(c - self.radius, c + self.radius) for c in self._center]

    def squared_distance_from(self, other_center):
        """Squared distance from self to other circle."""
        return (other_center - self._center).square_length()

    def distance_from(self, other_center):
        """Distance from self to other circle"""
        return (other_center - self._center).length()

    def move_ip(self, x_coord=0, y_coord=0):
        """Move circle in place, update the circle's center"""
        self._center += pygame.Vector2(x_coord, y_coord)

    def move(self, x_coord=0, y_coord=0):
        """Move circle, return a new Circle instance"""
        center = self._center + pygame.Vector2(x_coord, y_coord)
        return Circle(*center, self._radius)

    def stay_in_bounds(self, x_min, y_min, x_max, y_max):
        """Update the position of the circle so that it remains within
        the rectangle defined by x_min, x_max, y_min, y_max."""
        right, bottom = [item[1] for item in self.get_rect()]

        self.move_ip(x_coord=max(x_min, self._radius - self._center.x))
        self.move_ip(y_coord=max(y_min, self._radius - self._center.y))
        self.move_ip(x_coord=-max(0, right - x_max))
        self.move_ip(y_coord=-max(0, bottom - y_max))


class Ball:
    """A class representing a moving ball."""

    default_radius = 25

    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, 'data')
    # Feel free to change the sounds to something else.
    # Make sure you have permssion to use the sound effect file and document
    # where you retrieved this file, who is the author, and the terms of
    # the license.
    bounce_sound = os.path.join(data_dir, 'Boing.aiff')
    reflect_sound = os.path.join(data_dir, 'Monkey.aiff')

    def __init__(self, name, center_x, center_y, sound_on=True):
        """Initialize a bouncing ball."""
        self._name = name
        self._circle = Circle(center_x, center_y, Ball.default_radius)
        self._color = random_color()
        self._velocity = random_velocity()
        self._sound_on = sound_on
        self._bounce_count = randint(5, 10)
        self._is_alive = True
        self._draw_text = False
        font = pygame.font.SysFont(None, Ball.default_radius)
        self._name_text = font.render(str(self._name), True, rgbcolors.black)
        try:
            self._bounce_sound = pygame.mixer.Sound(Ball.bounce_sound)
            self._bounce_channel = pygame.mixer.Channel(2)
        except pygame.error as pygame_error:
            print(f'Cannot open {Ball.bounce_sound}')
            raise SystemExit(1) from pygame_error
        try:
            self._reflect_sound = pygame.mixer.Sound(Ball.reflect_sound)
            self._reflect_channel = pygame.mixer.Channel(3)
        except pygame.error as pygame_error:
            print(f'Cannot open {Ball.reflect_sound}')
            raise SystemExit(1) from pygame_error

    def draw(self, surface):
        """Draw the circle to the surface."""
        pygame.draw.circle(surface, self.color, self.center, self.radius)
        if self._draw_text:
            surface.blit(
                self._name_text,
                self._name_text.get_rect(center=self._circle.center),
            )

    def wall_reflect(self, x_min, y_min, x_max, y_max):
        """Reflect ball off of a wall, play sound if the sound flag is on."""
        (left, right), (top, bottom) = self.circle.get_rect()

        if left <= x_min or right >= x_max:
            self._velocity.x *= -1
        if top <= y_min or bottom >= y_max:
            self._velocity.y *= -1

        if self._sound_on:
            self._reflect_sound.play()

    def separate_from(self, other_ball, rect):
        """Separate a ball from the other ball (no overlapping)"""
        delta = (self.radius + other_ball.radius) - (
            self._circle.distance_from(other_ball.center)
        )
        half = max(1.0, delta / 2.0)

        factor = 1.0 if other_ball.is_alive else 2.0
        self._circle.move_ip(*(-self._velocity * half * factor))

        factor = 1.0 if self._is_alive else 2.0
        other_ball.circle.move_ip(*(-other_ball.velocity * half * factor))

    def collide_with(self, other_ball):
        """Return true if self collides with other_ball."""
        return (
            self._circle.distance_from(other_ball.center)
            <= self._circle.radius + other_ball.radius
        )

    def bounce(self, other_ball):
        """Bounce the ball off of another ball,
        play a sound if the ball is no alive."""
        normal = other_ball.center - self.center
        self._velocity = self._velocity.reflect(normal)
        if self._name:
            self.age_ball()

    @property
    def name(self):
        """Return the ball's name."""
        return self._name

    @name.setter
    def set_name(self, name):
        """Set the ball's name"""
        self._name = name

    @property
    def rect(self):
        """Return the ball's rect."""
        return self._circle.rect

    @property
    def circle(self):
        """Return the ball's circle."""
        return self._circle

    @property
    def center(self):
        """Return the ball's center."""
        return self._circle.center

    @property
    def radius(self):
        """Return the ball's radius"""
        return self._circle.radius

    @property
    def color(self):
        """Return the color of the ball."""
        return self._color

    @color.setter
    def color(self, value):
        """Set the ball's color"""
        self._color = value

    @property
    def velocity(self):
        """Return the velocity of the ball."""
        return self._velocity

    @property
    def is_alive(self):
        """Return true if the ball is still alive."""
        return self._is_alive

    @property
    def bounce_count(self):
        """Return the ball's bounce count."""
        return self._bounce_count

    @property
    def sound_on(self):
        """Return true if the sound is on."""
        return self._sound_on

    def bounce_sound_play(self):
        """Return the bounce sound effect."""
        return self._bounce_sound.play()

    def toggle_draw_text(self):
        """Toggle the debugging text where each circle's name is drawn."""
        self._draw_text = not self._draw_text

    def toggle_sound(self):
        """Turn on/off the sound effects."""
        self._sound_on = not self._sound_on

    def too_close(self, x_coord, y_coord, min_dist=55):
        """Is the ball too close to some point by some min_dist?"""
        point = pygame.Vector2(x_coord, y_coord)
        return self._circle.distance_from(point) <= min_dist

    def set_velocity(self, x_coord, y_coord):
        """Set the ball's velocity."""
        self._velocity = pygame.Vector2(x_coord, y_coord)

    def age_ball(self):
        """decreases the ball's life by a factor of one"""
        self._bounce_count -= 1

    def halt(self):
        """Stop the ball from moving."""
        self._is_alive = False
        self._color = rgbcolors.white
        self.set_velocity(0, 0)

    def update(self):
        """Update the ball's position"""
        self._circle.move_ip(*self._velocity)

    def __str__(self):
        """Ball stringify."""
        return f'Name: {self._name} \
            Rect: {self.rect} \
            Center: {self.center} \
            Velocity: {self._velocity} \
            Color: {self._color}'
