# File: board.py
# Project: 2023 Spring Semester SOS Project
# Programmer: Ian Rowse <imrnnc@umsystem.edu>

import unittest
import board

class TestMark(unittest.TestCase):

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

    def test_tuple(self):
        board.SOS((0, 0), (3, 3), 0)

    def test_list(self):
        board.SOS([0, 0], [3, 3], 0)

    def test_point_dimensions(self):
        self.assertRaises(board.SOS((0, 0), (3, 3, 3), 0), ValueError)

    def test_same_points(self):
        self.assertRaises(board.SOS((0, 0), (0, 0), 0), ValueError)

    def test_id_lt_zero(self):
        self.assertRaises(board.SOS((0, 0), (3, 3), -1), ValueError)


class TestPlayer(unittest.TestCase):

    def test_name(self):
        self.assertEqual(board.Player("Test").name, "Test")

    def test_default_hue(self):
        self.assertEqual(board.Player("Test").hue, 0)

    def test_set_hue(self):
        self.assertEqual(board.Player("Test", 180).hue, 180)

    def test_initial_score(self):
        self.assertEqual(board.Player("Test").score, 0)


class TestBoard(unittest.TestCase):
    
    def test_create_board_default_size(self):
        self.assertEqual(board.Board().grid, [board.Mark.EMPTY] * (8 * 8))

    def test_create_board_min_size(self):
        self.assertEqual(board.Board(3, 3).grid, [board.Mark.EMPTY] * (3 * 3))

    def test_create_board_lt_min_size(self):
        self.assertEqual(board.Board(2, 2).grid, [board.Mark.EMPTY] * (8 * 8))

    #def test_create_board_max_size(self):
    #    self.assertEqual(board.Board().grid, [board.Mark.EMPTY] * (8 * 8))

    def test_create_board_default_players(self):
        self.assertEqual(board.Board().players, 
                         [Player("One", 0), Player("Two", 240)])

    def test_create_board_three_players(self):
        test = [Player("Tom", 60), Player("Dick", 120), Player("Harry", 180)]
        self.assertEqual(board.Board(8, 8, test).players, test)


if __name__ == '__main__':
    unittest.main()

