# File: board.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

from enum import Enum

class Mark(Enum):
    EMPTY = 0
    S     = 1
    O     = 2

class Board:
    def __init__(self, numCols=8, numRows=8):
        self.numCols = numCols
        self.numRows = numRows
        self.grid = [Mark.EMPTY] * (numCols * numRows)

    def inBounds(self, col, row):
        return (0 <= col < self.numCols and
                0 <= row < self.numRows)

    def outOfBounds(self, col, row):
        return not self.inBounds(col, row)

    # Assumes that col and row are in bounds
    def getMark(self, col, row):
        return self.grid[(row * self.numCols) + col]

    # Assumes that col and row are in bounds
    def setMark(self, col, row, mark):
        self.grid[(row * self.numCols) + col] = mark

    def clear(self):
        self.grid = [Mark.EMPTY] * (numCols * numRows)

    # Assumes that col and row are in bounds
    def makeMove(self, col, row, mark):
        if mark != Mark.EMPTY and self.getMark(col, row) == Mark.EMPTY:
            self.setMark(col, row, mark)

    # Assumes that col and row are in bounds
    # Assumes that the space is empty
    def createsSOS(self, col, row, mark):
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

                        sosList.append((col, row, col + xOff*2, row + yOff*2))

            case Mark.O:
                for i in range(4):
                    xOff = offsets[i][0]
                    yOff = offsets[i][1]

                if (self.inBounds(col + xOff, row + yOff) and
                    self.inBounds(col - xOff, row - yOff) and
                    self.getMark( col + xOff, row + yOff) == Mark.S and
                    self.getMark( col - xOff, row - yOff) == Mark.S):
                        
                    sosList.append((col + xOff, row + yOff, 
                                    col - xOff, row - yOff))

        return sosList

    def reset(self, numCols=-1, numRows=-1):
        if numCols >= 3 and numRows >= 3:
            self.numCols = numCols
            self.numRows = numRows
        self.grid = [Mark.EMPTY] * (numCols * numRows)






