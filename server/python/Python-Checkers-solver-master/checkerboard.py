#! /usr/bin/python3
'''
Created on Feb 21, 2015
Modified Feb 26, 2018 - Expanded comments  

@author: mroch
'''

from __future__ import print_function
from board import Board
from copy import copy, deepcopy
import operator


class CheckerBoard(Board):
    '''
    CheckerBoard - Class for representing a checkerboard
    and making legal moves.

    All references to players in that are accessible externally to this
    class should use the pawn names. 

    Note that this implementation is designed for readability, not
    efficiency.  There are many changes that could be made to
    improve the speed of this class. As an example, the board could
    be represented as a single list of 32 positions.  

    You should not be making changes to the design for this
    assignment, but if you want to have fun later, redesigning
    it for efficiency could be fun and improve the number of plys
    that can be efficiently searched.

    Board notation:
    Board is arranged as with black pieces on top, red pieces on bottom
    Positions are denoted (row, column).
    Examples form the initial board setup before play begins
        left-most red pawn in the row closest to the red player:  (7,0)
        right-most black pawn farthest from the red player:  (0,7)
    Note that playable columns alternate.  In row 0, they are 1, 3, 5, 7
    and in row 1 they are 0, 2, 4, 6 making a modulo 2 counting scheme
    useful for determining which columns are valid.

    Initial board:
       0  1  2  3  4  5  6  7 
    0  .  b  .  b  .  b  .  b 
    1  b  .  b  .  b  .  b  . 
    2  .  b  .  b  .  b  .  b 
    3  .  .  .  .  .  .  .  . 
    4  .  .  .  .  .  .  .  . 
    5  r  .  r  .  r  .  r  . 
    6  .  r  .  r  .  r  .  r 
    7  r  .  r  .  r  .  r  .      
    '''

    # class variables and methods  -------------------------------------------

    # Lists for pawn, king, and player checks
    pawns = ['r', 'b']      # red and black pawns
    kings = ['R', 'B']      # red and black kings
    players = [['r', 'R'], ['b', 'B']]  # pieces for each player

    # Possible moves that will need to be validated for any position
    # pawns[0] red player moves towards top of board (row 0)
    # pawns[1] black player moves towards bottom of board (row N)
    pawnmoves = {pawns[0]: [(-1, -1), (-1, 1)],
                 pawns[1]: [(1, -1), (1, 1)]}
    # kings can move forwards and backwards
    kingmoves = [(-1, 1), (1, 1), (-1, -1), (1, -1)]

    step = 2  # Number of steps between valid columns

    # Number of moves for smallest tour
    # Tours end in the place they started and can only be done
    # by kings
    shortest_tour = 4

    # class methods - useful for evaluation methods
    @classmethod
    def piece_types(cls, player):
        """piece_types - Return pawn and king values for specified player
        e.g. piece_types('r') returns ['r', 'R']
        """

        try:
            index = cls.pawns.index(player)
        except ValueError:
            raise ValueError("No such player")

        return cls.players[index]

    @classmethod
    def other_player(cls, player):
        "other_player(player) - Return other player pawn based on a pawn"
        try:
            index = cls.pawns.index(player)
        except ValueError:
            raise ValueError("No such player")

        return cls.pawns[(index + 1) % 2]

    @classmethod
    def ispawn(cls, piece):
        "True if piece is a pawn"
        return piece in cls.pawns

    @classmethod
    def isking(cls, piece):
        "True if piece is a king"
        return piece in cls.kings

    @classmethod
    def isplayer(cls, player, piece):
        """isplayer - Does a piece belong to a player.
        Given a player name (value of cls.pawns r/b unless changed)
        and a piece from a board, does this piece belong to the 
        specified player?
        Example:  isplayer('r', 'R') returns True
                  isplayer('r', None) returns False
                  isplayer('r', 'b') returns False
        """
        try:
            index = cls.pawns.index(player)
        except ValueError:
            raise ValueError("No such player")

        return piece in cls.players[index]

    @classmethod
    def playeridx(cls, player):
        "playeridx(player) - Give idx of player based on pawn name"

        try:
            pidx = cls.pawns.index(player)
        except ValueError:
            raise ValueError("Unknown player")
        return pidx

    @classmethod
    def identifypiece(cls, piece):
        """identifytpiece(piece)
        Returns a tuple indicating (playeridx, kingpred)
        Used to find the player index of a piece and whether the piece
        is a king (True) or pawn (False)
        e.g. identifypiece('b') returns (1,False)
        """
        try:
            # Check if it is a pawn and note index
            idx = cls.pawns.index(piece)
            kingP = False  # king predicate - not a king
        except ValueError:
            # Similar for king
            try:
                idx = cls.kings.index(piece)
                kingP = True
            except ValueError:
                raise ValueError("Unknown piece type")

        return (idx, kingP)

    # instance methods -------------------------------------------------

    def __init__(self):
        "CheckerBoard - Create a new checkerboard"

        # Create the board
        self.edgesize = 8  # Number of squares per edge
        # Checkers only move on the dark squares, so game space
        # is only half as many states.  Note the number of valid
        # locations per row.
        self.locations_per_row = int(self.edgesize / self.step)

        super(CheckerBoard, self).__init__(self.edgesize, self.edgesize,
                                           displaycol=3)
        # for each row, indicate whether the squares that pieces move
        # in are offset by 0 or 1.
        # This lets us know that in some rows columns are 0, 2, 4, ...
        # and in others they are (0, 2, 4, ...)+1 = (1, 3, 5, 7, ...
        # We store a 0 or 1 offset value for each row.
        self.coloffset = [(r + 1) % self.step for r in range(self.edgesize)]

        rowpieces = 3  # Initial rows of checkers for each side

        # rows in which the players are kinged
        self.kingrows = [0, self.edgesize - 1]

        # Valid spaces are offset in each row.  At top left of board
        # row 0, col 0, the column offset is 0 before we reach the first
        # valid location.
        # In the next row, we need to move one to the right, e.g. [1,1]
        # before we reach a valid checker position.  Row three is back
        # to an offset of 0:  [2, 0]
        # Establish a set of offsets that indicate whether column 0 or 1
        # is the first valid position

        self.pawnsN = [0, 0]  # Number remaining pawns, indexed by player
        self.kingsN = [0, 0]  # Number remaining kings
        for row in range(self.rows):
            # Place pawns in this row?
            if row < rowpieces or row >= self.rows - rowpieces:
                if row < rowpieces:
                    playeridx = 1
                else:
                    playeridx = 0
                for col in range(self.locations_per_row):
                    self.place(row, col * self.step + self.coloffset[row],
                               self.pawns[playeridx])
                    self.pawnsN[playeridx] += 1
            # Place spaces in illegal positions to make board more readable
            for col in range(self.locations_per_row):
                self.board[row][col * self.step +
                                (self.coloffset[row]+1) % 2] = ' '

        self.movecount = 0
        # Counters for draw detection

        # Note that World Checker/Draughts Federation (WCDF) rules indicate that
        # reaching the same configuration board configuration 3 times in a row
        # is also a draw, but this is not implemented.

        # Used for detecting draws which are defined as N moves without
        # advancing a pawn AND no captures
        self.drawthreshN = 40
        self.lastcapture = 0  # move # of last capture
        self.lastpawnadvance = 0  # move number of last pawn advance

    def disttoking(self, player, row):
        "disttoking - how many rows from king position for player given row"

        # find row offset of any legal move for a pawn,
        # that is, which way does the pawn move?
        direction = self.pawnmoves[player][0][0]
        if direction < 0:
            distance = row  # red
        else:
            distance = self.rows - 1 - row  # black
        return distance

    def get_pawnsN(self):
        "get_pawnsN - Return counts of pawns"
        return self.pawnsN

    def get_kingsN(self):
        "get_kingsN - Return counts of kings"
        return self.kingsN

    def isempty(self, row, col):
        "isempty - Is the specified space empty?"
        return self.board[row][col] == None

    def clearboard(self):
        """clearboard - remove all pieces
        Useful for building specific board configurations
        WARNING:  Piece counts will be incorrect after calling
        this.  Call update_counts() to correct after placing new pieces
        """

        # Iterate over every piece and remove it
        for (r, c, piece) in self:
            self.place(r, c, None)

    def update_counts(self):
        """update_counts - When mucking around with the board, the counts
        of pawns and kings may be corrupted.  This method updates them.  Valid
        moves will not cause any problems, this is mainly for testing. 
        """
        self.pawnsN = [0, 0]
        self.kingsN = [0, 0]

        # Iterate through pieces
        for (_r, _c, piece) in self:
            # Find player index and piece type
            (playerId, kingP) = self.identifypiece(piece)
            # update appropriate player piece count
            if kingP:
                self.kingsN[playerId] += 1
            else:
                self.pawnsN[playerId] += 1

    def place(self, row, col, piece):
        "place(row, col, piece) - put a piece on the board"

        # Overrides parent as some spaces are illegal
        if col < 0 or col > self.cols or row < 0 or row > self.rows:
            raise ValueError('Bad row or column')
        if (col + self.coloffset[row]) % self.step == 1:
            if self.coloffset[row]:
                raise ValueError("Column must be odd for row %d" % (row))
            else:
                raise ValueError("Column must be even for row %d" % (row))
        self.board[row][col] = piece

    def is_terminal(self):
        """is_terminal - check if game over
        Returns tuple (terminal, winner)
        terminal - True implies game over
        winner - only applicable if terminal is true
            indicates winner by player color or None for draw
        """

        # Add the pawns and kings together
        piececounts = list(map(operator.add, self.pawnsN, self.kingsN))
        if not piececounts[0]:
            winner = self.pawns[1]
            terminal = True
        elif not piececounts[1]:
            winner = self.pawns[0]
            terminal = True
        else:
            winner = None
            # Check for draws
            terminal = \
                self.movecount - self.lastpawnadvance >= self.drawthreshN or \
                self.movecount - self.lastcapture >= self.drawthreshN

        return (terminal, winner)

    def get_actions(self, player):
        """"Return actions for specified player, CheckerBoard.pawns[i]
        Valid actions are lists of the following form:

        [move1, move2, move3, ..., moveN] where each move consists of 
        a list of two or more tuples

        The first tuple represents the original position (row, col) of 
        the piece, e.g. (5,4)

        A second tuple is either a simple move represented as (row, col) or
        a capture which is a 3-tuple with the third element being a 
        tuple indicating the captured piece.

        Examples:
        possible opening move by player at bottom of board
           0  1  2  3  4  5  6  7                     0  1  2  3  4  5  6  7
        0  .  b  .  b  .  b  .  b                  0  .  b  .  b  .  b  .  b
        1  b  .  b  .  b  .  b  .                  1  b  .  b  .  b  .  b  .
        2  .  b  .  b  .  b  .  b                  2  .  b  .  b  .  b  .  b
        3  .  .  .  .  .  .  .  .   action         3  .  .  .  .  .  .  .  .
        4  .  .  .  .  .  .  .  .   [(5,4),(4,3)]  4  .  .  .  r  .  .  .  .
        5  r  .  r  .  r  .  r  .   results in     5  r  .  r  .  .  .  r  .
        6  .  r  .  r  .  r  .  r                  6  .  r  .  r  .  r  .  r
        7  r  .  r  .  r  .  r  .                  7  r  .  r  .  r  .  r  .

        captures are mandatory.  If any captures exist, normally valid
        non-capture move actions will not be returned. 

        given the following board position, red player captures are as
        follows:  
           0  1  2  3  4  5  6  7
        0  .  b  .  b  .  b  .  b
        1  b  .  b  .  b  .  b  .
        2  .  b  .  .  .  .  .  b
        3  .  .  .  .  .  .  b  .
        4  .  .  .  b  .  .  . <r>   red player candidate moves are shown
        5  r  . <r> . <r> .  .  .    with <> to make it easier to see
        6  .  r  .  r  .  r  .  r
        7  r  .  r  .  r  .  r  .
        [[(4, 7), (2, 5, (3, 6))], 
         [(5, 2), (3, 4, (4, 3))], 
         [(5, 4), (3, 2, (4, 3))]]

        Example of multiple jump moves by red player.  As per World Checkers 
        Draughts Federation Rules, once started a multiple jump move must 
        be made to completion.
           0  1  2  3  4  5  6  7
        0  .  b  .  b  .  b  .  b
        1  b  .  r  .  b  .  .  .
        2  .  r  .  .  .  b  .  b
        3  .  .  .  .  .  .  .  .verb
        4  .  .  .  r  .  b  .  .
        5  .  .  .  .  .  . <r> .
        6  .  r  .  r  .  r  .  r
        7  r  .  .  .  r  .  .  .
        [[(5, 6), (3, 4, (4, 5)), (1, 6, (2, 5))]]
        Note that had multiple capture moves been possible, it is not mandatory
        to take the one with the most jumps
        """

        try:
            pidx = self.pawns.index(player)
        except ValueError:
            raise ValueError("Unknown player")

        # If we see any captures along the way, we will stop looking
        # for moves that do not capture as they will be filtered out
        # at the end.
        moves = []

        # Scan each square
        for r in range(self.rows):
            for c in range(self.coloffset[r], self.cols, self.step):
                piece = self.board[r][c]
                # If square contains pawn/king of player who will be moving
                if piece in self.players[pidx]:
                    # Determine types of moves that can be made
                    if piece == self.pawns[pidx]:
                        movepaths = self.pawnmoves[player]
                    else:
                        movepaths = self.kingmoves
                    # Generate moves based on possible directions
                    newmoves = self.genmoves(r, c, movepaths, pidx)
                    moves.extend(newmoves)

        # Check if any captures are possible
        # If so, remove all non-capture moves as player must make
        # a capture move if one is available.
        captureP = False  # capture predicate
        for a in moves:
            # each action is
            #    [(rsrc, csrc), (rdst, cdst)]  (non-capture case)
            # or [(rsrc, csrc), (rdst, cdst, (rcapture, ccapture), ...]
            captureP = len(a[1]) > 2
            if captureP:
                break
        if captureP:
            # Remove non capture moves as player must capture if possible
            # We only need to check the first destination to see if it
            # has a capture tuple after the destination row and column
            moves = [m for m in moves if len(m[1]) > 2]

        return moves

    @classmethod
    def get_action_str(cls, action):
        """get_action_str(action)
        Given an action tuple, format it as a human readable string
        """

        strings = []  # List of all position in one or more hops
        # Starting position, note that , is required after tuple for old
        # style formatter to not interpret tuple as multiple arguments
        strings.append("from %s" % (action[0],))
        # format moves
        for posn in action[1:]:
            if len(posn) == 2:
                # no capture (final move)
                strings.append("to %s" % (posn,))
            else:
                # capture, note position of captured piece
                strings.append("to %s capturing %sa" % (posn[0:2], posn[2]))
        return " ".join(strings)

    def __iter__(self):
        """iter - Board iterator
        Returns (r, c, piece) for non empty spaces.
        Might be helpful for board evaluation
        """
        for r in range(self.rows):
            for c in range(self.coloffset[r], self.cols, self.step):
                if self.board[r][c]:
                    yield (r, c, self.board[r][c])

    def move(self, move, validate=[], verbose=False):
        """move - Apply a move and return a new board
        move should be a list of the format described in get_actions
        It is assumed that the move is valid unless validate is set to a 
        list of moves (presumably produced by get_actions(), get_actions is
        not called as this has probably already been computed.
        """

        if validate:
            if move not in validate:
                raise ValueError("Invalid move")

        # Only need to copy the board and counter arrays
        # Everything else is static and can be a shallow copy
        newboard = copy(self)
        newboard.pawnsN = copy(self.pawnsN)
        newboard.kingsN = copy(self.kingsN)
        newboard.board = deepcopy(self.board)
        newboard.movecount += 1  # Record new move

        (firstr, firstc) = (lastr, lastc) = move[0]
        piece = self.get(lastr, lastc)
        oldpiece = piece  # Just in case we change and want to print
        newboard.place(lastr, lastc, None)  # Remove from current position

        captures = 0  # number of captures for verbose output and draw detection
        # Loop through move sequence, removing any
        # captured pieces as we go along
        for item in move[1:]:
            if len(item) > 2:
                # Capture, remove captured piece
                captures = captures + 1
                posn = item[2]  # captured position
                capturedpiece = newboard.get(posn[0], posn[1])

                # Remove the piece
                newboard.place(posn[0], posn[1], None)

                # Decrement count for captured piece
                (pieceidx, kingP) = newboard.identifypiece(capturedpiece)
                if kingP:
                    newboard.kingsN[pieceidx] -= 1
                else:
                    newboard.pawnsN[pieceidx] -= 1

            # update last known location of moving piece, might happen
            # more than once in a multiple jump move
            # In any case, last row and column will represent the final
            # position of the piece when we finish the loop
            (lastr, lastc) = item[0:2]

        if lastr == 0 or lastr + 1 == self.rows:
            # At end, do we need to crown a pawn?
            try:
                # find the appropriate pawn type and crown it
                playeridx = self.pawns.index(piece)
                piece = self.players[playeridx][1]  # king
            except ValueError:
                pass  # not a pawn

        # Put the piece as the last location of the move sequence
        newboard.place(lastr, lastc, piece)

        if captures:
            # Captured something, note the move for draw detection
            newboard.lastcapture = newboard.movecount

        if self.ispawn(oldpiece):
            # Advanced a pawn, note move number for draw detection
            newboard.lastpawnadvance = newboard.movecount
            if oldpiece != piece:
                # Kinged, update counts
                (pieceidx, kingP) = newboard.identifypiece(oldpiece)
                newboard.pawnsN[pieceidx] -= 1
                newboard.kingsN[pieceidx] += 1

        if verbose:
            # Show the move if folks are interested...
            print()
            print("Move %s from " % (oldpiece), (firstr, firstc))
            print(self)
            #print("move: ", end=' ')
            if captures > 0:
                print("")
                #print("captures %d, " % (captures), end=' ')
            if oldpiece != piece:
                print("kinged, ")
            print()
            print(newboard)

        return newboard

    def onboard(self, r, c):
        "onboard - Specified row and column on the board?"
        return r >= 0 and r < self.rows and c >= 0 and c < self.cols

    def genmoves(self, r, c, movepaths, playeridx):
        """genmoves - Generate moves from a specific position
        r,c - position
        movepaths - list of possible offsets (move directions) for piece
            e.g. for kings:  [ (-1, 1), (1, 1), (-1, -1), (1, -1) ] 
            pawns will have a subset of this moving forward or backward
        player - current player 0|1

        Returns list of possible moves (see get_actions) and captures
        """

        actions = self.__movehelper(r, c, movepaths, playeridx, [])
        return actions

    def __movehelper(self, r, c, movepaths, playeridx, history):
        """__movehelper - Helper finds possible moves from a given position.
        Helper function for genmoves
        r,c - position
        movepaths - list of possible offsets for piece
        playeridx - current playeridx 0|1
        history - list of moves made along a path - [] on first call
        Returns list of possible moves (see get_actions) and captures
        which indicates if a capture has been produced by the moves
        generated here or was already true.

        This function is called recursively to track move paths
        """

        otherplayer = (playeridx + 1) % 2
        actions = []
        for m in movepaths:
            rmove = r + m[0]
            cmove = c + m[1]
            # move only valid if it will be on the board
            if self.onboard(rmove, cmove):

                # check if blocked by opposing player, might be able to jump
                if self.board[rmove][cmove] in self.players[otherplayer]:
                    # Blocked See if capture possible by moving one more time
                    rjump = rmove + m[0]
                    cjump = cmove + m[1]
                    if self.onboard(rjump, cjump) and \
                        self.__valid_capture((rmove, cmove), (rjump, cjump),
                                             history):
                        # Note jump
                        if history:
                            # append to a copy of previous jumps so far
                            # We need to copy history as move sequences
                            # can branch, resulting in different moves
                            # with a common past.
                            capture = copy(history)
                            capture.append((rjump, cjump, (rmove, cmove)))
                        else:
                            # first jump
                            capture = [(r, c), (rjump, cjump, (rmove, cmove))]

                        # Crown a king?
                        # As pawns can only move forward, just look if we have
                        # moved to the first or last row.
                        if rjump == 0 or rjump == self.rows:
                            # Piece has moved onto a first or last row
                            # If this is a pawn, we stop even if there
                            # is another capture available

                            # Was this a pawn?
                            (rstart, cstart) = (capture[0][0], capture[0][1])
                            if self.get(rstart, cstart) == self.pawns[playeridx]:
                                # Can't move any more
                                return [capture]

                        # We can make this move, but if we can continue
                        # to capture, we are obligated to do so.
                        # See if we can continue.
                        # If no more moves are possible, will simply
                        # return the current move as one possible action
                        #
                        # Note:  If we wanted to not force subsequent
                        # available jumps after the first one, we could
                        # append the current capture move, and remove the
                        # code that returns [history] when there are no
                        # available actions.
                        more = self.__movehelper(rjump, cjump, movepaths,
                                                 playeridx, capture)
                        for m in more:
                            actions.append(m)

                # Regular move possible if not blocked and no history
                # of captures
                elif not self.board[rmove][cmove] and not history:
                    actions.append([(r, c), (rmove, cmove)])

        if history and not actions:
            # One or more captures have been made, but when we called
            # __movehelper to see if there were any more, there were
            # no valid actions.  We set actions to be a list containing
            # the history that was required to arrive here.
            actions = [history]

        return actions

    def __valid_capture(self, capturedpiece, moveto, history):
        """__valid_capture
            capturedpiece - (r,c) tuple to be captured
            moveto - position to which we will jump
            history - previous jumps

        already_captured - Prevent taking a piece more than once
        helper function for __movehelper
        """

        valid = True  # Until we learn otherwise

        # Verify that there's no piece at the destination.
        # If there is a piece, check to see if it was the starting
        # position as it is possible to do a jump tour
        if self.board[moveto[0]][moveto[1]]:
            # Something's there.  If it's the starting piece, that's okay,
            # otherwise not good.  Don't bother checking if there are
            # not enough moves.
            if len(history) >= self.shortest_tour:
                valid = history[0] == moveto
            else:
                valid = False

        if valid and len(history) > 1:
            for move in history[1:]:
                # Anything in the history is a capture as __movehelper
                # recursively builds the history on multi-jump moves.
                # All capture nodes consist of a 3-tuple:
                #  (newrow, newcol, (capturedrow, capturedcol))
                # First position in history is the starting one, anything
                # afterwards is a capture move.

                # If we already captured this piece, we cannot capture
                # it again.
                if move[2] == capturedpiece:
                    valid = False

        return valid

    def recount_pieces(self):
        """recount_pieces() - Recount pawns and kings
        This utility function is not normally needed.  However, when
        configuration custom boards where pieces are manually placed
        (e.g. in boardlibary), the board counts will not longer be accurate.
        This resets the counters based on the current configuration.
        """
        self.pawnsN = [0, 0]
        self.kingsN = [0, 0]
        for (r, c, piece) in self:
            (playeridx, kingP) = self.identifypiece(piece)
            if kingP:
                self.kingsN[playeridx] += 1
            else:
                self.pawnsN[playeridx] += 1
