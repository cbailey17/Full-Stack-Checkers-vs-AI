#! /usr/bin/python3
"""
@author: Cameron Bailey
"""

# Game representation and mechanics
from __future__ import print_function
from statistics import mean
from timer import Timer
import checkerboard

import imp
import ai
import human
import sys


board = checkerboard.CheckerBoard()
redplayer = ai.Strategy('r', board, maxplies=2)
blackplayer = human.Strategy('b', board, maxplies=2)
player_strategies = {'r': redplayer, 'b': blackplayer}
strategies = {'r': "AI", 'b': "Human"}
players = ['r', 'b']
current_player = players[0]
movenum, lastcap, pawn_move, count = 1, 0, 0, 0


def checkTerminal():
    terminal, winner = board.is_terminal()
    if terminal:
        gameover(winner)
        return


def makeHumanMove():
    print("Changing state of board for humans move...")
    current_player = players[1]
    move = player_strategies.get(current_player).play(
        board)  # get action from current player strategy
    piece = board.get(move[1][0][0], move[1][0][1])

    if board.ispawn(piece):
        pawn_move = 0
    else:
        pawn_move += 1

    action_str = board.get_action_str(move[1])
    if len(action_str) > 23:  # Check if there is a capture
        lastcap = 0
    else:
        lastcap += 1

    board = board.move(move[1])
    movenum += 1

    print(board)


def getAIMove():
    """ Function made for a UI to play human vs AI"""
    board = checkerboard.CheckerBoard()
    redplayer = human.Strategy('r', board, maxplies=2)
    blackplayer = ai.Strategy('b', board, maxplies=2)
    player_strategies = {'r': redplayer, 'b': blackplayer}
    strategies = {'r': "AI", 'b': "Human"}
    players = ['r', 'b']
    current_player = players[1]
    movenum, lastcap, pawn_move, count = 1, 0, 0, 0
    # makeHumanMove()
    checkTerminal()

    move = player_strategies.get(current_player).play(
        board)  # get action from current player strategy
    piece = board.get(move[1][0][0], move[1][0][1])

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

    board = board.move(move[1])
    movenum += 1
    sys.stdout.write(action_str)


def gameover(movetimes, winner, time_min):
    """Check if the game is over"""
    if winner is not None:
        return
    else:
        # draw
        return
    return


if __name__ == "__main__":
    # Game(init=boardlibrary.boards["multihop"])
    # Game(init=boardlibrary.boards["StrategyTest1"])
    # Game(init=boardlibrary.boards["EndGame1"], firstmove = 1)
    getAIMove()
