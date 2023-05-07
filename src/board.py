# File: board.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

"""Basic classes and methods for an SOS game. User interface not included."""

from collections.abc import Sequence
from copy import deepcopy
from enum import Enum
import math
import random
from typing import NamedTuple

class Mark(Enum):
    """Possible states of an SOS grid space."""

    NONE  = 0 # used for returning out of bounds spaces
    EMPTY = 1
    S     = 2
    O     = 3

    def __lt__(self, other) -> bool:
        """NONE < EMPTY < S == O"""
        if self.__class__ is not other.__class__:
            return NotImplemented
        elif self == Mark.S:
            return False
        else:
            return self.value < other.value

    def __gt__(self, other) -> bool:
        """S == O > EMPTY > NONE"""
        if self.__class__ is not other.__class__:
            return NotImplemented
        elif self == Mark.O and other == Mark.S:
            return False
        else:
            return self.value > other.value

    def __le__(self, other) -> bool:
        """NONE <= EMPTY <= S != O"""
        if self.__class__ is not other.__class__:
            return NotImplemented
        elif self == Mark.S and other == Mark.O:
            return False
        else:
            return self.value <= other.value

    def __ge__(self, other) -> bool:
        """S != O >= EMPTY >= NONE"""
        if self.__class__ is not other.__class__:
            return NotImplemented
        elif self == Mark.O and other == Mark.S:
            return False
        else:
            return self.value >= other.value


class SOS:
    """Stores the start coordinate, end coordinate, and player id of an SOS."""

    def __init__(self,
                 p1: Sequence[int],
                 p2: Sequence[int],
                 player_id: int) -> None:

        if len(p1) <= 0 or len(p1) <= 0:
            raise ValueError("points must have a positive number of dimensions")

        elif len(p1) != len(p2):
            raise ValueError("points must have the same length/dimensionality")

        elif p1 == p2:
            raise ValueError("points cannot be the same")

        elif player_id < 0:
            raise ValueError("player id may not be negative")

        else:
            self.p1 = p1
            self.p2 = p2
            
            #self.p1 = {"x" : p1[0], "y" : p1[1]}
            #self.p2 = {"x" : p2[0], "y" : p2[1]}
            
            self.player_id = player_id

    def __repr__(self) -> None:
        return f"SOS({self.p1!r}, {self.p2!r}, {self.player_id!r})"

    def __str__(self) -> None:
        return f"(SOS from {self.p1} to {self.p2} by player {self.player_id})"


class Player:
    """Stores a player's name, what hue to use in a gui, and their score."""
    def __init__(self, name: str, hue: int = 0, computer: bool = False) -> None:
        if not 0 <= hue <= 360:
            raise ValueError("player hue must be between 0 and 360")

        else:
            self.name = name
            self.hue = hue
            self.score = 0
            self.computer = computer

    def __repr__(self) -> None:
        return f"Player({self.name}, {self.hue})"

    def __str__(self) -> None:
        return f"({self.name} has hue {self.hue} and has {self.score} points)"


class Move(NamedTuple):
    col: int
    row: int
    mark: Mark
    sos_count: int = 0
    player: int = -1

