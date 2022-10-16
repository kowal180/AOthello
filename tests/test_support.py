"""
This file contains tests for functions in support.py.
"""

import unittest
from client.support import Position, Direction, Board


class TestPosition(unittest.TestCase):
    """Tests for the Position class"""

    def test_outside_board(self):
        inside_board = [Position(0, 0),
                        Position(0, 7),
                        Position(7, 7),
                        Position(7, 0)]
        outside_board = [Position(-1, 0),
                         Position(0, 8),
                         Position(10, 10),
                         Position(7, -1)]

        for point in inside_board:
            self.assertFalse(point.outside_board())

        for point in outside_board:
            self.assertTrue(point.outside_board())

    def test_add_point_and_direction(self):
        all_dir = Position(1, 1)
        self.assertEqual(all_dir + Direction.UP, Position(0, 1))
        self.assertEqual(all_dir + Direction.DOWN, Position(2, 1))
        self.assertEqual(all_dir + Direction.LEFT, Position(1, 0))
        self.assertEqual(all_dir + Direction.RIGHT, Position(1, 2))
        self.assertEqual(all_dir + Direction.UP_RIGHT, Position(0, 2))
        self.assertEqual(all_dir + Direction.UP_LEFT, Position(0, 0))
        self.assertEqual(all_dir + Direction.DOWN_LEFT, Position(2, 0))
        self.assertEqual(all_dir + Direction.DOWN_RIGHT, Position(2, 2))

        off_board1 = Position(0, 0)
        off_board2 = Position(7, 7)
        self.assertEqual(off_board1 + Direction.UP_LEFT, None)
        self.assertEqual(off_board1 + Direction.UP, None)
        self.assertEqual(off_board1 + Direction.LEFT, None)
        self.assertEqual(off_board2 + Direction.DOWN, None)
        self.assertEqual(off_board2 + Direction.DOWN_RIGHT, None)
        self.assertEqual(off_board2 + Direction.RIGHT, None)

    def test_opposite_dir(self):
        self.assertEqual(Direction.UP.get_opposite(), Direction.DOWN)
        self.assertEqual(Direction.DOWN.get_opposite(), Direction.UP)
        self.assertEqual(Direction.LEFT.get_opposite(), Direction.RIGHT)
        self.assertEqual(Direction.RIGHT.get_opposite(), Direction.LEFT)
        self.assertEqual(Direction.DOWN_LEFT.get_opposite(), Direction.UP_RIGHT)
        self.assertEqual(Direction.DOWN_RIGHT.get_opposite(), Direction.UP_LEFT)
        self.assertEqual(Direction.UP_LEFT.get_opposite(), Direction.DOWN_RIGHT)
        self.assertEqual(Direction.UP_RIGHT.get_opposite(), Direction.DOWN_LEFT)


