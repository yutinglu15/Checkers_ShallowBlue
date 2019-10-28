from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
import copy
#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)

        #index = randint(0,len(moves)-1)
        #inner_index =  randint(0,len(moves[index])-1)
        #move = moves[index][inner_index]
        #print(moves)
        move = self.best_move(moves)
        self.board.make_move(move,self.color)
        return move

    def best_move(self, moves: [list]) :
        best = moves[0][0]
        max_value = - math.inf
        depth = 5
        for chess in moves:
            for move in chess:
                val = self.minValue(move, depth)
                if val > max_value:
                    best = move
                    max_value = val
        return move

    def minValue(self, move, depth):
        tmp_board = copy.copy(self.board)
        if depth == 0:
            return self.utility(tmp_board)
        min_val = math.inf
        for chess in tmp_board.get_all_possible_moves(self.opponent[self.color]):
            for move in chess:
                min_val = min(self.maxValue(move, depth - 1), min_val)
        return min_val

    def maxValue(self, move, depth):
        tmp_board = copy.copy(self.board)
        if depth == 0:
            return self.utility(tmp_board)
        max_val = - math.inf
        for chess in tmp_board.get_all_possible_moves(self.color):
            for move in chess:
                max_val = max(self.minValue(move, depth - 1), max_val)
        return max_val

    def utility(self, board):
        b = sum([r.count('b')+r.count('B') for r in board.board])
        w = sum([r.count('w') + r.count('W') for r in board.board])
        return b-w if self.color == 1 else w-b