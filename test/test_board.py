# File: test_board.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

"""tests for the SOS board class"""

import unittest
from src import board

class TestMark(unittest.TestCase):
    """tests for the Mark Enum"""

    def test_s_lt_o(self):
        self.assertFalse(board.Mark.S < board.Mark.O)

    def test_o_lt_s(self):
        self.assertFalse(board.Mark.O < board.Mark.S)

    def test_s_gt_o(self):
        self.assertFalse(board.Mark.S > board.Mark.O)

    def test_o_gt_s(self):
        self.assertFalse(board.Mark.O > board.Mark.S)

    def test_s_le_o(self):
        self.assertFalse(board.Mark.S <= board.Mark.O)

    def test_o_le_s(self):
        self.assertFalse(board.Mark.O <= board.Mark.S)

    def test_s_ge_o(self):
        self.assertFalse(board.Mark.S >= board.Mark.O)

    def test_o_ge_s(self):
        self.assertFalse(board.Mark.O >= board.Mark.S)

    def test_empty_gt_none(self):
        self.assertTrue(board.Mark.EMPTY > board.Mark.NONE)


class TestSOS(unittest.TestCase):
    """tests for the SOS helper class"""

    """
    def test_tuple(self):
        board.SOS((0, 0), (3, 3), 0)

    def test_list(self):
        board.SOS([0, 0], [3, 3], 0)
    """

    def test_point_nonzero(self):
        with self.assertRaises(ValueError):
            board.SOS((), (), 0)

    def test_point_dimensions(self):
        with self.assertRaises(ValueError):
            board.SOS((0, 0), (3, 3, 3), 0)

    def test_same_points(self):
        with self.assertRaises(ValueError):
            board.SOS((0, 0), (0, 0), 0)

    def test_id_lt_zero(self):
        with self.assertRaises(ValueError):
            board.SOS((0, 0), (3, 3), -1)


class TestPlayer(unittest.TestCase):
    """tests for the Player helper class"""

    def test_name(self):
        self.assertEqual(board.Player("Test").name, "Test")

    def test_default_hue(self):
        self.assertEqual(board.Player("Test").hue, 0)

    def test_set_hue(self):
        self.assertEqual(board.Player("Test", 180).hue, 180)

    def test_initial_score(self):
        self.assertEqual(board.Player("Test").score, 0)


