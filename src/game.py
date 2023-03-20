# File: game.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

"""Pygame-based graphical frontend for the board.py SOS game."""

from collections.abc import Sequence
import math
import os
import pygame

import board

class Button:
    """A clickable button for Pygame"""

    def __init__(self,
                 rect: Sequence = None,
                 #color: ,
                 text: str = "") -> None:
        self.rect = [0, 0, 1, 1] if rect is None else rect

        self.text = text

    def is_hovered(self, pos: Sequence) -> bool:
        return (self.rect[0] <= pos[0] <= self.rect[0] + self.rect[2] and
                self.rect[1] <= pos[1] <= self.rect[1] + self.rect[3])

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 100, 100), self.rect, 2)
        
        font = pygame.font.SysFont(None, int(self.rect[3]))
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

        res = (window_width, window_height)

        self.surface = pygame.display.set_mode(res)

        self.board = board.Board()

        self.size = min(res)
        self.gap_size = self.size*0.01
        self.tile_size = ((self.size - self.gap_size) / 
                          self.board.num_cols - self.gap_size)

        self.cells = []

        x_offset = (res[0] - self.size)/2 + self.gap_size
        y_offset = (res[1] - self.size)/2 + self.gap_size
        for y in range(self.board.num_rows):
            for x in range(self.board.num_cols):
                tile_x = x_offset + (self.tile_size + self.gap_size)*x
                tile_y = y_offset + (self.tile_size + self.gap_size)*y

                self.cells.append(Button([tile_x, tile_y, 
                                          self.tile_size, self.tile_size]))

        self.state = "play"

    def menu(self) -> None:
        self.surface.fill((0, 0, 0))

    def play(self) -> None:
        self.surface.fill((0, 0, 0))
        for cell in self.cells:
            cell.is_hovered(pygame.mouse.get_pos())
            cell.draw(self.surface)

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

                    case pygame.MOUSEBUTTONUP:
                        pos = pygame.mouse.get_pos()
                        match self.state:
                            case "menu":
                                print("no")

                            case "play":
                                cell_x = math.floor((pos[0] - (self.surface.get_width()  - self.size + self.gap_size)/2) / (self.tile_size + self.gap_size))
                                cell_y = math.floor((pos[1] - (self.surface.get_height() - self.size + self.gap_size)/2) / (self.tile_size + self.gap_size))
                                if (0 <= cell_x < self.board.num_cols and
                                    0 <= cell_y < self.board.num_rows):
                                    
                                    print(cell_x, cell_y)

                                    match e.button:
                                        case 1:
                                            if self.board.make_move(cell_x, cell_y, board.Mark.S):
                                                self.cells[(cell_y * self.board.num_cols) + cell_x].text = "S"
                                        case 3:
                                            if self.board.make_move(cell_x, cell_y, board.Mark.O):
                                                self.cells[(cell_y * self.board.num_cols) + cell_x].text = "O"
                        
            
            match self.state:
                case "menu":
                    self.menu()

                case "play":
                    self.play()

            pygame.display.update()

