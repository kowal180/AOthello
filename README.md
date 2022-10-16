# AOthello by Nathan Kowalski

Hello! My name is Nathan Kowalski.
Welcome to my submission for this years Atomic Accelerator challenge!

This submission was made in Python and extends the provided `python_sdk`

## Notes

Here's a little information about how my submission is organized:
- client.py = a slightly modified version of the client.py file provided
- support.py = a file that contains support classes for the system.
- player.py = a file containing the player. The player pulls together all the classes to make the 'brains' of the operation.
- /tests = a directory containing tests for all functions used

## Future Improvement

Currently, the player for this game uses an expectimax with a self-provided 
strategy. This yields a somewhat "smarter" player, however it can fail if the 
strategy is not sufficiently tweaked. 

One improvement that was considered was making the AI find its own weights.
This would involve storing a weight table in a file (such as a csv), updating 
for each game, and then letting the game play a random player for a many, many
iterations.

Due to time constraints, this was not the strategy chosen, but serves as a nice
improvement in the future.


## License

Copyright © 2018

Distributed under the Eclipse Public License either version 1.0 or (at
your option) any later version.
