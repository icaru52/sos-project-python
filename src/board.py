# File: board.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

"""Basic classes and methods for an SOS game. User interface not included."""

from collections.abc import Sequence
from enum import Enum

#class Vector:
#    """For storing coordinates"""
#    def __init__(self, x: int, y: int) -> None:
#        self.x = x
#        self.y = y
#
#    def __add__(self, other) -> Vector:
#        if self.__class__ is not other.__class__:
#            return NotImplemented
#        else:
#            return Vector(self.x + other.x, self.y + other.y)
#
#    def __sub__(self, other) -> Vector:
#        if self.__class__ is not other.__class__:
#            return NotImplemented
#        else:
#            return Vector(self.x - other.x, self.y - other.y)
#
#    def __mul__(self, scalar: int) -> Vector:
#        if not isinstance(scalar, int):
#            return NotImplemented
#        else:
#            return Vector(self.x * scalar, self.y * scalar)

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
    
    """
    def __init__(self,
                 points: Sequence[Sequence[int]],
                 player_id: int) -> None:

        if any(len(p) <= 0 for p in self.points):
            raise ValueError("points must have a positive number of dimensions")

        elif any(len(point) != len(self.points[0]) for point in self.points):
            # TODO: make this not double compare first element
            raise ValueError("points must have the same length/dimensionality")

        #elif p1 == p2: # TODO: fix this
        #    raise ValueError("points cannot be the same")

        elif player_id < 0:
            raise ValueError("player id may not be negative")

        else:
            self.points = points
            self.player_id = player_id
    """

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
            self.player_id = player_id

    def __repr__(self) -> None:
        return f"SOS({self.p1!r}, {self.p2!r}, {self.player_id!r})"

    """
    def __repr__(self) -> None:
        return f"SOS({self.points!r}, {self.player_id!r})"
    """

    def __str__(self) -> None:
        return f"(SOS from {self.p1} to {self.p2} by player {self.player_id})"


class Player:
    """Stores a player's name, what hue to use in a gui, and their score."""
    def __init__(self, name: str, hue: int = 0) -> None:
        if hue < 0:
            raise ValueError("player hue may not be negative")

        else:
            self.name = name
            self.hue = hue
            self.score = 0

    def __repr__(self) -> None:
        return f"Player({self.name}, {self.hue})"

    def __str__(self) -> None:
        return f"({self.name} has hue {self.hue} and has {self.score} points)"


