# File: newgame.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

"""Pygame-based graphical frontend for the board.py SOS game."""

from collections.abc import Sequence
import math
import os
import pygame

import board
from pygame_helper import draw_nice_line
import ui


class Game:
    """GUI for displaying and interacting with SOS game board"""

    def __init__(self,
                 window_width:  int = 512,
                 window_height: int = 512) -> None:

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        self.surface = pygame.display.set_mode((window_width, window_height), 
                                               pygame.RESIZABLE)

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

    def populate_buttons(self) -> None:
        rect = pygame.Rect(0, 0, 0, 0)

        for y in range(self.board.num_rows):
            for x in range(self.board.num_cols):
                self.board_ui.add(ui.Button(rect,
                                            {"x": x, "y": y},
                                            self.board.get_char(x, y),
                                            False,
                                            pygame.Color(100),
                                            pygame.Color(150),
                                            pygame.Color("white")))

        # size down
        self.menu_ui.add(ui.Button(rect,
                                   "size_down",
                                   "-",
                                   False,
                                   pygame.Color(100),
                                   pygame.Color(150),
                                   pygame.Color("white")))

        # size up
        self.menu_ui.add(ui.Button(rect,
                                   "size_up",
                                   "+",
                                   False,
                                   pygame.Color(100),
                                   pygame.Color(150),
                                   pygame.Color("white")))

        # simple
        self.menu_ui.add(ui.Button(rect,
                                   "simple_game",
                                   "Simple Game",
                                   True,
                                   pygame.Color(100),
                                   pygame.Color(150),
                                   pygame.Color("white")))

        # general
        self.menu_ui.add(ui.Button(rect,
                                   "general_game",
                                   "General Game",
                                   False,
                                   pygame.Color(100),
                                   pygame.Color(150),
                                   pygame.Color("white")))

        """
        # start
        rect = pygame.Rect(0, row_y, 200, cell_size)
        rect.centerx = self.surface.get_rect().centerx
        draw_button(self.surface, 
                   (100, 100, 100), 
                   (150, 150, 150), 
                   "START", 
                   rect)
        """

        self.menu_ui.add(ui.Button(rect,
                                   "start_game",
                                   "START",
                                   False,
                                   pygame.Color(100),
                                   pygame.Color(150),
                                   pygame.Color("white")))

    #def resize(self, Sequence[]) -> None:
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
                           self.board_ui.buttons[sos.p1[1] * self.board.num_cols + sos.p1[0].rect.center], 
                           self.board_ui.buttons[sos.p2[1] * self.board.num_cols + sos.p2[0].rect.center],
                           max(1, self.size * 0.01))

    def menu_clicks(self, pos: Sequence, button: int = 1) -> None:
        """
        # size down
        self.board.num_cols -= 1
        self.board.num_rows -= 1
            
        # size up
        self.board.num_cols += 1
        self.board.num_rows += 1

        # simple
        self.board.game_mode = "simple"
                
        # general
        self.board.game_mode = "general"

        # start
        self.board.reset()
        self.state = "play"
        """

    def board_clicks(self, pos: Sequence, button: int = 1) -> None:
        cell_col, cell_row = self.pos_to_cell_indices(pos)

        if (0 <= cell_col < self.board.num_cols and
            0 <= cell_row < self.board.num_rows):

            match button:
                case 1: self.board.make_move(cell_col, cell_row, board.Mark.S)
                case 3: self.board.make_move(cell_col, cell_row, board.Mark.O)

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

                    case pygame.VIDEORESIZE:
                        #self.surface = pygame.display.set_mode(e.size, pygame.RESIZABLE)
                        self.resize(e.size)

                    case pygame.MOUSEBUTTONUP:
                        match self.state:
                            case "menu": self.menu_ui.click(e.pos, e.button)
                            case "play": self.board_ui.click(e.pos, e.button)
                            #case "end":  self.end_ui.click(e.pos, e.button)

                    case ui.BUTTON_CLICK:
                        match self.state:
                            case "menu": self.menu_clicks()
                            case "play": self.board_clicks()
                            #case "end":  self.end_clicks()


            match self.state:
                case "menu": self.draw_menu()
                case "play": self.draw_board()
                #case "end":  self.draw_end()

            pygame.display.update()

