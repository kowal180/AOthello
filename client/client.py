#!/usr/bin/python

import sys
import json
import socket
from support import Board
from player import Player
from typing import List


def prepare_response(move: List[int]):
    """
    Function that takes a movement and converts it to a response
    :param move:
    :return:
    """
    response = '{}\n'.format(move).encode()
    print('sending {!r}'.format(response))
    return response


if __name__ == "__main__":
    """
    Define port and host from command line
    """
    port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
    host = sys.argv[2] if (
                len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()

    # Define the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # Try to connect to the port
        sock.connect((host, port))
        while True:
            # While receiving
            data = sock.recv(1024)
            if not data:
                print('connection to server closed')
                break
            # Get the data from the program in json
            json_data = json.loads(str(data.decode('UTF-8')))
            # Create the player for this board.
            # Player is passed a board object and the players number
            player = Player(Board(json_data['board']), json_data['player'])
            maxTurnTime = json_data['maxTurnTime']

            # Get the move from the player
            move = player.get_move()
            response = prepare_response(move)
            # Send the response to the socket
            sock.sendall(response)
    finally:
        sock.close()
