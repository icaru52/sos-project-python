# File: game.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

"""Pygame-based graphical frontend for the board.py SOS game."""

from collections.abc import Sequence
import math
import os
import pygame

import board

def distance(p1: Sequence, p2: Sequence) -> float:
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

#def distance(p1: Sequence, p2: Sequence) -> float:
#    return math.sqrt(sum((a - b)**2 for a, b in zip(p1, p2)))

def midpoint(p1: Sequence, p2: Sequence) -> tuple:
    return ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)

#def midpoint(p1: Sequence, p2: Sequence) -> tuple:
#    return tuple(map(lambda a, b: (a + b) / 2, p1, p2))

def angle_between(p1: Sequence, p2: Sequence) -> float:
    return math.atan2(p1[1] - p2[1], p1[0] - p2[0])

def draw_nice_line(surface: pygame.Surface,
                   color: Sequence,
                   start_pos: Sequence,
                   end_pos: Sequence,
                   width: float) -> pygame.Rect:

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

    return rect


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
                     (self.rect[0] + (self.rect[2] - text.get_size()[0]) / 2,
                      self.rect[1] + (self.rect[3] - text.get_size()[1]) / 2))

    #def handle_clicks():
    #    


class Game:
    """GUI for displaying and interacting with SOS game board"""

    def __init__(self,
                 window_width:  int = 512,
                 window_height: int = 512) -> None:

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        self.surface = pygame.display.set_mode((window_width, window_height))

        self.board = board.Board()

        self.size = min(self.surface.get_size())
        self.gap_size = self.size*0.01
        self.cell_size = ((self.size - self.gap_size) /
                          self.board.num_cols - self.gap_size)

        self.cells = []

        x_offset = (self.surface.get_size()[0] - self.size)/2 + self.gap_size
        y_offset = (self.surface.get_size()[1] - self.size)/2 + self.gap_size
        for y in range(self.board.num_rows):
            for x in range(self.board.num_cols):
                cell_x = x_offset + (self.cell_size + self.gap_size)*x
                cell_y = y_offset + (self.cell_size + self.gap_size)*y

                self.cells.append(Button([cell_x, cell_y,
                                          self.cell_size, self.cell_size]))

        self.state = "play"

    #def resize(self, width: int, height: int) -> None:
    #    

    def draw_menu(self) -> None:
        self.surface.fill((0, 0, 0))
        print("menu not implemented")

    def draw_board(self) -> None:
        self.surface.fill((0, 0, 0))
        for cell in self.cells:
            cell.is_hovered(pygame.mouse.get_pos())
            cell.draw(self.surface)
        self.draw_sos_list()

    def new_draw_board(self) -> None:
        self.surface.fill((0, 0, 0))

        x_offset = (self.surface.get_size()[0] - self.size)/2 + self.gap_size
        y_offset = (self.surface.get_size()[1] - self.size)/2 + self.gap_size
        for row in range(self.board.num_rows):
            for col in range(self.board.num_cols):
            
                cell_x = x_offset + (self.cell_size + self.gap_size)*col
                cell_y = y_offset + (self.cell_size + self.gap_size)*row

                pygame.draw.rect(self.surface,
                                 (255, 100, 100),
                                 [cell_x, cell_y,
                                  self.cell_size, self.cell_size],
                                 2)

                font = pygame.font.SysFont(None, int(self.cell_size))
                text = font.render(self.board.get_char(col, row), 1, (255, 255, 255))
                self.surface.blit(text,
                                  (cell_x + (self.cell_size - text.get_size()[0]) / 2,
                                   cell_y + (self.cell_size - text.get_size()[1]) / 2))
        self.draw_sos_list()

    def draw_sos_list(self) -> None:
        for sos in self.board.sos_list:
            line_color = pygame.Color(0)
            line_color.hsla = (self.board.players[sos.player_id].hue, 100, 50, 100)
            #pygame.draw.line(self.surface, 
            draw_nice_line(self.surface,
                           line_color, 
                           [(i + 0.5) * self.cell_size + (i + 1) * self.gap_size for i in sos.p1], 
                           [(i + 0.5) * self.cell_size + (i + 1) * self.gap_size for i in sos.p2],
                           math.ceil(self.size * 0.01))

    def menu_clicks(self, pos: Sequence, button: int = 1) -> None:
        print("menu click handling not implemented")

    def cell_indices_to_pos(self, indices: Sequence) -> list:
        indices = [None] * len(indices)

        for idx, index in enumerate(indices):
            indices[idx] = 0 #TODO: fix this

        return indices

    def pos_to_cell_indices(self, pos: Sequence) -> list:
        indices = [None] * len(pos)

        for idx, coord in enumerate(pos):
            indices[idx] = math.floor((pos[idx] - (self.surface.get_size()[idx] - self.size + self.gap_size)/2) / (self.cell_size + self.gap_size))

        return indices

    def board_clicks(self, pos: Sequence, button: int = 1) -> None:
        cell_col, cell_row = self.pos_to_cell_indices(pos)

        if (0 <= cell_col < self.board.num_cols and
            0 <= cell_row < self.board.num_rows):

            match button:
                case 1:
                    self.board.make_move(cell_col, cell_row, board.Mark.S)
                        #self.cells[(cell_row * self.board.num_cols) + cell_col].text = "S"
                case 3:
                    self.board.make_move(cell_col, cell_row, board.Mark.O)
                        #self.cells[(cell_row * self.board.num_cols) + cell_col].text = "O"

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
                                self.menu_clicks(pos, e.button)

                            case "play":
                                self.board_clicks(pos, e.button)

            match self.state:
                case "menu":
                    self.draw_menu()

                case "play":
                    self.new_draw_board()

            pygame.display.update()

