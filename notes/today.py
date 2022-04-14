#!/usr/bin/env python3

"""

  ---------------------------------
  | Title Scene -> Bouncing Scene |
  ---------------------------------

FRAMEWORK:
    - sequence of scenes

EDGE:
    -

BOTH:
    - share a Graphics Context, Clock, Human Input, Audio
    - behavior

TITLE:
    - Message, font, colors, background, music track

BOUNCING:
    - balls, music, sfx, color

"""


if __name__ == '__main__':
    if len(sys.argv) > 1:
        n_balls = int(sys.argv[1])
    else:
        n_balls = 5
