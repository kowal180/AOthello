"""
This file contains classes that support the analysis of the game
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Tuple, Iterator, Dict

# Declare the board size
BOARD_SIZE = (8, 8)


class Direction(Enum):
    """
    This class represents the 8 directions on the board.
    """
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    DOWN_LEFT = (1, -1)
    DOWN_RIGHT = (1, 1)
    UP_LEFT = (-1, -1)
    UP_RIGHT = (-1, 1)

    def get_opposite(self):
        """
        Get the opposite direction of where this direction is pointing
        :return: Opposite direction
        """
        return Direction((-1 * self.value[0], -1 * self.value[1]))


@dataclass()
class Position:
    """
    This class represents a single position on the board.
    Essentially, it extends a tuple to be (row, column) with other functions
    """

    row: int
    """Row of the point"""
    column: int
    """Column of the point"""

    def outside_board(self) -> bool:
        """
        Function that returns true if the position is outside the board
        :return:
        """
        return True if self.row > BOARD_SIZE[0] - 1 \
                       or self.row < 0 \
                       or self.column > BOARD_SIZE[1] - 1 \
                       or self.column < 0 \
            else False

    def __add__(self, other: Direction) -> "Position":
        """
        Wrap the '+' function for a position and a direction.
        Simplifies moving around the board from a position.
        :param other: Direction to move
        :return: New Position
        """
        new_pos = Position(self.row + other.value[0],
                           self.column + other.value[1])
        return new_pos if not new_pos.outside_board() else None

    # Define hash function and equality so can be used in dictionary
    def __hash__(self):
        """
        Return the hash of the tuple
        :return:
        """
        return hash((self.row, self.column))

    def __eq__(self, other: "Position") -> bool:
        """
        Define if two positions are equal
        :param other:
        :return:
        """
        if type(other) != type(self):
            return False
        return self.row == other.row and self.column == other.column


class Board:
    """
    Board will contain and process the information for the game board.
    It contains a the current score, the current tokens on the board,
    and the raw board.
    """

    def __init__(self, input_board: List[List[int]]):
        """Creates a board from the given JSON"""

        self.score: List[int] = [0, 0]
        """
        Current score of the game in a list format.
        Player 1 is the first score, Player 2 is the second score.
        """

        self.curr_tokens: Dict[Position, int] = {}
        """
        Current tokens on the board. Maps a position to a player.
        Using a dictionary to reduce the need to loop over a complete board.
        """

        self.raw_board: List[List[int]] = input_board
        """
        Raw board of the game status
        """
        # Store the tokens in the current tokens.
        # Loop over rows
        for row in range(len(input_board)):
            # loop over columns
            for column in range(len(input_board[row])):
                player = input_board[row][column]
                # If the position is not empty
                if player in [1, 2]:
                    # Add the point and add the score
                    self.curr_tokens[Position(row, column)] = player
                    self.score[player - 1] += 1

    def flip_token(self, position: Position, set_player: int) -> None:
        """
        Given a position, flip the token at that position.
        If token is off board, do nothing.
        :param position:
        :param set_player:
        :return:
        """
        # If the position exists, flip
        if not position.outside_board():
            self.score[set_player - 1] += 1
            if self.curr_tokens.get(position):
                self.score[set_player % 2] -= 1
            self.curr_tokens[position] = set_player
            self.raw_board[position.row][position.column] = set_player

    def find_neighbor_in_direction(self, position: Position,
                                   direction: Direction
                                   ) -> Optional[int]:
        """
        Given a position and direction, return the player in that direction.
        :param position:
        :param direction:
        :return:
        """
        new_pos = position + direction
        if not new_pos:
            return None
        if not self.curr_tokens.get(new_pos):
            return 0
        return self.curr_tokens.get(new_pos)

    def find_neighbor_players(
            self,
            position: Position
    ) -> Iterator[Tuple[Direction, int]]:
        """
        Given a position on the board, loop over all neighbors and
        return the player occupying the space in each direction
        :param position:
        :return:
        """
        # Loop over all directions
        for direction in Direction:
            # Yield if point exists:
            neighbor = self.find_neighbor_in_direction(position,
                                                       direction)
            if neighbor is not None:
                yield direction, neighbor

    def is_flankable(self,
                     player: int,
                     init_position: Position,
                     direction: Direction
                     ) -> Tuple[bool, List[Position]]:
        """Check a line of tokens and see if the line is flankable by a
        player. A line is flankable if it ends in its own color, and not
        a wall or blank space.
        If flankable, return a list of what would be flipped."""
        visited_positions = []
        curr_pos = init_position + direction
        if not curr_pos:
            return False, []
        # Loop while position is not outside board or not empty
        while not curr_pos.outside_board() \
                and self.curr_tokens.get(curr_pos):
            # If ends with same token, flank!
            if self.curr_tokens[curr_pos] == player:
                return True, visited_positions

            # else add the current position to the return
            visited_positions.append(curr_pos)
            # Move in the direction again
            curr_pos = curr_pos + direction
            if not curr_pos:
                return False, []
        # Else, not flankable
        return False, []

    def find_valid(self, curr_player: int) -> Iterator[Position]:
        """
        Find and return all valid positions on the board.
        :param curr_player:
        :return:
        """
        # First, find all open positions next to an opponent
        for position, player in self.curr_tokens.items():
            # If the token is the same as the current player, ignore
            if player == curr_player:
                continue
            # Loop over all neighbors
            for direction, neighbor in self.find_neighbor_players(position):
                # Ignore occupied spaces
                if neighbor != 0:
                    continue
                # Left with all unoccupied spaces next to an opponent
                # Check if the line created by the position can be flanked
                unoccupied_space = position + direction
                opposite_dir = direction.get_opposite()

                # If flankable, yield that location
                if self.is_flankable(curr_player,
                                     unoccupied_space,
                                     opposite_dir)[0]:
                    yield unoccupied_space

    def update_board(self, placed_position: Position,
                     player: int) -> None:
        """
        Given a new position, update a board and flip tokens
        :param placed_position:
        :param player:
        :return:
        """
        # Add new token and update raw board
        self.flip_token(placed_position, player)
        # Loop over all directions and find all tiles to flip
        tokens_to_flip = []
        for direction in Direction:
            flankable = self.is_flankable(player, placed_position, direction)
            if flankable[0]:
                # Loop over spaces now flanked
                for flip in flankable[1]:
                    tokens_to_flip.append(flip)
        for token in tokens_to_flip:
            self.flip_token(token, player)

    def create_updated_board(self, placed_position: Position,
                             player: int) -> "Board":
        """
        Given a new position, return a new updated board with tiles flipped
        """
        new_board = Board(self.raw_board)
        new_board.update_board(placed_position, player)
        return new_board
