# -*- coding: utf-8 -*-
"""
Created on Wed Mar  4 13:42:32 2020

@author: Alex Cameron Bailey
"""
import abstractstrategy


class Strategy(abstractstrategy.Strategy):
    """Strategy class for implementing search with alpha-beta pruning"""
    values = {}
    nboard = {}

    def play(self, board):
        """play function from abstract strategies. This function is used in checkers.py in order to generate the move
        with the optimal utility
        """
        move = self.alpha_beta(board, self.maxplies)
        return move

    def utility(self, board):
        """
        utility function determines utility of a board
        Utility=(numAI checkers – number of human checkers)*500
        """
        reds = []
        blacks = []
        pawns = board.get_pawnsN()
        kings = board.get_kingsN()
        # Determine how many players are close to being kings
        if self.maxplayer == 'r':
            for i in range(2):
                for j in range(8):
                    reds.append(board.get(i, j))
            close_to_king = reds.count('r')
            u = (kings[0] + kings[0]) - (pawns[1] + kings[1])*500 + close_to_king*500
        else:
            if self.maxplayer == 'b':
                for i in range(5, 7):
                    for j in range(8):
                        blacks.append(board.get(i, j))
            close_to_king2 = blacks.count('b')
            u = (pawns[1] + kings[1]) - (pawns[0] + kings[0])*500 + close_to_king2*500
        return u

    def alpha_beta(self, board, plies):
        """implement alpha-beat pruning"""
        result = self._maxvalue(board, float('-inf'), float('inf'), plies)
        return self.nboard.get(result), self.values.get(result)

    def _maxvalue(self, board, alpha, beta, plies):
        """Alpha-beta max value function"""
        # Check if the board has reached an end state of if the search depth is reached
        if board.is_terminal()[0] or plies == 0:
            v = self.utility(board)
        else:
            v = float("-inf")
            actions = board.get_actions(self.maxplayer)
            for a in actions:  # loop through actions to find the move with max utility for maxplayer
                new_board = board.move(a)
                minvalue = self._minvalue(new_board, alpha, beta, plies-1)
                v = max(v, minvalue)
                self.values.update({v: a})  # add utilties to a dictionary to keep track of actions and their utilities
                self.nboard.update({v: new_board})
                if v >= beta:  # Check if utility is greater than beta for pruning
                    break
                else:
                    alpha = max(alpha, v)
        return v

    def _minvalue(self, board, alpha, beta, plies):
        """Alpha-beta min value function"""
        # Check if the board has reached an end state of if the search depth is reached
        if board.is_terminal()[0] or plies == 0:
            v = self.utility(board)
        else:
            v = float("inf")
            actions = board.get_actions(self.minplayer)  # get board actions of min player
            for a in actions:  # loop through the actions and find action with min utility
                new_board = board.move(a)
                maxvalue = self._maxvalue(new_board, alpha, beta, plies-1)
                v = min(v, maxvalue)
                if v <= alpha:  # Check if utility is less that alpha for pruning
                    break
                else:
                    beta = min(beta, v)
        return v
