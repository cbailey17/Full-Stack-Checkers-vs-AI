#! /usr/bin/python3

# Game representation and mechanics
from __future__ import print_function
from statistics import mean
from timer import Timer
import checkerboard

import imp
import ai
import human
import sys


def Game(red=ai.Strategy, black=human.Strategy,
         maxplies=2, init=None, verbose=True, firstmove=0):
    """Game function for playing checkers"""
    # Initialize variables and data structures
    movenum, lastcap, pawn_move, count = 1, 0, 0, 0
    movetimes = [[], []]
    players = ['r', 'b']
    # Define board and instances of the strategy and dictionarys for the players
    board = checkerboard.CheckerBoard()
    redplayer, blackplayer = red(
        'r', board, maxplies),  black('b', board, maxplies)
    player_strategies = {'r': redplayer, 'b': blackplayer}
    strategies = {'r': "AI", 'b': "Human"}

    # print out games initial information
    print("Invoked Game(", "red=", redplayer.__module__, ".Strategy", ",", "black=", blackplayer.__module__,
          ".Strategy", ",", "maxplies =", maxplies, ")\n\n")
    print("How about a nice game of checkers?")

    # Determine which player starts the game
    current_player = players[firstmove]

    tm = Timer()  # Timer for game in minutes
    time_min = 0
    finished = False
    while not finished:  # While game is not finished keep looping
        # Check if the game is over
        terminal, winner = board.is_terminal()
        if terminal:
            gameover(movetimes, winner, time_min)
            return

        print("Player", current_player, "turn")
        print(board)
        if current_player == players[0]:
            print(current_player, "thinking using",
                  strategies.get(current_player), "strategy...")

        t = Timer()  # Timer for player moves
        move = player_strategies.get(current_player).play(
            board)  # get action from current player strategy
        piece = board.get(move[1][0][0], move[1][0][1])
        # determine if the move is from a pawn
        if board.ispawn(piece):
            pawn_move = 0
        else:
            pawn_move += 1

        # get action string then display data
        action_str = board.get_action_str(move[1])
        if len(action_str) > 23:  # Check if there is a capture
            lastcap = 0
        else:
            lastcap += 1

        print("move", movenum, "by", current_player,
              ":", action_str, " Result:")
        board = board.move(move[1])

        movenum += 1
        ts = round(t.elapsed_s(), 2)
        if current_player == players[0]:
            movetimes[0].append(ts)
        else:
            movetimes[1].append(ts)
        time_min = round(tm.elapsed_min(), 2)

        # Display data from the action and about the state of the game
        print(board)
        print("Pawn/King count: r", board.get_pawnsN()[0], "R", board.get_kingsN()[0],
              "b", board.get_pawnsN()[1], "B", board.get_kingsN()[
            1], "Time - move:",
            ts, "s", "game", time_min, "m")
        print("Moves since last capture", lastcap,
              "last pawn advance", pawn_move, "\n")
        current_player = board.other_player(current_player)


def gameover(movetimes, winner, time_min):
    """Check if the game is over"""
    print("The game is finished")
    if winner is not None:
        print("player", winner, "wins")
        return
    else:
        print("The game is a draw")
        print("r average move time", mean(movetimes[0]))
        print("b average move time", mean(movetimes[1]))
        print("Total game time", time_min)
    return


# if __name__ == "__main__":
    # Game(init=boardlibrary.boards["multihop"])
    # Game(init=boardlibrary.boards["StrategyTest1"])
    # Game(init=boardlibrary.boards["EndGame1"], firstmove = 1)
    # Game()
