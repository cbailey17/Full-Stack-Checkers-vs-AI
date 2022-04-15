#! /usr/bin/python3
"""
@author: Cameron Bailey
"""

# Game representation and mechanics
from __future__ import print_function
import checkerboard

import importlib  # import imp
import ai
import human
import sys
import redis
import pickle

redis = redis.Redis(host='localhost',
                    port=6379,
                    db=0)


def init():
    board = checkerboard.CheckerBoard()
    # board = pickle.loads(redis_client.get('BoardState'))
    redplayer = human.Strategy('r', board, maxplies=2)
    blackplayer = ai.Strategy('b', board, maxplies=2)
    player_strategies = {'r': redplayer, 'b': blackplayer}
    strategies = {'r': "Human", 'b': "AI"}
    players = ['r', 'b']
    current_player = players[1]
    movenum, lastcap, pawn_move, count = 1, 0, 0, 0

    boardState = {
        'board': board,
        'redplayer': redplayer,
        'blackplayer': blackplayer,
        'player_strategies': player_strategies,
        'strategies': strategies,
        'players': players,
        'current_player': current_player,
        'movenum': movenum,
        'lastcap': lastcap,
        'pawn_move': pawn_move,
        'count': count
    }

    redis.set('BoardState', pickle.dumps(boardState))
    print("Initialized board state.....")


if __name__ == "__main__":
    init()
