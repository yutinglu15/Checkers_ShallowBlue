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
        best = []
        max_value = - math.inf
        depth = 3
        for chess in moves:
            for move in chess:
                # val = self.greedy(copy.deepcopy(self.board), move, depth, self.color)
                val = self.maxValue(copy.deepcopy(self.board), move, depth)
                if val > max_value:
                    best = [move]
                    max_value = val
                elif val == max_value:
                    best.append(move)
        print(max_value)
        return best[randint(0,len(best)-1)]

    def greedy(self, tmp_board, move, depth,curr_color):
        tmp_board.make_move(move, curr_color)
        if depth == 0:
            return self.utility(tmp_board)
        val = - math.inf
        moves = tmp_board.get_all_possible_moves(self.opponent[curr_color])
        for chess in moves:
            for move in chess:
                oppo_board = copy.deepcopy(tmp_board)
                val = max(val, self.greedy(oppo_board, move, depth - 1, self.opponent[curr_color]))
        return val


    def minValue(self, tmp_board, move, depth):
        tmp_board.make_move(move, self.opponent[self.color])
        if depth == 0:
            return self.utility(tmp_board)
        min_val = math.inf
        for chess in tmp_board.get_all_possible_moves(self.color):
            for move in chess:
                min_val = min(self.maxValue(copy.deepcopy(tmp_board),move, depth - 1), min_val)
        return min_val

    def maxValue(self, tmp_board, move, depth):
        tmp_board.make_move(move, self.color)
        if depth == 0:
            return self.utility(tmp_board)
        max_val = - math.inf
        for chess in tmp_board.get_all_possible_moves(self.opponent[self.color]):
            for move in chess:
                max_val = max(self.minValue(copy.deepcopy(tmp_board),move, depth - 1), max_val)
        return max_val

    def utility(self, board):
        b = self.count_color(board.board, 'B')
        w = self.count_color(board.board, 'W')
        #print("black:",b," white:",w)
        return b-w if self.color == 1 else w-b

    def count_color(self, board, color):
        count = 0
        for row in board:
            for chess in row:
                count += 1 if chess.get_color() == color else 0
        return count