#! /usr/bin/python3

import platform   # operating system platform

import checkerboard
import charIO  # character IO

import abstractstrategy
import redis


class Strategy(abstractstrategy.Strategy):
    "Human player"

    def play(self, board, hints=True):
        """"play - make a move
        Given a board, find a move and return a tuple of the new board
        and the action that created it.  If no moves are possible or the
        player forfeits, return the original board and the empty move []\

        Hints provides the user with a list of possible moves to choose
        from and is currently the only way to use this function.
        If you have problems with the unbuffered read charIO.getch(),
        use charIO.getchBuffered() which reads input in a buffered
        manner (you must press carriage return).  The charIO module has
        only been tested on CentOS 6.6 linux and Windows.  It will work
        with PyCharm but you will may need to set the debug/run configuration
        to emulate a terminal in console output.
        """
        actions = board.get_actions(self.maxplayer)

        forfeit = "F"  # Human choice for forfeiting

        if actions:
            if hints:
                # Show actions labeled a, b, c, etc.
                letter_a = ord('a')  # get encoding for "a"
                letters = [chr(letter_a + x) for x in range(len(actions))]
                for (action, letter) in zip(actions, letters):
                    print("%s: %s" % (letter, board.get_action_str(action)))

                # Read the players choice and convert to action
                print("%s move, choose by letter or F to forfeit: " %
                      (self.maxplayer), end=' ')
                letters.append(forfeit)
                choice = charIO.getch()
                print("You've chosen: ", choice)
                print(choice)
                while choice not in letters:
                    choice = charIO.getch()

                # Pick action (None if weak-minded human forfeited)
                action = actions[ord(
                    choice)-letter_a] if choice != forfeit else None

            else:
                """UI Implementaion"""

        else:
            action = []  # No possible actions

        # Execute human move
        if not action:
            newboard = board
        else:
            newboard = board.move(action)
        return (newboard, action)

    def utility(self, state):
        pass  # Human uses gray matter here...