class TestBoard(unittest.TestCase):
    """tests for the core SOS Board class"""

    def test_create_board_default_size(self):
        self.assertEqual(board.Board().grid, [board.Mark.EMPTY] * (8 * 8))

    def test_create_board_min_size(self):
        self.assertEqual(board.Board(3, 3).grid, [board.Mark.EMPTY] * (3 * 3))

    def test_create_board_lt_min_size(self):
        with self.assertRaises(ValueError):
            board.Board(2, 2)

    #def test_create_board_max_size(self):
    #    self.assertEqual(board.Board().grid, [board.Mark.EMPTY] * (8 * 8))

    def test_create_board_default_players(self):
        test_board = board.Board()

        self.assertEqual(test_board.players[0].name, "Player One")
        self.assertEqual(test_board.players[0].hue, 0)
        self.assertEqual(test_board.players[0].score, 0)

        self.assertEqual(test_board.players[1].name, "Player Two")
        self.assertEqual(test_board.players[1].hue, 240)
        self.assertEqual(test_board.players[1].score, 0)

        with self.assertRaises(IndexError):
            test_board.players[2]

    def test_create_board_three_players(self):
        test_board = board.Board(8, 8, [board.Player("Tom",    60),
                                        board.Player("Dick",  120),
                                        board.Player("Harry", 180)])

        self.assertEqual(test_board.players[0].name, "Tom")
        self.assertEqual(test_board.players[0].hue, 60)
        self.assertEqual(test_board.players[0].score, 0)

        self.assertEqual(test_board.players[1].name, "Dick")
        self.assertEqual(test_board.players[1].hue, 120)
        self.assertEqual(test_board.players[1].score, 0)

        self.assertEqual(test_board.players[2].name, "Harry")
        self.assertEqual(test_board.players[2].hue, 180)
        self.assertEqual(test_board.players[2].score, 0)

        with self.assertRaises(IndexError):
            test_board.players[3]

    def test_create_board_zero_players(self):
        with self.assertRaises(ValueError):
            board.Board(8, 8, [])

    def test_in_bounds(self):
        width, height = 3, 3
        test_board = board.Board(width, height)

        for y in range(width):
            for x in range(height):
                self.assertTrue(test_board.in_bounds((x, y)))
                self.assertFalse(test_board.out_of_bounds((x, y)))

    def test_out_of_bounds(self):
        width, height = 3, 3
        test_board = board.Board(width, height)

        for y in range(-1, width+1):
            self.assertTrue(test_board.out_of_bounds((-1, y)))
            self.assertFalse(test_board.in_bounds((-1, y)))

            self.assertTrue(test_board.out_of_bounds((width, y)))
            self.assertFalse(test_board.in_bounds((width, y)))

        for x in range(0, height):
            self.assertTrue(test_board.out_of_bounds((x, -1)))
            self.assertFalse(test_board.in_bounds((x, -1)))

            self.assertTrue(test_board.out_of_bounds((x, height)))
            self.assertFalse(test_board.in_bounds((x, height)))

    def test_get_mark_in_bounds(self):
        width, height = 3, 3
        test_board = board.Board(width, height)

        for y in range(width):
            for x in range(height):
                self.assertEqual(test_board.get_mark((x, y)), board.Mark.EMPTY)

    def test_get_mark_out_of_bounds(self):
        width, height = 3, 3
        test_board = board.Board(width, height)

        for y in range(-1, width+1):
            self.assertEqual(test_board.get_mark((-1, y)), board.Mark.NONE)
            self.assertEqual(test_board.get_mark((width, y)), board.Mark.NONE)

        for x in range(0, height):
            self.assertEqual(test_board.get_mark((x, -1)), board.Mark.NONE)
            self.assertEqual(test_board.get_mark((x, height)), board.Mark.NONE)


    def test_set_mark_in_bounds(self):
        width, height = 3, 3
        test_board = board.Board(width, height)

        for y in range(width):
            for x in range(height):
                test_board.set_mark((x, y), board.Mark.S)
                self.assertEqual(test_board.get_mark((x, y)), board.Mark.S)

    def test_set_mark_out_of_bounds(self):
        with self.assertRaises(IndexError):
            board.Board().set_mark((-1, 0), board.Mark.S)

    def test_set_mark_none(self):
        with self.assertRaises(ValueError):
            board.Board().set_mark((0, 0), board.Mark.NONE)

    def test_set_mark_mark_count_increment(self):
        width, height = 3, 3
        test_board = board.Board(width, height)

        count = 0

        for y in range(width):
            for x in range(height):
                test_board.set_mark((x, y), board.Mark.S)
                count += 1
                self.assertEqual(test_board.mark_count, count)

        for y in range(width):
            for x in range(height):
                test_board.set_mark((x, y), board.Mark.EMPTY)
                count -= 1
                self.assertEqual(test_board.mark_count, count)

    def test_clear_board(self):
        width, height = 3, 3
        test_board = board.Board(width, height)

        test_board.set_mark((0, 0), board.Mark.S)
        test_board.set_mark((1, 1), board.Mark.O)
        test_board.set_mark((2, 2), board.Mark.S)

        test_board.clear()

        self.assertEqual(test_board.grid, [board.Mark.EMPTY] * (width * height))
        self.assertEqual(test_board.mark_count, 0)
        self.assertEqual(test_board.sos_list, [])

    def test_make_move_empty(self):
        with self.assertRaises(ValueError):
            board.Board().make_move((0, 0), board.Mark.EMPTY)

    def test_make_move_filled_cell(self):
        width, height = 3, 3
        test_board = board.Board(width, height)

        test_board.set_mark((0, 0), board.Mark.S)

        self.assertFalse(test_board.make_move((0, 0), board.Mark.O))

    def test_make_move_sos(self):
        width, height = 3, 3
        test_board = board.Board(width, height)

        test_board.make_move((0, 0), board.Mark.S) # player 0
        test_board.make_move((1, 1), board.Mark.O) # player 1
        test_board.make_move((2, 2), board.Mark.S) # player 0

        self.assertEqual(test_board.sos_list[0].p1, (2, 2))
        self.assertEqual(test_board.sos_list[0].p2, (0, 0))
        self.assertEqual(test_board.sos_list[0].player_id, 0)

        self.assertEqual(test_board.players[0].score, 1)

    def test_make_move_turn_incement(self):
        width, height = 3, 3
        test_board = board.Board(width, height)

        test_board.make_move((0, 0), board.Mark.S)
        self.assertEqual(test_board.turn, 1)

        test_board.make_move((1, 1), board.Mark.O)
        self.assertEqual(test_board.turn, 0)

    """
    def test_creates_sos_s_off_edge(self):
        width, height = 3, 3
        test_board = board.Board(width, height)

        test_board.set_mark((1, 1), board.Mark.S)

    def test_creates_sos_o_off_edge(self):
        width, height = 3, 3
        test_board = board.Board(width, height)

        test_board.set_mark()
    """


if __name__ == "__main__":
    unittest.main()