class Board:
    """SOS game."""
    def __init__(self,
                 num_cols: int = 8,
                 num_rows: int = 8,
                 players: list[Player] = None) -> None:

        if num_cols < 3 or num_rows < 3:
            raise ValueError("board dimensions must be greater than or equal to 3x3")

        elif players == []:
            raise ValueError("must specify at least one player")

        self.num_cols = num_cols
        self.num_rows = num_rows
        self.grid = [Mark.EMPTY] * (num_cols * num_rows)
        #self.empty_cells = 
        self.mark_count = 0

        if players is None:
            self.players = [Player("Player One", 0), Player("Player Two", 240)]
        else:
            self.players = players

        self.sos_list = []
        self.turn = 0

        self.move_hist = []
        self.move_future = []

        self.game_mode = "simple"

        self.end = False

    def __repr__(self) -> None:
        return f"Board({self.num_cols}, {self.num_rows}, {self.players!r})"

    def __str__(self) -> None:
        temp = " " + "-" * self.num_cols + "\n"
        for y in range(self.num_rows):
            temp += "|"
            for x in range(self.num_cols):
                match self.get_mark((x, y)):
                    case Mark.EMPTY:
                        temp += " "
                    case Mark.S:
                        temp += "S"
                    case Mark.O:
                        temp += "O"
            temp += "|\n"
        temp += " " + "-" * self.num_cols
        return temp

    def in_bounds(self, pos: Sequence[int]) -> bool:
        return (0 <= pos[0] < self.num_cols and
                0 <= pos[1] < self.num_rows)

    def out_of_bounds(self, pos: Sequence[int]) -> bool:
        return not self.in_bounds(pos)

    def get_mark(self, pos: Sequence[int] = None) -> Mark:
        if self.in_bounds(pos):
            return self.grid[(pos[1] * self.num_cols) + pos[0]]
        else:
            return Mark.NONE

    def get_char(self, pos: Sequence[int]) -> str:
        match self.get_mark(pos):
            case Mark.NONE:
                return " "
            case Mark.EMPTY:
                return " "
            case Mark.S:
                return "S"
            case Mark.O:
                return "O"

    # Does not automatically remove broken SOSes
    def set_mark(self, pos: Sequence[int], mark: Mark) -> None:
        if self.out_of_bounds(pos):
            raise IndexError("tried to set mark out of bounds")

        elif mark == Mark.NONE:
            raise ValueError("cannot set a cell to NONE")

        else:
            if mark > self.get_mark(pos):
                #self.empty_cells.discard(tuple(pos))
                self.mark_count += 1
            elif mark < self.get_mark(pos):
                #self.empty_cells.add(tuple(pos))
                self.mark_count -= 1

            self.grid[(pos[1] * self.num_cols) + pos[0]] = mark

    def clear(self) -> None:
        self.grid = [Mark.EMPTY] * (self.num_cols * self.num_rows)
        self.mark_count = 0
        self.sos_list.clear()
        self.move_hist.clear()
        self.move_future.clear()
        for player in self.players:
            player.score = 0

    # Assumes that col and row are in bounds
    def make_move(self, pos: Sequence[int], mark: Mark) -> bool:
        if mark <= Mark.EMPTY:
            raise ValueError("player cannot set a mark to empty")

        elif self.get_mark(pos) == Mark.EMPTY:
            self.set_mark(pos, mark)

            new_sos_list = self.creates_sos(pos, mark)
            self.get_player().score += len(new_sos_list)
            self.sos_list.extend(new_sos_list)

            self.move_hist.append(
                    Move(pos[0], pos[1], mark, len(new_sos_list), self.turn))
            self.move_future.clear()

            if self.detect_end():
                self.end = True
            else:
                self.turn = self.get_next_turn()

            return True
        else:
            return False

    def undo_move(self) -> None:
        if len(self.move_hist) > 0:
            last_move = self.move_hist.pop(-1)
            self.set_mark((last_move.col, last_move.row), Mark.EMPTY)
            del self.sos_list[-last_move.sos_count:]
            self.players[last_move.player].score -= last_move.sos_count
            self.turn = (self.turn - 1) % len(self.players)
            self.move_future.append(last_move)

    def save(self, file: str = "sos.sav") -> None:
        f = open('file', 'w')
        f.write(repr(self.move_hist))
        f.close()

    # Assumes that col and row are in bounds
    # Assumes that the space is empty
    def creates_sos(self, pos: Sequence[int], mark: Mark) -> list[SOS]:
        sos_list = []

        if self.out_of_bounds(pos):
            return sos_list

        offsets = ((-1,-1), # north west
                   ( 0,-1), # north
                   ( 1,-1), # north east
                   ( 1, 0), #       east
                   ( 1, 1), # south east
                   ( 0, 1), # south
                   (-1, 1), # south west
                   (-1, 0)) #       west

        match mark:
            case Mark.S:
                for off in offsets:
                    if (self.get_mark((pos[0] + off[0]  , pos[1] + off[1]  )) == Mark.O and
                        self.get_mark((pos[0] + off[0]*2, pos[1] + off[1]*2)) == Mark.S):

                        sos_list.append(SOS(pos,
                                            (pos[0] + off[0]*2, pos[1] + off[1]*2),
                                            self.turn))
            case Mark.O:
                for off in offsets[:4]:
                    if (self.get_mark((pos[0] + off[0], pos[1] + off[1])) == Mark.S and
                        self.get_mark((pos[0] - off[0], pos[1] - off[1])) == Mark.S):

                        sos_list.append(SOS((pos[0] + off[0], pos[1] + off[1]),
                                            (pos[0] - off[0], pos[1] - off[1]),
                                            self.turn))
        return sos_list

    def get_empty_cells(self) -> list[tuple[int]]:
        empty_cells = []
        for row in range(self.num_rows):     
            for col in range(self.num_cols):
                if self.get_mark((col, row)) == Mark.EMPTY:
                    empty_cells.append((col, row))
        return empty_cells


    def get_random_legal_position(self) -> tuple[int, int]:
        return random.choice(self.get_empty_cells())

    def get_optimal_move(self, depth: int = 0) -> Move:
        if self.mark_count == len(self.grid):
            return None
        
        else:
            best_score = -9
            best_moves = []

            for row in range(self.num_rows):
                for col in range(self.num_cols):
                    if self.get_mark((col, row)) == Mark.EMPTY:
                        for mark in (Mark.S, Mark.O):
                            
                            expected_gain = len(self.creates_sos((col, row), mark))

                            if self.game_mode == "simple" and expected_gain > 0:
                                return Move(col, row, mark, expected_gain)

                            if depth > 0:
                                test_board = deepcopy(self)
                                test_board.make_move((col, row), mark)
                                next_move = test_board.get_optimal_move(depth - 1)

                                if next_move is None:
                                    expected_loss = 0
                                else:
                                    expected_loss = next_move.sos_count
                            else:
                                expected_loss = 0

                            if self.game_mode == "simple":
                                if not expected_loss > 0:
                                    best_moves.append(Move(col, row, mark, 0))
                                continue

                            else:
                                expected_score = expected_gain# - expected_loss

                                if expected_score >= best_score:
                                    if expected_score > best_score:
                                        best_score = expected_score
                                        best_moves.clear()
                                    best_moves.append(Move(col, row, mark, expected_score))

            return random.choice(best_moves)

    def make_computer_move(self) -> None:
        move = self.get_optimal_move(1)
        self.make_move(move.col, move.row, move.mark)

    def get_next_turn(self) -> int:
        return (self.turn + 1) % len(self.players)

    def get_player(self) -> Player:
        return self.players[self.turn]

    def general_end(self) -> bool:
        return self.mark_count == self.num_cols * self.num_rows

    def simple_end(self) -> bool:
        return len(self.sos_list) > 0 or self.general_end()

    def detect_end(self) -> bool:
        match self.game_mode:
            case "simple"  : return self.simple_end()
            case "general" : return self.general_end()
            case _: raise NotImplementedError(f"Game mode {self.game_mode} does not exist.")


    # Can return a victor even when game isn't over
    # Useful for listing current leader(s)
    def general_victors(self) -> list[Player]:
        victors = []
        highscore = 0

        for player in self.players:
            if player.score >= highscore:
                if player.score > highscore:
                    highscore = player.score
                    victors.clear()
                victors.append(player)
        return victors

    def simple_victor(self) -> list[Player]:
        if len(self.sos_list) > 0:
            return [self.players[self.sos_list[0].player_id]]
        else:
            return self.players

    def victors(self) -> list[Player]:
        match self.game_mode:
            case "simple"  : return self.simple_victor()
            case "general" : return self.general_victors()
            case _: raise NotImplementedError(f"Game mode {self.game_mode} does not exist.")

    def reset(self,
              num_cols: int = -1, 
              num_rows: int = -1, 
              game_mode: str = None) -> None:
        
        if num_cols >= 3 and num_rows >= 3:
            self.num_cols = num_cols
            self.num_rows = num_rows
        
        self.clear()
        self.turn = 0
        self.end = False
 
        if game_mode in ("simple", "general"):
            self.game_mode = game_mode

