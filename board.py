# File: board.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

from collections.abc import Sequence
from enum import Enum

class Mark(Enum):
    NONE  = 0
    EMPTY = 1
    S     = 2
    O     = 3

    def __lt__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented
        elif self == Mark.S and other == Mark.O:
            return False
        else:
            return self.value < other.value

    def __gt__(self, other):
        if self.__class__ is not other.__class__:
            return NotImplemented
        elif self == Mark.O and other == Mark.S:
            return False
        else:
            return self.value > other.value

class SOS:
    def __init__(self, p1: Sequence, p2: Sequence, player_id: int) -> None:
        self.p1 = p1
        self.p2 = p2
        self.player_id = player_id

    def __repr__(self) -> None:
        return f'SOS({self.p1.__repr__()}, {self.p2.__repr__()})'

    def __str__(self) -> None:
        return f'({self.p1.__str__()}, {self.p2.__str__()})'


class Player:
    def __init__(self, name: str, hue: int) -> None:
        self.name = name
        self.hue = hue
        self.score = 0


class Board:
    def __init__(self, num_cols: int = 8, num_rows: int = 8) -> None:
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.grid = [Mark.EMPTY] * (num_cols * num_rows)
        self.mark_count = 0

        self.players = [Player("One",   0),
                        Player("Two", 240)]
        self.sos_list = []
        self.turn = 0

    def __str__(self):
        temp = ' ' + '-' * self.num_cols + '\n'
        for y in range(self.num_rows):
            temp += '|'
            for x in range(self.num_cols):
                match self.get_mark(x, y):
                    case Mark.EMPTY:
                        temp += ' '
                    case Mark.S:
                        temp += 'S'
                    case Mark.O:
                        temp += 'O'
            temp += '|\n'
        temp += " " + "-" * self.num_cols
        return temp

    def in_bounds(self, col: int, row: int) -> bool:
        return (0 <= col < self.num_cols and
                0 <= row < self.num_rows)

    def out_of_bounds(self, col: int, row: int) -> bool:
        return not self.in_bounds(col, row)

    def get_mark(self, col: int, row: int) -> Mark:
        if self.in_bounds(col, row):
            return self.grid[(row * self.num_cols) + col]
        else:
            return Mark.NONE

    # Does not automatically remove broken SOSes
    def set_mark(self, col: int, row: int, mark: Mark) -> None:
        if self.in_bounds(col, row) and mark != Mark.NONE:
            self.grid[(row * self.num_cols) + col] = mark

            # If one or the other is empty, but not neither
            if mark > self.get_mark(col, row):
                self.mark_count += 1
            elif mark < self.get_mark(col, row):
                self.mark_count -= 1

    def clear(self) -> None:
        self.grid = [Mark.EMPTY] * (self.num_cols * self.num_rows)
        self.mark_count = 0
        self.sos_list = []

    # Assumes that col and row are in bounds
    def make_move(self, col: int, row: int, mark: Mark) -> bool:
        if mark > Mark.EMPTY and self.get_mark(col, row) == Mark.EMPTY:
            self.set_mark(col, row, mark)

            new_sos_list = self.creates_sos(col, row, mark)
            self.players[self.turn].score += len(new_sos_list)
            self.sos_list.extend(new_sos_list)

            self.turn = (self.turn + 1) % len(self.players)

            return True
        else:
            return False


    # Assumes that col and row are in bounds
    # Assumes that the space is empty
    def creates_sos(self, col: int, row: int, mark: Mark) -> list[SOS]:
        offsets = ((-1,-1), # north west
                   ( 0,-1), # north
                   ( 1,-1), # north east
                   ( 1, 0), #       east
                   ( 1, 1), # south east
                   ( 0, 1), # south
                   (-1, 1), # south west
                   (-1, 0)) #       wes

        sos_list = []

        match mark:
            case Mark.S:
                for i in range(8):
                    x_off = offsets[i][0]
                    y_off = offsets[i][1]

                    if (self.get_mark(col + x_off, row + y_off) == Mark.O and
                        self.get_mark(col + x_off*2, row + y_off*2) == Mark.S):

                        sos_list.append(SOS((col, row),
                                            (col + x_off*2, row + y_off*2),
                                            self.turn))
            case Mark.O:
                for i in range(4):
                    x_off = offsets[i][0]
                    y_off = offsets[i][1]

                    if (self.get_mark(col + x_off, row + y_off) == Mark.S and
                        self.get_mark(col - x_off, row - y_off) == Mark.S):

                        sos_list.append(SOS((col + x_off, row + y_off),
                                            (col - x_off, row - y_off),
                                            self.turn))
        return sos_list

    def general_end(self) -> bool:
        return self.mark_count == self.num_cols * self.num_rows:

    def simple_end(self) -> bool:
        return len(self.sos_list) > 0 or self.general_end()

    # Can return a victor even when game isn't over
    # Useful for listing current leader(s)
    def general_victors(self) -> List(int):
        victors = []
        highscore = 0

        for player in self.players:
            if player.score >= highscore:
                if player.score > highscore:
                    highscore = player.score
                    victors.clear()
                victors.append(player)
        return victors

    def simple_victor(self) -> int:
        if len(self.sos_list) > 0:
            return self.sos_list[0].player_id
        else:
            return -1

    def reset(self, num_cols: int = -1, num_rows: int = -1) -> None:
        if num_cols >= 3 and num_rows >= 3:
            self.num_cols = num_cols
            self.num_rows = num_rows
        self.clear()
        self.turn = 0
