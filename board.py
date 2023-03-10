# File: board.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

from enum import Enum

class Mark(Enum):
    EMPTY = 0
    S     = 1
    O     = 2


class SOS:
    def __init__(self, p1, p2, playerID: int) -> None:
        self.p1 = p1
        self.p2 = p2
        self.playerID = playerID


class Player:
    def __init__(self, name: str, hue) -> None:
        self.name = name
        self.hue = hue
        self.score = 0


class Board:
    def __init__(self, numCols: int = 8, numRows: int = 8) -> None:
        self.numCols = numCols
        self.numRows = numRows
        self.grid = [Mark.EMPTY] * (numCols * numRows)
        self.markCount = 0

        self.players = [Player("One",   0), 
                        Player("Two", 240)]
        self.sosList = []
        self.turn = 0

    def __str__(self):
        temp = ' ' + '-' * self.numCols + '\n'
        for y in range(self.numRows):
            temp += '|'
            for x in range(self.numCols):
                match self.getMark(x, y):
                    case Mark.EMPTY:
                        temp += ' '
                    case Mark.S:
                        temp += 'S'
                    case Mark.O:
                        temp += 'O'
            temp += '|\n'
        temp += " " + "-" * self.numCols
        return temp

    def inBounds(self, col: int, row: int) -> bool:
        return (0 <= col < self.numCols and
                0 <= row < self.numRows)

    def outOfBounds(self, col: int, row: int) -> bool:
        return not self.inBounds(col, row)

    # Assumes that col and row are in bounds
    def getMark(self, col: int, row: int) -> Mark:
        return self.grid[(row * self.numCols) + col]

    # Assumes that col and row are in bounds
    def setMark(self, col: int, row: int, mark: Mark) -> None:
        self.grid[(row * self.numCols) + col] = mark

        # If one or the other is empty, but not neither
        if (mark == Mark.EMPTY) != (self.getMark(col, row) == Mark.EMPTY):
            self.markCount += (-1 if mark == Mark.EMPTY else 1)

    def clear(self) -> None:
        self.grid = [Mark.EMPTY] * (self.numCols * self.numRows)

    # Assumes that col and row are in bounds
    def makeMove(self, col: int, row: int, mark: Mark) -> bool:
        if mark != Mark.EMPTY and self.getMark(col, row) == Mark.EMPTY:
            self.setMark(col, row, mark)
            
            newSOSList = self.createsSOS(col, row, mark)
            self.players[self.turn].score += len(newSOSList)
            self.sosList.extend(newSOSList)

            self.turn = (self.turn + 1) % len(self.players)

            return True
        else:
            return False


    # Assumes that col and row are in bounds
    # Assumes that the space is empty
    def createsSOS(self, col: int, row: int, mark: Mark) -> list[SOS]:
        offsets = ((-1,-1), # north west
                   ( 0,-1), # north
                   ( 1,-1), # north east
                   ( 1, 0), #       east
                   ( 1, 1), # south east
                   ( 0, 1), # south
                   (-1, 1), # south west
                   (-1, 0)) #       west

        sosList = []

        match mark:
            case Mark.S:
                for i in range(8):
                    xOff = offsets[i][0]
                    yOff = offsets[i][1]

                    if (self.inBounds(col + xOff*2, row + yOff*2) and
                        self.getMark( col + xOff  , row + yOff  ) == Mark.O and
                        self.getMark( col + xOff*2, row + yOff*2) == Mark.S):

                        sosList.append(SOS((col, row), 
                                           (col + xOff*2, row + yOff*2), 
                                           self.turn))

            case Mark.O:
                for i in range(4):
                    xOff = offsets[i][0]
                    yOff = offsets[i][1]

                if (self.inBounds(col + xOff, row + yOff) and
                    self.inBounds(col - xOff, row - yOff) and
                    self.getMark( col + xOff, row + yOff) == Mark.S and
                    self.getMark( col - xOff, row - yOff) == Mark.S):
                        
                    sosList.append(SOS((col + xOff, row + yOff), 
                                       (col - xOff, row - yOff), 
                                       self.turn))

        return sosList

    def reset(self, numCols: int = -1, numRows: int = -1):
        if numCols >= 3 and numRows >= 3:
            self.numCols = numCols
            self.numRows = numRows
        self.grid = [Mark.EMPTY] * (self.numCols * self.numRows)






