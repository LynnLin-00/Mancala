# File: llg8421.py
# Ling Lin: llg8421
# Yue Shao: ysk9916
# Date: Oct 13, 2017
# Group work statement: All group members were present and contributing during all work
# on this project.
# Defines a simple artificially intelligent player agent



from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            print m
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            #print "s in maxValue is: " + str(s)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                #print "turn.score(board) in min Value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            #print "s in minValue is: " + str(s)
            if s < score:
                score = s
        return score


    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
            return 100.0
        elif board.hasWon(self.opp):
            return 0.0
        else:
            return 50.0


    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """

        move = -1
        turn = self

        # a represents alpha, b represents beta
        a = -1
        b = 50


        for m in board.legalMoves(self):
            print m
            # for each legal move
            if ply == 0:
                # if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            # make a new board
            nb.makeMove(self, m)
            # try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply - 1, turn)
            b = s
            # and see what the opponent would do next

            # if beta is less than alpha, prune the node
            if b <= a:
                break

            # if the result is better than our best score so far, save that move,score
            move = m
            a = s
        # return the best score and move so far
        return a, move

    # here is an improved alphaBetaMove used by our custom player
    def alphaBetaMoveCustom(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """

        move = -1
        turn = self
        a = -1
        b = 50

        # find self cup
        if self.num == 1:
            selfcups = board.P1Cups
        else:
            selfcups = board.P2Cups

        # if there is a way to put the last ball into the score cup
        # and thus get a free turn, just go with that move
        for i in range(board.NCUPS):
            if i + selfcups[i] == board.NCUPS:
                return a, i + 1

        # same thing from here as alphaBetaMove
        for m in board.legalMoves(self):
            # for each legal move
            if ply == 0:
                # if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            # make a new board
            nb.makeMove(self, m)
            # try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply - 1, turn)
            b = s
            # and see what the opponent would do next
            if b <= a:
                break
            # if the result is better than our best score so far, save that move,score
            move = m
            a = s
        # return the best score and move so far
        return a, move

    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "random chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            # use alphaBetaMoveCustom and ply equals 7,
            # choose a customized move which is an improved alphaBetaMove defined above
            val, move = self.alphaBetaMoveCustom(board, 7)
            print "llg8421 chose move", move, " with value", val
            return move

        else:
            print "Unknown player type"
            return -1


class MancalaPlayer(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """

    def score(self, board):



        """ Evaluate the Mancala board for this player """
        # Currently this function just calls Player's score
        # function.  You should replace the line below with your own code
        # for evaluating the board
        # print "Calling score in MancalaPlayer"



        # number of zeros in the cups
        nzero = 0
        # if there is zero in our cup, add one point, else if there is zero in our opponent's cup, reduce one.
        for i in board.getPlayersCups(self.opp - 1):
            if i == 0:
                nzero -= 1
        for i in board.getPlayersCups(self.num - 1):
            if i == 0:
                nzero += 1
        # one ball in our score cup earns one point and plus the score of zeros equals the final score
        return board.scoreCups[self.num - 1] + nzero




