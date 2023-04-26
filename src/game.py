# File: game.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

"""Pygame-based graphical frontend for the board.py SOS game."""

from collections.abc import Sequence
import os
import pygame

import board
from pygame_helper import draw_nice_line
from pygame_helper import rect_center
import ui


class Game:
    """GUI for displaying and interacting with SOS game board"""

    def __init__(self, window_size: Sequence[int]) -> None:

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        self.surface = pygame.display.set_mode(window_size, pygame.RESIZABLE)

        self.board = board.Board()

        self.board_ui = ui.UI()
        self.menu_ui = ui.UI()

        self.populate_buttons()
        self.resize()

        self.state = "menu"

    def populate_buttons(self) -> None:
        rect = pygame.Rect(0, 0, 0, 0)

        self.board_ui.clear()
        for y in range(self.board.num_rows):
            for x in range(self.board.num_cols):
                self.board_ui.add(str(x)+" "+str(y), 
                                  ui.Button(rect, self.board.get_char(x, y), {"x": x, "y": y}))

        self.menu_ui.clear()

        # size down
        self.menu_ui.add("size_down", ui.Button(rect, "-"))

        # current size
        self.menu_ui.add("cur_size", ui.Button(rect, str(self.board.num_cols)))

        # size up
        self.menu_ui.add("size_up", ui.Button(rect, "+"))

        # simple
        self.menu_ui.add("simple_game", ui.Button(rect, "Simple Game", {}, True))

        # general
        self.menu_ui.add("general_game", ui.Button(rect, "General Game", {}, False))

        # start
        self.menu_ui.add("start_game", ui.Button(rect, "START"))

    def resize(self) -> None:
        self.size = min(self.surface.get_size())
        gap_size = self.size*0.01
        cell_size = ((self.size - gap_size) / self.board.num_cols - gap_size)

        width, height = self.surface.get_size()

        board_offset = ((width  - self.size)/2 + gap_size,
                        (height - self.size)/2 + gap_size)

        for y in range(self.board.num_rows):
            for x in range(self.board.num_cols):
                self.board_ui.buttons[str(x)+" "+str(y)].rect = ( # Cursed, I know...
                    pygame.Rect(board_offset[0] + (cell_size + gap_size) * x, 
                                board_offset[1] + (cell_size + gap_size) * y, 
                                cell_size, 
                                cell_size))

        self.menu_ui.buttons["size_down"].rect = rect_center(width * 1/3, height * 1/4,
                                                             cell_size, cell_size)
 
        self.menu_ui.buttons["cur_size"].rect = rect_center(width * 1/2, height * 1/4,
                                                           cell_size, cell_size)
        
        self.menu_ui.buttons["size_up"].rect = rect_center(width * 2/3, height * 1/4,
                                                           cell_size, cell_size)

        self.menu_ui.buttons["simple_game"].rect = rect_center(width * 1/4, height * 1/2,
                                                               width * 1/4, cell_size)

        self.menu_ui.buttons["general_game"].rect = rect_center(width * 3/4, height * 1/2,
                                                                width * 1/4, cell_size)

        self.menu_ui.buttons["start_game"].rect = rect_center(width * 1/2, height * 3/4,
                                                              width * 1/2, cell_size)
    

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

        #rect = pygame.Rect(0, 0, 200, 200)
        #rect.center = self.surface.get_rect().center
        #draw_button(self.surface, (0, 0, 0), (50, 50, 50), "end", rect)

    def draw_sos_list(self) -> None:
        for sos in self.board.sos_list:
            line_color = pygame.Color(0)
            line_color.hsla = (self.board.players[sos.player_id].hue, 100, 50, 100)
            draw_nice_line(self.surface,
                           line_color, 
                           self.board_ui.buttons[str(sos.p1[0])+" "+str(sos.p1[1])].rect.center, 
                           self.board_ui.buttons[str(sos.p2[0])+" "+str(sos.p2[1])].rect.center,
                           max(1, self.size / self.board.num_cols * 0.1))

    def menu_clicks(self, key: str, mouse_button: int = 1) -> None:
        match key:
            case "size_down":
                if self.board.num_cols > 3:
                    self.board.num_cols -= 1
                    self.board.num_rows -= 1
                    self.menu_ui.buttons["cur_size"].text = str(self.board.num_cols)
            
            case "size_up":
                self.board.num_cols += 1
                self.board.num_rows += 1
                self.menu_ui.buttons["cur_size"].text = str(self.board.num_cols)
            
            case "simple_game":
                self.board.game_mode = "simple"
                self.menu_ui.buttons["simple_game"].clicked = True
                self.menu_ui.buttons["general_game"].clicked = False
            
            case "general_game":
                self.board.game_mode = "general"
                self.menu_ui.buttons["simple_game"].clicked = False
                self.menu_ui.buttons["general_game"].clicked = True
            
            case "start_game":
                self.board.reset()
                self.populate_buttons()
                self.resize()
                self.state = "play"

    def board_clicks(self, col: int, row: int, button: int = 1) -> None:
        self.board.make_move(col, row, board.Mark.S if button == 1 else board.Mark.O)
        self.board_ui.buttons[str(col) + " " + str(row)].text = self.board.get_char(col, row)

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
                        self.resize()

                    case pygame.MOUSEBUTTONUP:
                        match self.state:
                            case "menu": self.menu_ui.click(e.pos, e.button)
                            case "play": self.board_ui.click(e.pos, e.button)
                            #case "end":  self.end_ui.click(e.pos, e.button)

                    case ui.BUTTON_CLICK:
                        match self.state:
                            case "menu": self.menu_clicks(e.key, e.mouse_button)
                            case "play": self.board_clicks(e.x, e.y, e.mouse_button)
                            #case "end":  self.end_clicks()


            match self.state:
                case "menu": self.draw_menu()
                case "play": self.draw_board()
                #case "end":  self.draw_end()

            pygame.display.update()

