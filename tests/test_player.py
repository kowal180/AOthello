"""
This file contains tests for functions in support.py.
"""

import unittest
from support import Board
from player import Player


class TestPlayer(unittest.TestCase):
    def setUp(self) -> None:
        self.input_board = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 1, 0, 0, 0, 0, 0],
                            [0, 1, 2, 0, 0, 2, 0, 0],
                            [0, 2, 1, 1, 1, 0, 0, 0],
                            [0, 1, 1, 1, 1, 0, 0, 0],
                            [0, 1, 1, 2, 2, 0, 0, 0],
                            [0, 1, 1, 2, 1, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]]

        self.player_num = 2

    def test_constructor(self) -> None:
        Player(Board(self.input_board), self.player_num)

    def test_get_move(self):
        player = Player(Board(self.input_board), self.player_num)
        self.assertEqual(player.get_move(), [7, 0])


if __name__ == '__main__':
    unittest.main()
