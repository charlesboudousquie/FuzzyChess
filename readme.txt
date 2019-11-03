Fuzzy Evaluation of Chess using Alpha-Beta Pruning
Project by Lux Cardell, Barrett Karstens, and Charles Boudousquie

This project was written using Python 3.7 and python-chess 0.28.3.

To perform first-time setup, run "make setup". This will install the chess library for python.

To run the program, run "make run".

Our code does not currently work as intended. We have implemented and tested both Mamdani and Takagi-Sugeno fuzzy systems, but the alpha-beta pruning is currently in progress. Given the difficulties caused by illness, we have not had the time to fully debug the system.

We are submitting this as a work in progress, and have asked for an extension.


DISCOVERIES:

In the first few moves of the game it is hard to evaluate the quality of our system. Since the neither player can immediately interact with the other, the fuzzy system needs something to handle the opening moves. With a deeper search tree it would be possible to get past this. Unfortunately due to the nature of Python as a scripting language, deeper search takes significant processing time.
