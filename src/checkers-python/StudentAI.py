from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
import copy
import random

import time
#import numpy as np


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

        self.movecount = 1


    def get_move(self, move):
        #print(self.color)
        self.time = time.time()
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)

        #index = randint(0,len(moves)-1)
        #inner_index =  randint(0,len(moves[index])-1)
        #move = moves[index][inner_index]
        #print(moves)
        move = moves[0][0] if len(moves) == 1 and len(moves[0]) == 1 else self.minimax_move(moves)
        self.board.make_move(move, self.color)
        self.movecount += 1
        return move

    def minimax_move(self, moves: [list]) :
        best = []
        max_value = - math.inf
        depth = 6
        for chess in moves:
            for move in chess:
                val = self.max_value(move, depth, -math.inf, math.inf)
                if val > max_value:
                    best = [move]
                    max_value = val
                elif val == max_value:
                    best.append(move)
        return best[randint(0,len(best)-1)]
        # if len(best) == 1:
        #     return best[0]
        # return self.monte_carlo_tree(best, 10, 100)

    def monte_carlo_tree(self, moves: [], simulate_times: int, s_parent: int):
        best_uct = - math.inf
        best_move = 0
        for move in moves:
            wins = self.simulate(move, simulate_times)
            uct = wins/simulate_times + math.sqrt(2*math.log(s_parent)/simulate_times)
            if uct > best_uct:
                best_move = move
        return best_move

    def simulate(self, move, s):
        wins = 0
        board = self.board
        board.make_move(move, self.color)
        for i in range(s):
            curr_turn = self.opponent[self.color]
            t = 0

            moves = board.get_all_possible_moves(curr_turn)
            while len(moves) > 0 and t <= 30:

            for turn in range(20):
                if board.is_win(self.color) == self.color:
                    wins = 1
                    self.undo(board, t)
                    break
                elif board.is_win(self.opponent[self.color]) == self.opponent[self.color]:
                    self.undo(board, t)
                    break
                moves = board.get_all_possible_moves(curr_turn)

                index = randint(0,len(moves)-1)
                inner_index = randint(0,len(moves[index])-1)
                board.make_move(moves[index][inner_index], curr_turn)
                curr_turn = self.opponent[curr_turn]
                moves = board.get_all_possible_moves(curr_turn)
                t += 1
            wins += 1 if board.is_win(curr_turn) == self.color else -1
            self.undo(board, t)
        board.undo()
        return wins

    def undo(self, board, times):
        for _ in range(times):
            board.undo()

    def min_value(self, move, depth, alpha, beta):
        self.board.make_move(move, self.opponent[self.color])

        if depth == 0 or time.time() - self.time > 8:
            u = self.utility(self.board, depth)
            self.board.undo()
            return u

        moves = self.board.get_all_possible_moves(self.color)
        if len(moves) == 0:
            u = self.utility(self.board, depth)
            u -= 10
            self.board.undo()
            return u

        min_val = math.inf
        for chess in moves:
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

        if depth == 0 or time.time() - self.time > 8:
            u = self.utility(self.board, depth)
            self.board.undo()
            return u

        moves = self.board.get_all_possible_moves(self.opponent[self.color])
        if len(moves) == 0:
            u = self.utility(self.board, depth)
            u += 10
            self.board.undo()
            return u

        max_val = - math.inf
        for chess in moves:
            for move in chess:
                max_val = max(self.min_value(move, depth - 1, alpha, beta), max_val)
                alpha = max(alpha, max_val)
                if alpha >= beta:
                    self.board.undo()
                    return max_val
        self.board.undo()
        return max_val


    def utility(self, board, depth):
        u = 0
        # u = board.is_win(self.color)
        # u = 0 if u == 0 else 10 if u == 2 else -10
        if self.movecount + depth < 15:
            time_param = math.log(self.movecount) + depth
            # u = self.wcount_bcount(board) + self.wking_bking(board) * time_param + \
            #     self.wback_bback(board) * (1/time_param) + self.wedge_bedge(board)
            u += self.wcount_bcount(board) + self.wking_bking(board) * time_param
        elif self.movecount + depth > 35:
            # time_param = math.log(self.movecount) + 1
            u += self.wcount_bcount(board) # + self.wback_bback(board) * (1/time_param) + self.wedge_bedge(board)
        else:
            time_param = math.log(self.movecount) + depth
            u += self.wcount_bcount(board) + self.wking_bking(board)
            # u += self.wcount_bcount(board) + self.wking_bking(board) * time_param * 0.5 + \
            #     self.wback_bback(board) * (1/time_param) * 0.1 + self.wedge_bedge(board) * 0.1* (1/time_param)
        return u if self.color == 2 else -u


    def wcount_bcount(self, board):
        return board.white_count - board.black_count


    def wking_bking(self, board):
        bking, wking = 0, 0
        for r in range(self.board.row):
            for c in range(self.board.col):
                if self.board.board[r][c].color == "B":
                    bking += self.board.board[r][c].is_king
                elif self.board.board[r][c].color == "W":
                    wking += self.board.board[r][c].is_king
        return wking - bking

    def wback_bback(self, board):
        bback = sum(board.board[0][i].color == "B" for i in range(board.col))
        wback = sum(board.board[board.row - 1][i].color == "W" for i in range(board.col))
        return wback - bback

    def wedge_bedge(self, board):
        bedge = sum(
            board.board[i][0].color == "B" + board.board[i][board.col - 1].color == "B" for i in
            range(board.row))
        wedge = sum(
            board.board[i][0].color == "W" + board.board[i][board.col - 1].color == "W" for i in
            range(board.row))
        return wedge - bedge

    def wdiagonal_bdiagonal(self, board):
        bdiagonal = sum(board.board[i][i].color == "B"  for i in range(board.row))
        wdiagonal = sum(board.board[i][i].color == "W"  for i in range(board.row))
        return wdiagonal - bdiagonal