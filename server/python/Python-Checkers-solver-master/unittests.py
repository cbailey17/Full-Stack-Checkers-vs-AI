'''
Created on Mar 1, 2015

@author: mroch
'''
import unittest

import boardlibrary

# Unit tests for verifying functionality of checkerboard class
# Students do not need this to complete the assignment, but if you
# want to learn about unit testing, this may be helpful although
# you'll need to couple it with a unit test tutorial as this is not
# designed to be a ground-up tutorial.


class testBoard(unittest.TestCase):
    def setUp(self):
        pass
         
    def tupleize_list(self, l):
        # tupleize_list - list
        # Convert list of lists to tuple so that we can
        # use it in set operations (tuples are hashable,
        # lists are not). 
        return tuple([tuple(item) for item in l])

    def test_prisitine(self):
        "Check moves on initial checkerboard"
        
        # Initial board
        b = boardlibrary.boards["Pristine"]

        # Red moves?        
        actions = b.get_actions('r')
        
        if False:
            # Show board moves
            # Not a real unit test
            for a in actions:
                newb = b.move(a)
            
        # Convert to tuple for set operations
        actions = self.tupleize_list(actions)
        redexpected = set(
                (((5, 0), (4, 1)), 
                 ((5, 2), (4, 1)), 
                 ((5, 2), (4, 3)), 
                 ((5, 4), (4, 3)), 
                 ((5, 4), (4, 5)), 
                 ((5, 6), (4, 5)), 
                 ((5, 6), (4, 7))))
        self.assertEqual(set(actions), redexpected, "Bad red move")
        
        # Black moves?
        actions = b.get_actions('b')
        # Convert to tuple for set operations
        actions = self.tupleize_list(actions)
        blackexpected = set(
                (((2, 1), (3, 0)), 
                 ((2, 1), (3, 2)), 
                 ((2, 3), (3, 2)), 
                 ((2, 3), (3, 4)), 
                 ((2, 5), (3, 4)), 
                 ((2, 5), (3, 6)), 
                 ((2, 7), (3, 6))))       
        self.assertEqual(set(actions), blackexpected, "Bad black move")        
        
    def test_simplecapture(self):
        "Single capture - no multiple hops"
        
        # See boardlibrary for details
        b = boardlibrary.boards["SingleHopsRed"]
        actions = b.get_actions('r')
        actions = set(self.tupleize_list(actions))
        redexpected = set(
            self.tupleize_list([
                    [(4, 7), (2, 5, (3, 6))], 
                    [(5, 2), (3, 4, (4, 3))], 
                    [(5, 4), (3, 2, (4, 3))]
                    ]))
        self.assertEqual(actions, redexpected)
        
        # Set up black captures
        # See boardlbirary for details
        b = boardlibrary.boards["SingleHopsBlack"]
        actions = b.get_actions('b')
        actions = set(self.tupleize_list(actions))
        blackexpected = set(self.tupleize_list([
                [(2, 7), (4, 5, (3, 6))], 
                [(4, 3), (6, 1, (5, 2))]
                ]))
        self.assertEqual(actions, blackexpected)
        
    def test_multihopcapture(self):
        "Can we predict multiple hops"
        
        # See boardlibrary for details
        b = boardlibrary.boards['multihop']
        
        actions = b.get_actions('r')
        actions = set(self.tupleize_list(actions))
        redexpected = set(self.tupleize_list([
                    [(5, 6), (3, 4, (4, 5)), (1, 6, (2, 5))]
                    ]))
        self.assertEqual(actions, redexpected)
        
        actions = b.get_actions('b')
        
        if True:
            # Show board moves
            # Not a real unit test
            for a in actions:
                newb = b.move(a, verbose=True)
        
        actions = set(self.tupleize_list(actions))
        blackexpected = set(self.tupleize_list([
                [(0, 1), (2, 3, (1, 2))], 
                [(1, 0), (3, 2, (2, 1)), (5, 4, (4, 3)), (7, 2, (6, 3))], 
                [(1, 0), (3, 2, (2, 1)), (5, 4, (4, 3)), (7, 6, (6, 5))]
                ]))
        self.assertEqual(actions, blackexpected)       

    def test_kingstour(self):
        """"test_kingstour - Verify kings tour
        Verify that we can accurately find a king's tour and that a pawn
        that is kinged cannot continue on to the King's tour
        """
        
        # Black can be crowned after double jump move
        # See boardlibrary for details
        b = boardlibrary.boards['KingBlack']        
        # Need to make sure that we can go backwards after being kinged
        # and that we don't retake any pieces that were already taken
        actions = b.get_actions('b')
        actions = set(self.tupleize_list(actions))
        blackexpected = set(self.tupleize_list([
                [(3, 4), (5, 2, (4, 3)), (7, 4, (6, 3))], 
                [(3, 4), (5, 6, (4, 5)), (7, 4, (6, 5))]
            ]))
        self.assertEqual(actions, blackexpected)
        
        # Black king can tour
        # See boardlibrary for details
        b = boardlibrary.boards['BlackKingTour']
        actions = b.get_actions('b')
        actions = set(self.tupleize_list(actions))
        blackexpected = set(self.tupleize_list([
                [(3, 4), (5, 6, (4, 5)), (7, 4, (6, 5)), 
                 (5, 2, (6, 3)), (3, 4, (4, 3))], 
                [(3, 4), (5, 2, (4, 3)), (7, 4, (6, 3)), 
                 (5, 6, (6, 5)), (3, 4, (4, 5))]
            ]))
        self.assertEqual(actions, blackexpected)

        # Red king can tour
        # See boardlibrary for details
        b = boardlibrary.boards['RedKingTour']
        actions = b.get_actions('r')
        actions = set(self.tupleize_list(actions))
        redexpected = set(self.tupleize_list([
                [(3, 4), (5, 6, (4, 5)), (7, 4, (6, 5)), 
                 (5, 2, (6, 3)), (3, 4, (4, 3))], 
                [(3, 4), (5, 2, (4, 3)), (7, 4, (6, 3)), 
                 (5, 6, (6, 5)), (3, 4, (4, 5))]
            ]))
        self.assertEqual(actions, redexpected)

# Run test cases if invoked as main module
if __name__ == "__main__":
    b = boardlibrary.boards["Pristine"]
    for player in ['r', 'b']:
        for r in range(8):
            print("player %s row %d distance %d\n"%(player, r, b.disttoking(player, r)))

    # Execute the test suite shwoing results for each test
    suite = unittest.TestLoader().loadTestsFromTestCase(testBoard)
    unittest.TextTestRunner(verbosity=2).run(suite)