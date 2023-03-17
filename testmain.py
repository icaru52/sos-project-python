#!/usr/bin/env python3

# File: testmain.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

from enum import Enum
from board import Board, Mark

if __name__ == "__main__":
    board = Board(8, 8)

    print(board.__repr__())

    board.make_move(0, 0, Mark.S)
    board.make_move(1, 1, Mark.O)
    board.make_move(2, 2, Mark.S)
    board.make_move(0, 1, Mark.O)
    board.make_move(0, 2, Mark.S)
    board.make_move(1, 2, Mark.O)

    print(board)
    #print(board.sos_list)
    for i in board.sos_list: print(i)


