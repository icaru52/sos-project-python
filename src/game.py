# File: game.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

"""Pygame-based graphical frontend for the board.py SOS game."""

from collections.abc import Sequence
import os
import pygame

import board
from pygame_helper import *
import ui

class GameEvents:
    MAKE_MOVE = pygame.event.custom_type()

class Game:
    """GUI for displaying and interacting with SOS game board"""

    def __init__(self, window_size: Sequence[int]) -> None:

        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        self.surface = pygame.display.set_mode(window_size, pygame.RESIZABLE)

        self.board = board.Board()

        self.board_ui = ui.UI()
        self.menu_ui  = ui.UI()
        self.end_ui   = ui.UI()

        self.populate_buttons()
        self.resize()

        self.state = "menu"

        self.running = False

        self.clock = pygame.time.Clock()

    def populate_buttons(self) -> None:
        rect = pygame.Rect(0, 0, 0, 0)

        self.board_ui.clear()
        for y in range(self.board.size[1]):
            for x in range(self.board.size[0]):
                self.board_ui[f"{x} {y}"] = ui.Button(rect, 
                                                      self.board.get_char((x, y)), 
                                                      {"pos": (x, y)})

        self.menu_ui = ui.UI({
            "size_down"    : ui.Button(rect, "-"),
            "cur_size"     : ui.Button(rect, str(self.board.size[0])),
            "size_up"      : ui.Button(rect, "+"),
            
            "simple_game"  : ui.Button(rect, 
                                       "Simple Game", 
                                       {}, 
                                       self.board.game_mode == "simple"),
            
            "general_game" : ui.Button(rect, 
                                       "General Game", 
                                       {}, 
                                       self.board.game_mode == "general"),
            
            "player_one"   : ui.Button(rect, 
                                       "Player One: " + ("Computer"
                                            if self.board.players[0].computer
                                            else "Human"), 
                                       {}, 
                                       self.board.players[0].computer),
            
            "player_two"   : ui.Button(rect, 
                                       "Player Two: " + ("Computer" 
                                            if self.board.players[1].computer
                                            else "Human"), 
                                       {}, 
                                       self.board.players[1].computer),

            "start_game"   : ui.Button(rect, "START"),

            "load"         : ui.Button(rect, "Load?", {"file_path" : "sos.sav"})
        })

        self.end_ui = ui.UI({
            "victor"   : ui.Button(rect, "Victor"),
            "new_game" : ui.Button(rect, "New Game?"),
            "save"     : ui.Button(rect, "Save?"),
            "quit"     : ui.Button(rect, "Quit?")
        })

    def resize(self) -> None:
        self.size = min(self.surface.get_size())
        gap_size = self.size*0.01
        cell_size = ((self.size - gap_size) / self.board.size[0] - gap_size)

        width, height = self.surface.get_size()

        board_offset = ((width  - self.size)/2 + gap_size,
                        (height - self.size)/2 + gap_size)

        for y in range(self.board.size[1]):
            for x in range(self.board.size[0]):
                self.board_ui[f"{x} {y}"].rect = ( # Cursed, I know...
                    pygame.Rect(board_offset[0] + (cell_size + gap_size) * x, 
                                board_offset[1] + (cell_size + gap_size) * y, 
                                cell_size, 
                                cell_size))

        self.menu_ui["size_down"].rect    = rect_center((width * 1/6, height * 1/8),
                                                        (width * 1/8, height * 1/8))
 
        self.menu_ui["cur_size"].rect     = rect_center((width * 1/2, height * 1/8),
                                                        (width * 1/8, height * 1/8))
        
        self.menu_ui["size_up"].rect      = rect_center((width * 5/6, height * 1/8),
                                                        (width * 1/8, height * 1/8))

        self.menu_ui["simple_game"].rect  = rect_center((width * 1/4, height * 3/8),
                                                        (width * 1/4, height * 1/8))

        self.menu_ui["general_game"].rect = rect_center((width * 3/4, height * 3/8),
                                                        (width * 1/4, height * 1/8))

        self.menu_ui["player_one"].rect   = rect_center((width * 1/4, height * 5/8),
                                                        (width * 1/4, height * 1/8))

        self.menu_ui["player_two"].rect   = rect_center((width * 3/4, height * 5/8),
                                                        (width * 1/4, height * 1/8))
        
        self.menu_ui["start_game"].rect   = rect_center((width * 1/2, height * 7/8),
                                                        (width * 1/2, height * 1/8))
        
        self.menu_ui["load"].rect         = rect_center((width * 7/8, height * 7/8),
                                                        (width * 1/8, height * 1/8))
        
        self.end_ui["victor"].rect        = rect_center((width * 1/2, height * 1/4),
                                                        (width * 1/2, height * 1/4))

        self.end_ui["new_game"].rect      = rect_center((width * 1/6, height * 3/4),
                                                        (width * 1/6, height * 1/4))

        self.end_ui["save"].rect          = rect_center((width * 3/6, height * 3/4),
                                                        (width * 1/6, height * 1/4))

        self.end_ui["quit"].rect          = rect_center((width * 5/6, height * 3/4),
                                                        (width * 1/6, height * 1/4))

    def draw_menu(self) -> None:
        self.surface.fill((50, 50, 50))
        self.menu_ui.draw(self.surface)
        
    def draw_board(self) -> None:
        self.surface.fill((50, 50, 50))
        border_color = hue_to_color(self.board.get_player().hue)
        pygame.draw.rect(self.surface, border_color, self.surface.get_rect(), 2)

        self.board_ui.draw(self.surface)
        self.draw_sos_list()

    def draw_end(self) -> None:
        self.surface.fill((50, 50, 50))
        self.board_ui.draw(self.surface, False)
        self.draw_sos_list()

        victors = self.board.victors()
        victor_colors = [hue_to_color(victor.hue) for victor in victors]
        victor_color = color_multilerp(victor_colors)

        cover_rect = pygame.Surface(self.surface.get_size())
        cover_rect.set_alpha(50)
        cover_rect.fill(victor_color)
        self.surface.blit(cover_rect, (0, 0))

        if len(victors) == 1:

            victor_names = "Victor: " + victors[0].name
        else:
            victor_names = "Victors:"
            for victor in victors:
                victor_names += " " + victor.name

        self.end_ui["victor"].text = victor_names

        self.end_ui.draw(self.surface)

    def draw_sos_list(self) -> None:
        for sos in self.board.sos_list:
            draw_nice_line(self.surface,
                           hue_to_color(self.board.players[sos.player_id].hue), 
                           self.board_ui[f"{sos.p1[0]} {sos.p1[1]}"].rect.center, 
                           self.board_ui[f"{sos.p2[0]} {sos.p2[1]}"].rect.center,
                           max(1, self.size / self.board.size[0] * 0.1))

    def handle_menu_clicks(self, key: str, mouse_button: int = 1) -> None:
        match key:
            case "size_down":
                if self.board.size[0] > 3:
                    self.board.size = tuple(i-1 for i in self.board.size)
                    self.menu_ui["cur_size"].text = str(self.board.size[0])
            
            case "size_up":
                self.board.size = tuple(i+1 for i in self.board.size)
                self.menu_ui["cur_size"].text = str(self.board.size[0])
            
            case "simple_game":
                self.board.game_mode = "simple"
                self.menu_ui["simple_game"].clicked = True
                self.menu_ui["general_game"].clicked = False
            
            case "general_game":
                self.board.game_mode = "general"
                self.menu_ui["simple_game"].clicked = False
                self.menu_ui["general_game"].clicked = True
            
            case "player_one":
                self.board.players[0].computer = not self.board.players[0].computer
                self.menu_ui["player_one"].clicked = not self.menu_ui["player_one"].clicked
                self.menu_ui["player_one"].text = "Player One: " + ("Computer" 
                                            if self.board.players[0].computer
                                            else "Human")
            
            case "player_two":
                self.board.players[1].computer = not self.board.players[1].computer
                self.menu_ui["player_two"].clicked = not self.menu_ui["player_two"].clicked
                self.menu_ui["player_two"].text = "Player Two: " + ("Computer" 
                                            if self.board.players[1].computer
                                            else "Human")
            
            case "start_game":
                self.board.reset()
                self.populate_buttons()
                self.resize()
                self.state = "play"

            case "load":
                if os.path.isfile("sos.sav"):
                    self.board.load("sos.sav")

                    self.menu_ui["cur_size"].text = str(self.board.size[0])

                    self.menu_ui["simple_game"].clicked = (self.board.game_mode == "simple")
                    self.menu_ui["general_game"].clicked = (self.board.game_mode == "general")

                    self.menu_ui["player_one"].clicked = self.board.players[0].computer
                    self.menu_ui["player_one"].text = "Player One: " + ("Computer" 
                                                if self.board.players[0].computer
                                                else "Human")

                    self.menu_ui["player_two"].clicked = self.board.players[1].computer
                    self.menu_ui["player_two"].text = "Player Two: " + ("Computer" 
                                                if self.board.players[1].computer
                                                else "Human")
                    while self.board.move_future:
                        next_move = self.board.move_future[-1]
                        attrs = {"pos": next_move.pos, "mark": next_move.mark}
                        pygame.event.post(pygame.event.Event(GameEvents.MAKE_MOVE, attrs))

    def handle_board_clicks(self, pos: Sequence[int], button: int) -> None:
        if (not self.board.get_player().computer) and (button in (1, 3)) :
            match button:
                case 1: mark = board.Mark.S
                case 3: mark = board.Mark.O
            attrs = {"pos": pos, "mark": mark}
            pygame.event.post(pygame.event.Event(GameEvents.MAKE_MOVE, attrs))

    def click_cell(self, pos: Sequence[int], mark: board.Mark) -> None:
        self.board.make_move(pos, mark)
        self.board_ui[f"{pos[0]} {pos[1]}"].text = self.board.get_char(pos)
        if self.board.end:
            self.state = "end"

    def handle_end_clicks(self, key: str, button: int = 1) -> None:
        match key:
            case "new_game":
                self.state = "menu"
            case "save":
                self.board.save()
            case "quit":
                self.running = False

    def start(self) -> None:
        self.running = True

        while self.running:
            if self.state == "play" and self.board.get_player().computer:
                move = self.board.get_optimal_move(1)
                attrs = {"pos": move.pos, "mark": move.mark}
                pygame.event.post(pygame.event.Event(GameEvents.MAKE_MOVE, attrs))

            for e in pygame.event.get():
                match e.type:
                    case pygame.QUIT:
                        self.running = False

                    case pygame.KEYDOWN:
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_q] or keys[pygame.K_ESCAPE]:
                            self.running = False

                    case pygame.VIDEORESIZE:
                        self.resize()

                    case pygame.MOUSEBUTTONUP:
                        match self.state:
                            case "menu" : self.menu_ui.click(e.pos, e.button)
                            case "play" : self.board_ui.click(e.pos, e.button)
                            case "end"  : self.end_ui.click(e.pos, e.button)

                    case ui.BUTTON_CLICK:
                        match self.state:
                            case "menu" : self.handle_menu_clicks(e.key, e.mouse_button)
                            case "play" : self.handle_board_clicks(e.pos, e.mouse_button)
                            case "end"  : self.handle_end_clicks(e.key, e.mouse_button)

                    case GameEvents.MAKE_MOVE:
                        self.click_cell(e.pos, e.mark)

            match self.state:
                case "menu" : self.draw_menu()
                case "play" : self.draw_board()
                case "end"  : self.draw_end()

            pygame.display.update()

            self.clock.tick(40)

