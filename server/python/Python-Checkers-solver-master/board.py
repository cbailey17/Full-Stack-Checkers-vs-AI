#! /usr/bin/python3
"""
@author: Cameron Bailey
"""
import math


class Board:
    """Grid board class
    Represent a two dimensional grid of items
    """

    def __init__(self, rows, cols, displaycol=9, empty_symbol='.'):
        """construct a board with specified rows and cols
        displaytab can be set to display the board with a specified
        number of columns so that items line up.
        empty_symbol is the string that is displayed when a board
        space is empty."""
        self.rows = rows
        self.cols = cols
        self.displaycol = displaycol
        self.empty_symbol = empty_symbol
        # Generated 2D list representing an empty board
        # in row-major order (rows indexed first)
        self.board = \
            [[None for c in range(cols)] for r in range(rows)]

    def place(self, row, col, item):
        "place an item"
        self.board[row][col] = item

    def get(self, row, col):
        "get an item"
        return self.board[row][col]

    def get_rows(self):
        "get_rows - return number of rows"
        return self.rows

    def get_cols(self):
        "get_cols - return number of columns"
        return self.cols

    def __repr__(self):
        "return a representation of the board"

        lines = []
        # NOTE:  This section uses Python's format strings (see string
        # operations in the standard library).  Most times these are overkill
        # and Python's string substitution can be used (e.g. "x=%d"%(result))
        # but for centering the formatter is a bit easier.
        # Basic format syntax
        #    { } specifies something to be replaced
        #

        # Generate format strings such that:
        # columns:
        #  digits will be converted to string (!s)
        #  column numbers will be centered (^)
        colheader = "{!s:^%d}" % (self.displaycol)
        # number of digits needed for rows
        rowheadersz = int(math.ceil(self.rows / 10.0))
        # rows labels are right justified (>) with a trailing space
        rowheader = "{:>%dd} " % (rowheadersz)  # right justified digit

        # force conversion to string !s and center in a field of
        # displaycol spaces.
        colentry = "{!s:^%d}" % (self.displaycol)
        # Generate column labels
        lines.append(
            # leave space for row labels in subsequent rows
            # one space for each digit + space before row content
            "".join([" " for _ in range(rowheadersz+1)]) +
            # column labels
            "".join([colheader.format(idx) for idx in range(self.cols)]))
        # Generate board string
        r = 0
        for row in self.board:
            lines.append(
                # row label
                rowheader.format(r) +
                # row content
                "".join([colentry.format(entry if entry else self.empty_symbol)
                         for entry in row]))
            r = r + 1
        # concatenate list into a string
        return "\n".join(lines)
