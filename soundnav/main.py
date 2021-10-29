"""
Themain idea of this package is to try to provide a better usability for screen reader users while playing this game. As blind users can't see how bird is moving, the idea is based on a sound - the sound should play exactly at the same position where a bird is moving, also the sound should replicate with the pipes when a bird is neext to it.
Note: currently in experimentss - not implemented yet! TBD in Refactor version!
"""

import math
import positionAudio
import time
import pygame

pygame.init()

effect = pygame.mixer.Sound("testas.wav")
channel = pygame.mixer.find_channel(True)

x1: float = 1
y1: float = 1
x2: float = 10
y2: float = 1
direction: float = 0
while True:
    vol = positionAudio.calcVolume((x1, y1), (x2, y2), direction)
    channel.set_volume(*vol)
    if not channel.get_busy():
        channel.play(effect)
    time.sleep(0.3)
    direction = direction + 20 if direction < 360 else 0

    # Commented, here just  so to show that it is possible
    # (x2, y2) = positionAudio.move((x2, y2), math.radians(45.0))
