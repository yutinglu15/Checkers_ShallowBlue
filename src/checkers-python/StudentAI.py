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
        print(self.color)
        best = None
        max_value = - math.inf
        depth = 3
        for chess in moves:
            for move in chess:
                val = self.greedy(move, depth)
                if val > max_value:
                    best = move
                    max_value = val
        print(best, max_value)
        return move

    def greedy(self, move, depth):
        tmp_board = copy.copy(self.board)
        if depth == 0:
            return self.utility(tmp_board)
        val = 0
        for chess in tmp_board.get_all_possible_moves(self.color):
            for move in chess:
                val += self.greedy(move, depth - 1)
        return val

    # def minValue(self, move, depth):
    #     tmp_board = copy.copy(self.board)
    #     if depth == 0:
    #         return self.utility(tmp_board)
    #     min_val = math.inf
    #     for chess in tmp_board.get_all_possible_moves(self.opponent[self.color]):
    #         for move in chess:
    #             min_val = min(self.maxValue(move, depth - 1), min_val)
    #     return min_val
    #
    # def maxValue(self, move, depth):
    #     tmp_board = copy.copy(self.board)
    #     if depth == 0:
    #         return self.utility(tmp_board)
    #     max_val = - math.inf
    #     for chess in tmp_board.get_all_possible_moves(self.color):
    #         for move in chess:
    #             max_val = max(self.minValue(move, depth - 1), max_val)
    #     return max_val

    def utility(self, board):
        b = self.count_color(board.board, 'B')
        w = self.count_color(board.board, 'W')
        #print("black:",b," white:",w)
        return b-w if self.color == 1 else w-b

    def count_color(self, board, color):
        count = 0
        for row in board:
            for chess in row:
                count += 1 if chess.color == color else 0
        return count