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
        self.depth = 6
        self.movecount = 1
        self.start = time.time()
        #self.theta = [8.61043154e+00,  4.48291855e+00,  7.78473553e+00, -7.07767178e-14,2.06230092e+00,  1.18768964e+00]#, 0]
        #self.theta = [ 1.77478239e+01, -2.06957248e+00,  1.34482992e+00, -9.76996262e-15,
       #-2.57914175e-01, -5.09654566e-01, -4.29094492e+00,  1.78097634e+00,
       #-8.69330850e-01,  0.00000000e+00]


    def get_move(self, move):
        #print(self.color)
        self.time = time.time()
        if self.time - self.start > 400:
            self.depth = 4
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
        for chess in moves:
            for move in chess:
                val = self.max_value(move, self.depth, -math.inf, math.inf)
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
                index = randint(0,len(moves)-1)
                inner_index = randint(0,len(moves[index])-1)
                board.make_move(moves[index][inner_index], curr_turn)
                curr_turn = self.opponent[curr_turn]
                moves = board.get_all_possible_moves(curr_turn)
                t += 1
            wins += -1 if curr_turn == self.color else 1
            self.undo(board, t)
        board.undo()
        return wins

    def undo(self, board, times):
        for _ in range(times):
            board.undo()

    def min_value(self, move, depth, alpha, beta):
        self.board.make_move(move, self.opponent[self.color])

        if depth == 0 or time.time() - self.time > 8:
            u = self.utility(self.board, self.color, depth)
            self.board.undo()
            return u

        moves = self.board.get_all_possible_moves(self.color)
        if len(moves) == 0:
            u = self.utility(self.board, self.color, depth)
            #u -= 1000
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
            u = self.utility(self.board, self.opponent[self.color], depth)
            self.board.undo()
            return u

        moves = self.board.get_all_possible_moves(self.opponent[self.color])
        if len(moves) == 0:
            u = self.utility(self.board, self.opponent[self.color], depth)
            #u += 1000
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

    def utility(self, board, color, depth):
        wking, bking = self.wking_bking(board)
        wcount, bcount = self.wcount_bcount(board)
        wdis, bdis = self.wdis_bdis(board)
        wedge, bedge = self.wedge_bedge(board)
        wcenter, bcenter = self.wcenter_bcenter(board)
        wback, bback = self.wback_bback(board)

        wdiag, bdiag = self.wdiag_bdiag(board)
        wdog, bdog = self.wdog_bdog(board)
        wbridge, bbridge = self.wbridge_bbridge(board)
        wuptriangle, buptriangle = self.wuptriangle_buptriangle(board)
        wdowntriangle, bdowntriangle = self.wdowntriangle_bdowntriangle(board)
        woreo, boreo = self.woreo_boreo(board)

        movelen, eatable = self.moveables(board, color)

        wscore = 5*wking + 3*wcount + 0.01*wdis + 0.001*wback + 0.0001*wedge + 0.00001*wcenter \
                + 0.001*wdiag + 0.001*wdog + 0.001*wbridge + 0.001*wuptriangle + 0.001* wdowntriangle \
                + 0.001 * woreo
        bscore = 5 * bking + 3 * bcount + 0.01 * bdis + 0.001 * bback + 0.0001 * bedge + 0.00001 * bcenter\
                + 0.001*bdiag + 0.001*bdog + 0.001*bbridge + 0.001*buptriangle + 0.001* bdowntriangle \
                + 0.001 * boreo
        if color == 2:
            wscore += movelen*0.01 + eatable*0.01
        else:
            bscore += movelen*0.01 + eatable*0.01
        # wscore = 5 * wking + 3 * wcount + 0.01 * wdis + 0.001 * wback + 0.0001 * wedge + 0.00001 * wcenter
        # bscore = 5 * bking + 3 * bcount + 0.01 * bdis + 0.001 * bback + 0.0001 * bedge + 0.00001 * bcenter

        return wscore-bscore if self.color == 2 else bscore-wscore

    def features(self, board, color):
        '''
        :param board:
        :return: white_features, black_features
            features order = [count, king, dis, back, edge,
                            center, diag, dog, bridge, uptriangle,
                            downtriangle, oreo, moveable, eatable]
        '''
        wfeature = [0 for _ in range(14)]
        bfeature = [0 for _ in range(14)]
        wfeature[0], bfeature[0] = board.white_count, board.black_count

        for r in range(board.row):
            # count edge
            wfeature[4] += (board.board[r][0].color == "W") + (board.board[r][board.col - 1].color == "W")
            bfeature[4] += (board.board[r][0].color == "B") + (board.board[r][board.col - 1].color == "B")

            for c in range(board.col):
                if board.board[r][c].color == 'W':
                    if board.board[r][c].is_king:
                        wfeature[1] += 1   ## count king
                    wfeature[2] += board.row - 1 - r    ## count dis
                elif board.board[r][c].color == 'B':
                    if board.board[r][c].is_king:
                        bfeature[1] += 1    ## count king
                    bfeature[2] += r    ## count dis



    def wcount_bcount(self, board):
        return board.white_count , board.black_count


    def wking_bking(self, board):
        bking, wking = 0, 0
        for r in range(self.board.row):
            for c in range(self.board.col):
                if self.board.board[r][c].color == "B":
                    bking += self.board.board[r][c].is_king
                elif self.board.board[r][c].color == "W":
                    wking += self.board.board[r][c].is_king
        return wking, bking

    def moveables(self, board, color):
        moves = [m for chess in board.get_all_possible_moves(color) for m in chess]
        eatable = 0
        for m in moves:
            if len(m.seq) > 2:
                eatable += (len(m.seq) - 1)
                continue
            if math.sqrt((m.seq[0][0] - m.seq[1][0]) ** 2 + (m.seq[0][1] - m.seq[1][1]) ** 2) > 1:
                eatable += 1
        print(f"len(moves): {len(moves)}, eatable: {eatable}")
        return len(moves), eatable


    def wback_bback(self, board):
        bback = sum(board.board[0][i].color == "B" for i in range(board.col))
        wback = sum(board.board[board.row - 1][i].color == "W" for i in range(board.col))
        return wback, bback


    def wedge_bedge(self, board):
        bedge = sum(
            (board.board[i][0].color == "B") + (board.board[i][board.col - 1].color == "B") for i in
            range(board.row))
        wedge = sum(
            (board.board[i][0].color == "W") + (board.board[i][board.col - 1].color == "W") for i in
            range(board.row))
        print(f"wedge: {wedge}, bedge: {bedge}")
        return wedge , bedge


    def wcenter_bcenter(self, board):
        wcenter = sum((board.board[int(board.row/2)][i].color =="W")+ \
                      (board.board[int(board.row/2)+1][i].color =="W") for i in range(board.col))
        bcenter = sum((board.board[int(board.row/2)][i].color == "B")+ \
                      (board.board[int(board.row/2)+1][i].color =="B") for i in range(board.col))
        print(f"wcenter: {wcenter}, bcenter: {bcenter}")
        return wcenter, bcenter

    def wdiagonal_bdiagonal(self, board):
        bdiagonal = sum(board.board[i][i].color == "B"  for i in range(board.row//4, 3*board.row//4)) + \
                    sum(board.board[board.row - 1 - i][board.row - 1 - i].color == "B"  for i in range(board.row))
        wdiagonal = sum(board.board[i][i].color == "W"  for i in range(board.row)) + \
                    sum(board.board[board.row - 1 - i][board.row - 1 - i].color == "W" for i in range(board.row))
        print(f"wdiagonal: {wdiagonal}, bdiagonal: {bdiagonal}")
        return wdiagonal , bdiagonal

    def wdiag_bdiag(self, board):
        bc,wc = 0, 0
        for r in range(board.row-1):
            bc += (board.board[r][r].color == "B") + (board.board[r+1][r].color == "B") + (board.board[r][r+1].color == "B") \
                + (board.board[r][board.col-1-r].color == "B") + (board.board[r+1][board.col-1-r].color == "B") +\
                   (board.board[r][board.col-2-r].color == "B")

            wc += (board.board[r][r].color == "W") + (board.board[r + 1][r].color == "W") + (board.board[r][r + 1].color == "W")\
                + (board.board[r][board.col-1-r].color == "W") + (board.board[r+1][board.col-1-r].color == "W") +\
                   (board.board[r][board.col-2-r].color == "W")
        bc += (board.board[board.row-1][0].color == "B") + (board.board[board.row-1][board.row-1].color == "B")
        wc += (board.board[board.row - 1][0].color == "W") + (board.board[board.row - 1][board.row - 1].color == "W")

        print(f"wdiag: {wc}, bdiag: {bc}")
        return wc, bc

    def wdog_bdog(self, board):
        wc = (board.board[board.row-1][board.col-1].color == "." and board.board[board.row-1][board.col-2].color == "W" \
            and board.board[board.row-2][board.col-1].color == "B") +\
             (board.board[board.row-1][0].color == "." and board.board[board.row-1][1].color == "W"\
            and board.board[board.row-2][0].color == "B")

        bc = (board.board[0][0].color == "." and board.board[0][1].color == "B" \
             and board.board[1][0].color == "W") + \
              (board.board[0][board.col-1].color == "." and board.board[0][board.col-2].color == "B" \
             and board.board[1][board.col-1].color == "W")
        print(f"wdog: {wc}, bdog: {bc}")
        return wc, bc


    def wbridge_bbridge(self, board):
        bc = sum(board.board[0][c].color == "B" and board.board[0][c+2].color == "B" for c in range(1, board.col - 3))
        wc = sum(board.board[board.row-1][c].color == "W" and board.board[board.row-1][c + 2].color == "W" for c in range(1, board.col - 3))
        print(f"wbridge: {wc}, bbridge: {bc}")
        return wc, bc

    def wuptriangle_buptriangle(self, board):
        bcount, wcount = 0, 0
        for r in range(1, board.row-1):
            for c in range(board.col-2):
                if board.board[r][c].color == "B" and board.board[r-1][c+1].color == "B" and board.board[r][c+2].color == "B":
                    bcount += 1
                if board.board[r][c].color == "W" and board.board[r-1][c+1].color == "W" and board.board[r][c+2].color == "W":
                    wcount += 1
        print(f"wuptriangle: {wcount}, buptriangle: {bcount}")
        return wcount, bcount

    def wdowntriangle_bdowntriangle(self, board):
        bcount, wcount = 0, 0
        for r in range(board.row-1):
            for c in range(board.col-2):
                if board.board[r][c].color == "B" and board.board[r+1][c+1].color == "B" and board.board[r][c+2].color == "B":
                    bcount += 1
                if board.board[r][c].color == "W" and board.board[r+1][c+1].color == "W" and board.board[r][c+2].color == "W":
                    wcount += 1
        print(f"wdowntriangle: {wcount}, bdowntriangle: {bcount}")
        return wcount, bcount


    def woreo_boreo(self, board):
        '''
        :param board:
        :return: triangle pattern in the last row
        '''
        boreo = sum(board.board[0][c].color == "B" and board.board[1][c+1].color == "B" \
                    and board.board[0][c+2].color == "B" for c in range(0, board.col-1))
        woreo = sum(board.board[board.row-1][c].color == "W" and board.board[board.row-2][c+1].color == "W" \
                    and board.board[board.row-1][c+2].color == "W" for c in range(0, board.col-1))
        print(f"woreo: {woreo}, boreo: {boreo}")
        return woreo, boreo


    def wdis_bdis(self, board):
        wdis = sum(board.row - 1 - i for i in range(board.row) for j in range(board.col) if board.board[i][j].color == "W")
        bdis = sum(i for i in range(board.row) for j in range(board.col) if board.board[i][j].color == "B")
        return wdis, bdis