class Board:
    """SOS game."""
    def __init__(self,
                 num_cols: int = 8,
                 num_rows: int = 8,
                 players: list[Player] = None) -> None:

    #def __init__(self,
    #             dimensions: tuple[int],
    #             players: list[Player] = None) -> None:

        if num_cols < 3 or num_rows < 3:
            raise ValueError("board dimensions must be greater than 3x3")

        elif players == []:
            raise ValueError("must specify at least one player")

        self.num_cols = num_cols
        self.num_rows = num_rows
        #self.dimensions = dimensions 
        self.grid = [Mark.EMPTY] * (num_cols * num_rows)
        #self.grid = [Mark.EMPTY] * sum(dimensions)
        self.mark_count = 0

        if players is None:
            self.players = [Player("One", 0), Player("Two", 240)]
        else:
            self.players = players

        self.sos_list = []
        self.turn = 0

    def __repr__(self) -> None:
        return f"Board({self.num_cols}, {self.num_rows}, {self.players!r})"

    """
    def __repr__(self) -> None:
        return f"Board({self.dimensions}, {self.players!r})"
    """

    def __str__(self) -> None:
        temp = " " + "-" * self.num_cols + "\n"
        for y in range(self.num_rows):
            temp += "|"
            for x in range(self.num_cols):
                match self.get_mark(x, y):
                    case Mark.EMPTY:
                        temp += " "
                    case Mark.S:
                        temp += "S"
                    case Mark.O:
                        temp += "O"
            temp += "|\n"
        temp += " " + "-" * self.num_cols
        return temp

    def in_bounds(self, col: int, row: int) -> bool:
        return (0 <= col < self.num_cols and
                0 <= row < self.num_rows)

    """
    def in_bounds(self, coords: Sequence[int]) -> bool:
        return all(0 <= coord < axis for coord, axis in zip(coords, self.dimensions))
    """

    def out_of_bounds(self, col: int, row: int) -> bool:
        return not self.in_bounds(col, row)

    """
    def out_of_bounds(self, coords: Sequence[int]) -> bool:
        return not self.in_bounds(coords)
    """

    def get_mark(self, col: int = -1, row: int = -1) -> Mark:
        if self.in_bounds(col, row):
            return self.grid[(row * self.num_cols) + col]
        else:
            return Mark.NONE

    """
    def get_mark(self, coords: Sequence[int]) -> Mark:
        if self.in_bounds(coords):
            return self.grid[] #TODO: fix this
        else:
            return Mark.NONE
    """

    def get_char(self, col: int, row: int) -> str:
        match self.get_mark(col, row):
            case Mark.NONE:
                return " "
            case Mark.EMPTY:
                return " "
            case Mark.S:
                return "S"
            case Mark.O:
                return "O"
    """
    def get_char(self, coords: Sequence[int]) -> str:
        match self.get_mark(coords):
            case Mark.NONE:
                return " "
            case Mark.EMPTY:
                return " "
            case Mark.S:
                return "S"
            case Mark.O:
                return "O"
    """

    # Does not automatically remove broken SOSes
    def set_mark(self, col: int, row: int, mark: Mark) -> None:
        if self.out_of_bounds(col, row):
            raise IndexError("tried to set mark out of bounds")

        elif mark == Mark.NONE:
            raise ValueError("cannot set a cell to NONE")

        else:
            if mark > self.get_mark(col, row):
                self.mark_count += 1
            elif mark < self.get_mark(col, row):
                self.mark_count -= 1

            self.grid[(row * self.num_cols) + col] = mark

    """
    # Does not automatically remove broken SOSes
    def set_mark(self, coords: Sequence[int], mark: Mark) -> None:
        if self.out_of_bounds(coords):
            raise IndexError("tried to set mark out of bounds")

        elif mark == Mark.NONE:
            raise ValueError("cannot set a cell to NONE")

        else:
            if mark > self.get_mark(coords):
                self.mark_count += 1
            elif mark < self.get_mark(coords):
                self.mark_count -= 1

            self.grid[] = mark # TODO: fix this
    """

    def clear(self) -> None:
        self.grid = [Mark.EMPTY] * (self.num_cols * self.num_rows)
        self.mark_count = 0
        self.sos_list = []

    """
    def clear(self) -> None:
        self.grid = [Mark.EMPTY] * sum(self.dimensions)
        self.mark_count = 0
        self.sos_list = []
    """

    # Assumes that col and row are in bounds
    def make_move(self, col: int, row: int, mark: Mark) -> bool:
        if mark <= Mark.EMPTY:
            raise ValueError("player cannot set a mark to empty")

        elif self.get_mark(col, row) == Mark.EMPTY:
            self.set_mark(col, row, mark)

            new_sos_list = self.creates_sos(col, row, mark)
            self.players[self.turn].score += len(new_sos_list)
            self.sos_list.extend(new_sos_list)

            self.turn = (self.turn + 1) % len(self.players)

            return True
        else:
            return False

    """
    # Assumes that col and row are in bounds
    def make_move(self, coords: Sequence[int], mark: Mark) -> bool:
        if mark <= Mark.EMPTY:
            raise ValueError("player cannot set a mark to empty")

        elif self.get_mark(coords) == Mark.EMPTY:
            self.set_mark(coords, mark)

            new_sos_list = self.creates_sos(coords, mark)
            self.players[self.turn].score += len(new_sos_list)
            self.sos_list.extend(new_sos_list)

            self.turn = (self.turn + 1) % len(self.players)

            return True
        else:
            return False
    """

    # Assumes that col and row are in bounds
    # Assumes that the space is empty
    def creates_sos(self, col: int, row: int, mark: Mark) -> list[SOS]:
        sos_list = []

        if self.out_of_bounds(col, row):
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
                for x_off, y_off in offsets:
                    if (self.get_mark(col + x_off, row + y_off) == Mark.O and
                        self.get_mark(col + x_off*2, row + y_off*2) == Mark.S):

                        sos_list.append(SOS((col, row),
                                            (col + x_off*2, row + y_off*2),
                                            self.turn))
            case Mark.O:
                for x_off, y_off in offsets[:4]:
                    if (self.get_mark(col + x_off, row + y_off) == Mark.S and
                        self.get_mark(col - x_off, row - y_off) == Mark.S):

                        sos_list.append(SOS((col + x_off, row + y_off),
                                            (col - x_off, row - y_off),
                                            self.turn))
        return sos_list

    def general_end(self) -> bool:
        return self.mark_count == self.num_cols * self.num_rows

    """
    def general_end(self) -> bool:
        return self.mark_count == sum(self.dimensions)
    """

    def simple_end(self) -> bool:
        return len(self.sos_list) > 0 or self.general_end()

    # Can return a victor even when game isn't over
    # Useful for listing current leader(s)
    def general_victors(self) -> list[int]:
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

