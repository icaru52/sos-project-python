# File: newgame.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

"""Pygame-based graphical frontend for the board.py SOS game."""

from collections.abc import Sequence
import math
import os
import pygame

import ui
import board

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
        gap_size = self.size*0.01
        cell_size = ((self.size - gap_size) /
                      self.board.num_cols - gap_size)

        cell_stride = cell_size + gap_size

        board_offset = ((self.surface.get_size()[0] - self.size)/2 + gap_size,
                        (self.surface.get_size()[1] - self.size)/2 + gap_size)

        self.board_ui = ui.UI()

        for y in range(self.board.num_rows):
            for x in range(self.board.num_cols):
                cell_x = board_offset[0] + cell_stride * x
                cell_y = board_offset[1] + cell_stride * y

                self.board_ui.add(ui.Button(pygame.Rect(cell_x, cell_y,
                                                        cell_size, cell_size),
                                            {"x": x, "y": y},
                                            self.board.get_char(x, y),
                                            False,
                                            pygame.Color(100),
                                            pygame.Color(150),
                                            pygame.Color("white")))

        self.menu_ui = ui.UI()

        row_y = self.surface.get_height() * 1/4

        # size down
        rect = pygame.Rect(0, row_y, cell_size, cell_size)
        rect.centerx = self.surface.get_width() * 1/3
        self.menu_ui.add(ui.Button(rect,
                                   "size_down",
                                   "-",
                                   False,
                                   pygame.Color(100),
                                   pygame.Color(150),
                                   pygame.Color("white")))

        # size up
        rect = pygame.Rect(0, row_y, cell_size, cell_size)
        rect.centerx = self.surface.get_width() * 2/3
        self.menu_ui.add(ui.Button(rect,
                                   "size_up",
                                   "+",
                                   False,
                                   pygame.Color(100),
                                   pygame.Color(150),
                                   pygame.Color("white")))


 
        row_y = self.surface.get_height() * 1/2

        # simple
        rect = pygame.Rect(0, row_y, 300, cell_size)
        rect.centerx = self.surface.get_width() * 1/4
        self.menu_ui.add(ui.Button(rect,
                                   "simple_game",
                                   "Simple Game",
                                   True,
                                   pygame.Color(100),
                                   pygame.Color(150),
                                   pygame.Color("white")))


        
        # general
        rect = pygame.Rect(0, row_y, 300, cell_size)
        rect.centerx = self.surface.get_width() * 3/4
        self.menu_ui.add(ui.Button(rect,
                                   "general_game",
                                   "General Game",
                                   False,
                                   pygame.Color(100),
                                   pygame.Color(150),
                                   pygame.Color("white")))




        row_y = self.surface.get_height() * 3/4

        # start
        rect = pygame.Rect(0, row_y, 200, cell_size)
        rect.centerx = self.surface.get_rect().centerx
        draw_button(self.surface, 
                   (100, 100, 100), 
                   (150, 150, 150), 
                   "START", 
                   rect)
        self.menu_ui.add(ui.Button(rect,
                                   "start_game",
                                   "START",
                                   False,
                                   pygame.Color(100),
                                   pygame.Color(150),
                                   pygame.Color("white")))
    

        self.state = "menu"

    #def resize(self, width: int, height: int) -> None:
    #    

    def draw_menu(self) -> None:
        self.surface.fill((50, 50, 50))
        self.menu_ui.draw(self.surface)
        
    def draw_board(self) -> None:
        self.surface.fill((50, 50, 50))
        self.board_ui.draw(self.surface)
        self.draw_sos_list()

    def draw_end(self) -> None:
        self.draw_board()

        gray_rect = pygame.Surface(self.surface.get_size())
        gray_rect.set_alpha(128)
        gray_rect.fill((128, 128, 128))
        self.surface.blit(gray_rect, (0, 0))

        rect = pygame.Rect(0, 0, 200, 200)
        rect.center = self.surface.get_rect().center
        draw_button(self.surface, (0, 0, 0), (50, 50, 50), "end", rect)

    def draw_sos_list(self) -> None:
        for sos in self.board.sos_list:
            line_color = pygame.Color(0)
            line_color.hsla = (self.board.players[sos.player_id].hue, 100, 50, 100)
            draw_nice_line(self.surface,
                           line_color, 
                           (self.board_ui.buttons[sos.p1], ), 
                           (, ),
                           max(1, self.size * 0.01))

    def menu_clicks(self, pos: Sequence, button: int = 1) -> None:
        row_y = self.surface.get_height() * 1/4

        # size down
        rect = pygame.Rect(0, row_y, self.cell_size, self.cell_size)
        rect.centerx = self.surface.get_width() * 1/3
        if self.board.num_cols - 1 >= 3 and rect.collidepoint(pos):
            self.board.num_cols -= 1
            self.board.num_rows -= 1
            return
            
        # size up
        rect = pygame.Rect(0, row_y, self.cell_size, self.cell_size)
        rect.centerx = self.surface.get_width() * 2/3
        if rect.collidepoint(pos):
            self.board.num_cols += 1
            self.board.num_rows += 1
            return


        row_y = self.surface.get_height() * 1/2

        # simple
        rect = pygame.Rect(0, row_y, 300, self.cell_size)
        rect.centerx = self.surface.get_width() * 1/4
        if rect.collidepoint(pos):
            self.board.game_mode = "simple"
            return
        
        # general
        rect = pygame.Rect(0, row_y, 300, self.cell_size)
        rect.centerx = self.surface.get_width() * 3/4
        if rect.collidepoint(pos):
            self.board.game_mode = "general"
            return

        row_y = self.surface.get_height() * 3/4

        # start
        rect = pygame.Rect(0, row_y, 200, self.cell_size)
        rect.centerx = self.surface.get_width() * 1/2
        if rect.collidepoint(pos):
            self.board.reset()

            self.cell_size = ((self.size - self.gap_size) /
                              self.board.num_cols - self.gap_size)

            self.cell_stride = self.cell_size + self.gap_size

            self.board_offset = ((self.surface.get_size()[0] - self.size)/2 + self.gap_size,
                                 (self.surface.get_size()[1] - self.size)/2 + self.gap_size)

            self.state = "play"
            return

    def cell_indices_to_pos(self, indices: Sequence) -> list:
        indices = [None] * len(indices)

        for idx, index in enumerate(indices):
            indices[idx] = 0 #TODO: fix this

        return indices

    def pos_to_cell_indices(self, pos: Sequence) -> list:
        indices = [None] * len(pos)

        for idx, coord in enumerate(pos):
            indices[idx] = math.floor((pos[idx] - (self.surface.get_size()[idx] - self.size + self.gap_size)/2) / self.cell_stride)

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

    def end_clicks(self, pos: Sequence, button: int = 1) -> None:
        print("Endgame click detection not implemented")

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

                            case "end":
                                self.end_clicks(pos, e.button)

            match self.state:
                case "menu":
                    self.draw_menu()

                case "play":
                    self.new_draw_board()

                case "end":
                    self.draw_end()

            pygame.display.update()

