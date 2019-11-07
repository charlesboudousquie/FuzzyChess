Fuzzy Evaluation of Chess using Alpha-Beta Pruning
--------------------------------------------------
Project by Lux Cardell, Barrett Karstens, and Charles Boudousquie

This project was written using Python 3.7 and python-chess 0.28.3.

To perform first-time setup, run "make setup". This will install the chess library for python.

To run the program, run "make run".

The program will print the chess board and a list of valid moves and prompt for input. Typing a move from the list and pressing enter will make the move, print out the board, and calculate the responding move.

Other valid input options are:
'help': displays the help menu
'quit': forfeits the game
'reset': resets the board to the start of the game
'mam': sets AI to use a Mamdani fuzzy system
'ts': sets AI to use a Takagi-Sugeno fuzzy system

By default, the application uses a Takagi-Sugeno fuzzy system. Switching to a Mamdani fuzzy system will cause a noticeable change in calculation time.