class TestBoard(unittest.TestCase):
    """Test all functions for the board"""

    def setUp(self) -> None:
        self.input_board = [[0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 1, 2, 0, 0, 0],
                            [0, 0, 0, 2, 1, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]]

        self.pos1 = Position(3, 3)
        self.pos2 = Position(3, 4)
        self.pos3 = Position(4, 3)
        self.pos4 = Position(4, 4)

        self.init_curr_tokens = {self.pos1: 2,
                                 self.pos2: 2,
                                 self.pos3: 2,
                                 self.pos4: 1}

    def test_constructor(self):
        board = Board(self.input_board)

        self.assertEqual(board.curr_tokens, {
            self.pos1: 1,
            self.pos2: 2,
            self.pos3: 2,
            self.pos4: 1
        })
        self.assertEqual(board.score, [2, 2])

    def test_flip_token(self):
        board = Board(self.input_board)
        board.flip_token(Position(3, 3), 2)
        self.init_curr_tokens[Position(3, 3)] = 2
        self.assertEqual(board.curr_tokens, self.init_curr_tokens)
        self.assertEqual(board.raw_board,
                         [[0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 2, 1, 2, 0, 0, 0],
                          [0, 0, 0, 2, 1, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0]])

        board.flip_token(self.pos1, 2)
        self.init_curr_tokens[Position(3, 3)] = 2
        self.assertEqual(board.curr_tokens, self.init_curr_tokens)
        self.assertEqual(board.raw_board,
                         [[0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 2, 1, 2, 0, 0, 0],
                          [0, 0, 0, 2, 1, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0]])

    def test_neighbor_in_direction(self):
        board = Board(self.input_board)

        self.assertEqual(
            board.find_neighbor_in_direction(self.pos1, Direction.DOWN_RIGHT),
            1
        )
        self.assertEqual(
            board.find_neighbor_in_direction(self.pos2, Direction.DOWN_RIGHT),
            0
        )
        self.assertEqual(
            board.find_neighbor_in_direction(self.pos3, Direction.RIGHT),
            1
        )
        self.assertEqual(
            board.find_neighbor_in_direction(self.pos4, Direction.LEFT),
            2
        )
        self.assertEqual(
            board.find_neighbor_in_direction(Position(7, 7), Direction.RIGHT),
            None
        )

    def test_find_neighbors(self):
        board = Board(self.input_board)

        pos1_neighbors = list(board.find_neighbor_players(self.pos1))
        self.assertEqual(pos1_neighbors,
                         [
                             (Direction.UP, 0),
                             (Direction.DOWN, 2),
                             (Direction.LEFT, 0),
                             (Direction.RIGHT, 2),
                             (Direction.DOWN_LEFT, 0),
                             (Direction.DOWN_RIGHT, 1),
                             (Direction.UP_LEFT, 0),
                             (Direction.UP_RIGHT, 0),
                         ])
        corner_neighbors = list(board.find_neighbor_players(Position(0, 0)))
        self.assertEqual(corner_neighbors,
                         [
                             (Direction.DOWN, 0),
                             (Direction.RIGHT, 0),
                             (Direction.DOWN_RIGHT, 0),
                         ])

    def test_is_flankable(self):
        board = Board(self.input_board)
        # Test vertical, horizontal, and diagonal
        self.assertEqual(
            board.is_flankable(2, self.pos1 + Direction.LEFT, Direction.RIGHT),
            (True, [self.pos1])
        )
        self.assertEqual(
            board.is_flankable(2, self.pos1 + Direction.UP, Direction.DOWN),
            (True, [self.pos1])
        )
        self.assertEqual(board.is_flankable(2, self.pos1 + Direction.UP_LEFT,
                                            Direction.DOWN_RIGHT),
                         (False, []))
        board.curr_tokens[Position(2, 2)] = 2
        self.assertEqual(board.is_flankable(2, self.pos4 + Direction.DOWN_RIGHT,
                                            Direction.UP_LEFT),
                         (True, [self.pos4, self.pos1]))

    def test_find_valid(self):
        board = Board(self.input_board)
        self.assertEqual(list(board.find_valid(1)),
                         [
                             Position(row=2, column=4),
                             Position(row=3, column=5),
                             Position(row=5, column=3),
                             Position(row=4, column=2)
                         ]
                         )
        self.assertEqual(list(board.find_valid(2)),
                         [
                             Position(row=2, column=3),
                             Position(row=3, column=2),
                             Position(row=5, column=4),
                             Position(row=4, column=5)
                         ]
                         )
        # Check when at edge of board
        board.curr_tokens[Position(3, 5)] = 1
        board.curr_tokens[Position(3, 6)] = 1
        board.curr_tokens[Position(3, 7)] = 1
        self.assertEqual(list(board.find_valid(1)),
                         [
                             Position(row=2, column=4),
                             Position(row=5, column=3),
                             Position(row=4, column=2)
                         ]
                         )

    def test_create_updated_board(self):
        board = Board(self.input_board)

        new_board = board.create_updated_board(self.pos1 + Direction.LEFT,
                                               2)
        self.assertEqual(new_board.raw_board,
                         [[0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 2, 2, 2, 0, 0, 0],
                          [0, 0, 0, 2, 1, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0]])
        self.assertEqual(new_board.curr_tokens,
                         {self.pos1: 2,
                          self.pos2: 2,
                          self.pos3: 2,
                          self.pos4: 1,
                          self.pos1 + Direction.LEFT: 2})
        self.assertEqual(new_board.score,
                         [1, 4])
        new_board.update_board(self.pos1 + Direction.UP_LEFT, 1)
        self.assertEqual(new_board.raw_board,
                         [[0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 1, 0, 0, 0, 0, 0],
                          [0, 0, 2, 1, 2, 0, 0, 0],
                          [0, 0, 0, 2, 1, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0]])


if __name__ == '__main__':
    unittest.main()
