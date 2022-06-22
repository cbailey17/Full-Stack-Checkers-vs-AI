#! /usr/bin/python3
"""
@author: Cameron Bailey
"""

# Game representation and mechanics
from __future__ import print_function
from statistics import mean
from timer import Timer
import checkerboard

import importlib  # import imp
import ai
import human
import sys
import redis
import pickle
import logging

redis_client = redis.Redis(host='localhost',
                           port=6379,
                           db=0)

def checkTerminal(board):
    terminal, winner = board.is_terminal()
    if terminal:
        gameover(winner)
        return

def findCapturedPiece(action):
    piece_row = int(action[6])-1
    if int(action[19]) > int(action[9]):
        piece_col = int(action[19])-1
    else:
        piece_col = int(action[19])+1
    return (piece_row, piece_col)

def buildCaptureAction(action, board):
    """  A second tuple is either a simple move represented as (row, col) or
        a capture which is a 3-tuple with the third element being a
        tuple indicating the captured piece.
        [[(4, 7), (2, 5, (3, 6))],
    """
    captured_piece = findCapturedPiece(action)
    capture = [(int(action[6]), int(action[9])), (int(action[16]), int(action[19]), captured_piece)]
    return capture


def buildHumanAction(action, board):
    """build list of tuples"""
    actionArray = [action[6], action[9], action[16], action[19]]
    if (board.isHumanCapture(actionArray)):
        action = buildCaptureAction(action, board)
    else:
        action = [(int(action[6]), int(action[9])), (int(action[16]), int(action[19]))]
    return action


def makeHumanMove(humanAction, board, lastcap, movenum, pawn_move):
    piece = board.get(int(humanAction[6]), int(humanAction[9]))

    if board.ispawn(piece):
        pawn_move = 0
    else:
        pawn_move += 1

    human_action = buildHumanAction(humanAction, board)

    if len(human_action[1]) > 2:  # Check if there is a capture
        lastcap = 0
    else:
        lastcap += 1
    board = board.move(human_action)
    movenum += 1

    return board, movenum, lastcap, pawn_move, piece


def getAIMove():
    """ Function made for a UI to play human vs AI"""
    boardState = pickle.loads(redis_client.get('BoardState'))
    board = boardState['board']
    redplayer = boardState['redplayer']
    blackplayer = boardState['blackplayer']
    player_strategies = boardState['player_strategies']
    strategies = boardState['strategies']
    players = boardState['players']
    current_player = boardState['current_player']
    movenum = boardState['movenum']
    lastcap = boardState['lastcap']
    pawn_move = boardState['pawn_move']
    count = boardState['count']


    logging.warning("Current board in getAIMove() before humans move: ", board)
    # logging.warning("board state object: ", boardState)
    # logging.warning("Humans move sent to server: ", sys.argv[1])
    logging.warning("last capture: ", lastcap)
    logging.warning("move number: ", movenum)
    logging.warning("Current player: ", current_player)
    # logging.warning("board string", board.findListPositions())
    logging.warning("-------------------------------------------")

    board, movenum, lastcap, pawn_move, piece = makeHumanMove(
        sys.argv[1], board, lastcap, movenum, pawn_move)
    checkTerminal(board)

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

    newBoardState = {
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
    logging.warning("Current board in getAIMove() after humans and AI move: ", board)
    # logging.warning("board state object: ", boardState)
    # logging.warning("Humans move sent to server: ", sys.argv[1])
    # logging.warning("last capture: ", lastcap)
    # logging.warning("move number: ", movenum)
    # logging.warning("Current player: ", current_player)
    # logging.warning("newBoardState", newBoardState)
    logging.warning("move", move)
    # logging.warning("board string", board.findListPositions())
    logging.warning("-------------------------------------------")

    redis_client.set('BoardState', pickle.dumps(newBoardState))
    sys.stdout.write(action_str)



def gameover(winner):
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
