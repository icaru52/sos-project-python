# File: game.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

"""Pygame-based graphical frontend for the board.py SOS game."""

from collections.abc import Sequence
import os
import pygame

import board

class Button:
    """A clickable button for Pygame"""

    def __init__(self, rect: Sequence = None, text:str = "") -> None:
        self.rect = [0, 0, 1, 1] if rect is None else rect

        self.text = text

    def is_hovered(self, pos: Sequence) -> bool:
        return (self.rect[0] <= pos[0] <= self.rect[2] and
                self.rect[1] <= pos[1] <= self.rect[3])

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 100, 100), self.rect, 2)
        text = font.render(self.text, 1, (255, 255, 255))
        surface.blit(text,
                     (self.rect[0] + self.rect[2] / 2 - text.get_width()  / 2,
                      self.rect[1] + self.rect[3] / 2 - text.get_height() / 2))


class Game:
    """"""

    def __init__(self,
                 window_width:  int = 512,
                 window_height: int = 512) -> None:

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        self.res = (window_width, window_height)

        self.size = min(self.res)

        self.surface = pygame.display.set_mode(self.res)

        board = Board()

    #def menu(self):
    #    self.surface.fill((0, 0, 0))

    def play(self) -> None:
        self.surface.fill((0, 0, 0))
        for i in range(board.num_rows):
            for j in range(board.num_cols):
                tile_x = (self.res[0] - self.size)/2 + gap_size + (tile_size + gap_size)*j
                tile_y = (self.res[1] - self.size)/2 + gap_size + (tile_size + gap_size)*i
                pygame.draw.rect(self.surface,
                                 (255, 100, 100),
                                 [tile_x, tile_y, tile_size, tile_size],
                                 2)

    def start(self) -> None:
        running = True

        while running:
            for e in pygame.event.get():
                match e.type:
                    case pygame.QUIT:
                        running = False

                    case pygame.KEYDOWN:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                            running = False

            pygame.display.update()

