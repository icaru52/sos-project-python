# File: pygame_helper.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

from collections.abc import Sequence
import math
import pygame

def distance(p1: Sequence[float], p2: Sequence[float]) -> float:
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

#def distance(p1: Sequence[float], p2: Sequence[float]) -> float:
#    return math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))

def midpoint(p1: Sequence[float], p2: Sequence[float]) -> tuple[float]:
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

#def midpoint(p1: Sequence[float], p2: Sequence[float]) -> tuple[float]:
#    return tuple(map(lambda a, b: (a + b) / 2, p1, p2))

def angle_between(p1: Sequence, p2: Sequence) -> float:
    return math.atan2(p1[1] - p2[1], p1[0] - p2[0])

def draw_nice_line(surface: pygame.Surface,
                   color: Sequence[int],
                   start_pos: Sequence[float],
                   end_pos: Sequence[float],
                   width: float = 2) -> pygame.Rect:

    if len(start_pos) != 2 or len(end_pos) != 2:
        #any(not isinstance(x, int) for x in start_pos + end_pos)):
        raise TypeError("Points must be two-dimensional")

    line = pygame.Surface([distance(start_pos, end_pos), width])

    line.set_colorkey((0, 0, 0))
    line.fill(color)

    # must multiply by -1 because atan assumes up is positive, 
    # while in pygame down is positive
    angle = math.degrees(angle_between(start_pos, end_pos)) * (-1)
    line = pygame.transform.rotate(line, angle)
    
    rect = line.get_rect(center = midpoint(start_pos, end_pos))

    surface.blit(line, rect)

    pygame.draw.circle(surface, color, start_pos, width/2)
    pygame.draw.circle(surface, color, end_pos,   width/2)

    return rect

def rect_center(center: Sequence[float], 
                size: Sequence[float]) -> pygame.Rect:
    return pygame.Rect((center[0] - size[0]/2, 
                        center[1] - size[1]/2), size)



