from support import Board, Position
from queue import PriorityQueue
from typing import Optional, List, Tuple, Iterator, Dict

MAX_DEPTH: int = 10
CORNERS = [
    Position(0, 0),
    Position(0, 7),
    Position(7, 7),
    Position(7, 0)
]
X_SQUARES = [
    Position(1, 0),
    Position(1, 1),
    Position(0, 1),
    Position(6, 1),
    Position(6, 0),
    Position(7, 1),
    Position(0, 6),
    Position(1, 6),
    Position(1, 7),
    Position(6, 6),
    Position(6, 7),
    Position(7, 6)
]
EDGES = [Position(row, col) for row in range(0, 7) for col in [0, 7]] + [
    Position(row, col) for row in [0, 7] for col in range(0, 7)]
CORNER_REWARD = 100
X_SQUARE_REWARD = -10
EDGES_REWARD = 5
NUM_MOVES_MULTIPLIER = 5
REWARD_SCORE_DIFF = 2


class Player:
    """
    The player class is the 'brains' of the operation.
    It will hold the board information and decide where to place pieces next
    """

    def __init__(self, board: Board, player_number: int):
        self.board = board
        self.player_num = player_number
        self.fringe: List[Tuple[float, Position]]

    def get_move(self) -> list:
        """
        Get move will determine the next move for the player.
        This will be done using the heuristics below.
        """
        # Get all possible locations for next move.
        # Add a value to the possible location to determine which is best
        fringe = [[0, pos] for pos in self.board.find_valid(self.player_num)]

        # Get the value for all possible moves
        for move in fringe:
            move[0] = self.compute_val(move[1], self.board, 0, self.player_num)

        # Return the best move
        best_move = max(fringe, key=lambda x: x[0])
        return [best_move[1].row, best_move[1].column]

    def compute_val(self,
                    position: Position,
                    board: Board,
                    depth: int,
                    curr_player: int) -> int:
        """
        Recursive function to compute the value of a move. This method is
        based on an expectimax search, which assumes the opponent is random.
        This makes the bot more risky, but better models the situation here.

        During the bot's turn, it will evaluate how good the board looks and
        report that number. Then, it will add the max of its children and
        recursively call the function.
        On the opponent turn, we assume the bot is random. Therefore, the value
        is computed to be the average of its childrens value (computed
        recursively)

        Will recurse to a depth of MAX_DEPTH.
        :param position:
        :param board:
        :param depth:
        :param curr_player:
        :return:
        """
        # initialize the value of at 0
        value = 0
        # Find the opponents number and possible moves
        # opponent = self.player_num % 2 + 1
        opponent = curr_player % 2 + 1
        opponent_moves = list(board.find_valid(opponent))

        # Get the updated board from the move
        new_board = board.create_updated_board(position, curr_player)

        # See if max depth is reached or opponent has no moves
        stop = depth >= MAX_DEPTH or len(opponent_moves) == 0

        # If the current player in the recursion is the player
        if curr_player == self.player_num:
            value += self._compute_board_value(
                curr_player,
                opponent,
                position,
                opponent_moves,
                board,
                new_board
            )
            # If not at max_depth
            if not stop:
                value += max([
                    self.compute_val(move, new_board, depth, opponent)
                    for move in opponent_moves
                ])
        # Else, if the current player is not the bot and still iterating
        elif not stop:
            value += 1 / len(opponent_moves) * sum([
                self.compute_val(move, new_board, depth, opponent)
                for move in opponent_moves
            ])
        #
        return value

    def _compute_board_value(self,
                             curr_player: int,
                             opponent: int,
                             position: Position,
                             opponent_moves: List[Position],
                             curr_board: Board,
                             new_board: Board):
        """
        This helper function computes the value of a singular state of the
        board. These strategies were chosen based on the recommendations from
        UltraBoardGames.com, and converted into arbitrary values
        :param position: Current choice being decided on
        :param opponent_moves: The moves the opponent can make
        :param curr_board: The current board
        :param new_board: The board after the move is made
        :return:
        """
        value = 0

        # First, judge how good the current move is based on if its a
        # corner, edge, or an 'X square'
        if position in CORNERS:
            value += CORNER_REWARD
        elif position in X_SQUARES:
            value += X_SQUARE_REWARD
        elif position in EDGES:
            value += EDGES_REWARD

        # Then, find all the number of opponent moves that can be made with
        # this choice.
        value -= 10 * len(opponent_moves)

        # Finally, compute the change in score for the move
        curr_score = curr_board.score[curr_player - 1] - \
                     curr_board.score[opponent - 1]
        score_on_update = new_board.score[curr_player - 1] - \
                          curr_board.score[opponent - 1]
        value += REWARD_SCORE_DIFF * (score_on_update - curr_score)

        return value
