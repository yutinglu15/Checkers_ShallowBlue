from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
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
        move = self.minimax_move(moves)
        self.board.make_move(move,self.color)
        return move

    def minimax_move(self, moves: [list]) :
        print(self.color)
        best = []
        max_value = - math.inf
        depth = 4
        for chess in moves:
            for move in chess:
                val = self.max_value(move, depth, -math.inf, math.inf)
                if val > max_value:
                    best = [move]
                    max_value = val
                elif val == max_value:
                    best.append(move)
        print(max_value)
        return best[randint(0,len(best)-1)]


    def min_value(self, move, depth, alpha, beta):
        self.board.make_move(move, self.opponent[self.color])
        if depth == 0:
            u = self.utility(self.board)
            self.board.undo()
            return u
        min_val = math.inf
        for chess in self.board.get_all_possible_moves(self.color):
            for move in chess:
                min_val = min(self.max_value(move, depth - 1, alpha, beta), min_val)
                beta = min(beta, min_val)
                if alpha >= beta:
                    self.board.undo()
                    return min_val
        self.board.undo()
        return min_val

    def max_value(self, move, depth, alpha, beta):
        self.board.make_move(move, self.color)
        if depth == 0:
            u = self.utility(self.board)
            self.board.undo()
            return u
        max_val = - math.inf
        for chess in self.board.get_all_possible_moves(self.opponent[self.color]):
            for move in chess:
                max_val = max(self.min_value(move, depth - 1, alpha, beta), max_val)
                alpha = max(alpha, max_val)
                if alpha >= beta:
                    self.board.undo()
                    return max_val
        self.board.undo()
        return max_val

    def utility(self, board):
        b = self.board.black_count
        w = self.board.white_count
        #print("black:",b," white:",w)
        return b-w if self.color == 1 else w-b
