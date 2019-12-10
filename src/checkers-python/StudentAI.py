from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
import copy
import random

import time


# import numpy as np


# The following part should be completed by students.
# Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col, row, p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1: 2, 2: 1}
        self.color = 2
        self.movecount = 1

        self.file = f"{self.col}-{self.row}-{self.color}-{randint(0, 500)}-test.txt"
        self.start = time.time()

        self.theta1, self.theta2 = self.get_theta()
        self.cutoff = self.get_cutoff()

        # self.theta = [8.61043154e+00,  4.48291855e+00,  7.78473553e+00, -7.07767178e-14,2.06230092e+00,  1.18768964e+00]#, 0]
        # self.theta = [-24.13, -7.87, -17.89, -16.67, -6.99, 7.22, 1.19, 0.72,
        #               -4.2, -4.52, -2.49, -3.14, 5.69, 0.02, 3.53, -3.58, 9.37,
        #               -3.81, -1.58, -1.75, 2.51, 0.26, 18.3, 10.25, 3.63,
        #               3.69, 1.32, -4.03]
        # self.theta = [-57.35, -6.41, -2.09, -38.9, -3.91, 6.48, 11.97, -0.39, 27.23, 11.11, -22.04, -11.36, 39.62, -41.32,
        #    55.17, 24.54, 16.05, 12.08, 10.46, -17.8, 5.61, -7.38, 48.46, 20.26, 4.3, 2.54, 0.0, 0.0]
        # self.theta77 = [-1.49, 0.41, 0.0, -0.19, -0.07, 0.25, 0.13, 0.0, 0.0, 0.09, -0.28, -0.53, 3.83, -3.95,
        #     1.88, 0.93, 0.08, 0.25, 0.17, 0.0, -0.22, 0.0, -0.24, -0.2, -0.02, 0.03, 0.0, 0.0]
        # self.theta98 = [-1.76, -0.4, 0.03, -0.08, 0.16, 0.3, 0.16, 0.55, -0.38, -0.17, -0.12, 0.28, 2.8, -2.77,
        #     1.82, 0.82, 0.22, 0.1, 0.09, -0.38, -0.09, -1.31, 0.78, 0.42, -0.02, 0.15, 0.0, 0.0]

    def get_move(self, move):
        print(self.color)

        self.time = time.time()
        # if self.time - self.start > 400:
        #     self.depth = 4
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)

        self.depth = self.get_depth()
        # index = randint(0,len(moves)-1)
        # inner_index =  randint(0,len(moves[index])-1)
        # move = moves[index][inner_index]
        # print(moves)
        move = moves[0][0] if len(moves) == 1 and len(moves[0]) == 1 else self.minimax_move(moves)
        self.board.make_move(move, self.color)
        self.movecount += 1
        # with open(self.file, 'a') as f:
        #     f.write(f"Movecount:{self.movecount} Total time:{time.time()-self.start} This move takes:{time.time()-self.time} Depth:{self.depth}\n")
        return move

    def get_cutoff(self):
        if self.row == 7 and self.col == 7:
            return (5, 3)
        else:
            return (6, 3)

    def get_depth(self):
        if self.row == 7 and self.col == 7:
            return 0
        else:
            return 4

    def get_theta(self):
        theta771_start = [-3.05, -1.9, 0.04, -0.85, -0.06, 0.43, 0.21, 0.0, -0.18, 0.56, -0.32, -0.25, 2.9, -2.56, 1.23,
                          0.06, 0.44, 0.89, 0.67, 0.27, -0.0, 0.0, 0.64, 0.56, 0.07, 0.91, 0.0, 0.0]
        theta771_mid = [-2.84, -1.09, -0.05, -0.67, 0.22, 0.42, 0.24, 0.0, -0.18, 0.72, 0.26, 0.38, 3.44, -2.88, 1.83,
                        0.04, 0.3, 0.79, 0.11, -0.02, -0.14, 0.0, 0.36, 0.3, -0.45, 0.9, 0.0, 0.0]
        theta771_last = [-3.01, -1.01, -0.06, 0.13, 0.42, 0.18, 0.03, 0.0, -0.51, 0.75, 1.31, 1.26, 2.86, -2.55, 1.5,
                         0.22, 0.05, 0.42, 0.2, -0.06, -0.16, 0.0, 0.53, 0.45, -0.26, 0.44, 0.0, 0.0]

        theta772_start = [2.07, -0.44, 0.29, 0.45, 0.32, -0.46, -0.04, 0.0, 0.37, -0.25, 0.16, 0.17, 0.0, 0.0, -2.18,
                          -0.62, -0.16, -1.0, 0.24, 0.72, 0.2, 0.0, 0.12, 0.04, 0.75, -1.29, 3.36, -2.93]
        theta772_mid = [1.93, 0.09, 0.16, 0.37, 0.28, -0.18, -0.17, 0.0, 0.02, -0.28, 0.02, 0.13, 0.0, 0.0, -2.3, -1.12,
                        -0.07, -0.63, 0.38, 0.08, 0.16, 0.0, -0.4, 0.43, 0.54, -0.74, 3.47, -3.05]
        theta772_last = [1.51, 0.44, -0.01, 0.11, 0.16, -0.16, -0.14, 0.0, -0.17, 0.47, -0.16, 0.02, 0.0, 0.0, -2.79,
                         -0.98, 0.0, 0.14, 0.4, -0.08, 0.0, 0.0, -0.26, 1.25, 0.06, -0.07, 2.32, -2.19]

        theta981_start = [-2.85, -0.22, 0.11, -0.54, 0.31, -0.03, 0.07, 0.0, -0.19, 0.45, -0.17, 0.45, 2.09, -1.88,
                          2.46, 1.24, -0.04, 0.64, 0.41, -0.36, 0.11, 0.25, -0.01, 0.09, -0.34, 0.96, 0.0, 0.0]
        theta981_mid = [-1.95, -1.35, 0.11, -0.44, 0.11, 0.16, 0.02, 0.0, -0.18, 0.57, 0.26, 0.54, 2.37, -2.06, 1.22,
                        -0.19, 0.3, 0.9, 0.43, 0.09, 0.05, -0.06, 0.19, 0.19, -0.04, 0.69, 0.0, 0.0]
        theta981_last = [-3.22, -1.85, 0.18, 0.48, 0.23, 0.14, -0.18, 0.0, -0.53, 1.25, 0.93, 0.03, 3.33, -3.01, 2.08,
                         0.05, 0.15, 0.65, 0.27, 0.03, -0.13, -1.0, -0.24, -0.25, 0.01, 0.03, 0.0, 0.0]

        theta982_start = [1.47, -0.0, 0.21, 0.5, 0.09, -0.09, 0.05, 0.0, 0.12, -0.45, 0.15, 0.55, 0.0, 0.0, -2.5, -0.49,
                          0.05, -0.45, 0.24, 0.24, 0.29, 0.29, 0.02, 0.12, 0.26, -0.26, 2.31, -2.11]
        theta982_mid = [1.22, -0.16, 0.29, 0.22, 0.28, -0.21, -0.05, 0.0, 0.38, -0.24, -0.31, 0.59, 0.0, 0.0, -2.04,
                        -1.22, 0.14, -0.54, 0.12, -0.07, 0.05, -0.04, 0.31, 0.57, 0.41, -0.88, 3.14, -2.84]
        theta982_last = [2.12, -0.19, 0.19, -0.23, 0.33, -0.17, -0.11, 0.0, -0.44, 0.32, 0.16, 0.0, 0.0, 0.0, -2.06,
                         -1.58, 0.09, -0.16, 0.46, -0.19, 0.0, -0.94, -0.7, 0.74, 1.33, -0.08, 4.14, -3.98]

        if self.row == 7 and self.col == 7:
            return (theta771_start, theta771_mid, theta771_last), (theta772_start, theta772_mid, theta772_last)
        else:
            return (theta981_start, theta981_mid, theta981_last), (theta982_start, theta982_mid, theta982_last)

    def minimax_move(self, moves: [list]):
        best = []
        max_value = - math.inf
        for chess in moves:
            for move in chess:
                val = self.min_value(move, self.depth, -math.inf, math.inf)
                if val > max_value:
                    best = [move]
                    max_value = val
                elif val == max_value:
                    best.append(move)
        return best[0]

    def min_value(self, move, depth, alpha, beta):
        self.board.make_move(move, self.color)

        if depth == 0:
            u = self.utility(self.board, self.color)
            print(u)
            self.board.undo()
            return u

        moves = self.board.get_all_possible_moves(self.opponent[self.color])
        moves = [m for sub in moves for m in sub]
        # moves = self.reorder(self.get_u_list(moves, self.board, self.opponent[self.color]), reverse = False)

        if len(moves) == 0:
            u = +1000
            self.board.undo()
            return u

        min_val = math.inf
        for move in moves:
            min_val = min(self.max_value(move, depth - 1, alpha, beta), min_val)
            beta = min(beta, min_val)
            if alpha >= beta:
                self.board.undo()
                return min_val
        self.board.undo()
        return min_val

    def max_value(self, move, depth, alpha, beta):
        self.board.make_move(move, self.opponent[self.color])

        if depth == 0:
            u = self.utility(self.board, self.opponent[self.color])
            print(u)
            self.board.undo()
            return u

        moves = self.board.get_all_possible_moves(self.color)
        moves = [m for sub in moves for m in sub]
        # moves = self.reorder(self.get_u_list(moves, self.board, self.color), reverse = True)

        if len(moves) == 0:
            u = -1000
            self.board.undo()
            return u

        max_val = - math.inf
        for move in moves:
            max_val = max(self.min_value(move, depth - 1, alpha, beta), max_val)
            alpha = max(alpha, max_val)
            if alpha >= beta:
                self.board.undo()
                return max_val
        self.board.undo()
        return max_val

    def u_after_move(self, move, board, color):
        board.make_move(move, color)
        u = self.utility(board, color)
        board.undo()
        return u

    def get_u_list(self, moves, board, color):
        u_list = {}
        for chess in moves:
            for move in chess:
                u_list[move] = self.u_after_move(move, board, color)
        return u_list

    def reorder(self, u_list, reverse):
        return sorted(u_list, key=lambda x: u_list[x], reverse=reverse)

    def utility(self, board, color):
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
        board.show_board()
        if color == 1:
            wmoveable, weatable = self.moveables(board, 2)
            bmoveable, beatable = 0, 0
        else:
            wmoveable, weatable = 0, 0
            bmoveable, beatable = self.moveables(board, 1)

        if self.color == 1:
            features = [wcount, wking, wdis, wback, wedge,
                        wcenter, wdiag, wdog, wbridge, wuptriangle,
                        wdowntriangle, woreo, wmoveable, weatable,
                        bcount, bking, bdis, bback, bedge,
                        bcenter, bdiag, bdog, bbridge, buptriangle,
                        bdowntriangle, boreo, bmoveable, beatable]
            print(str([i for i in features]))
            if bcount > self.cutoff[0]:
                return sum(x * t for x, t in zip(features, self.theta1[0]))
            elif self.cutoff[1] < bcount <= self.cutoff[0]:
                return sum(x * t for x, t in zip(features, self.theta1[1]))
            else:
                return sum(x * t for x, t in zip(features, self.theta1[2]))


        else:
            features = [wcount, wking, wdis, wback, wedge,
                        wcenter, wdiag, wdog, wbridge, wuptriangle,
                        wdowntriangle, woreo, wmoveable, weatable,
                        bcount, bking, bdis, bback, bedge,
                        bcenter, bdiag, bdog, bbridge, buptriangle,
                        bdowntriangle, boreo, bmoveable, beatable]
            print(str([i for i in features]))
            if wcount > self.cutoff[0]:
                return sum(x * t for x, t in zip(features, self.theta2[0]))
            elif self.cutoff[1] < wcount <= self.cutoff[0]:
                return sum(x * t for x, t in zip(features, self.theta2[1]))
            else:
                return sum(x * t for x, t in zip(features, self.theta2[2]))

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
                wfeature[3] += (board.board[board.row - 1][c].color == "B")  # count back
                bfeature[3] += (board.board[0][c].color == "B")  # count back

                wfeature[5] += (board.board[int(board.row / 2)][c].color == "W") + (
                        board.board[int(board.row / 2) + 1][c].color == "W")  # count center
                bfeature[5] += (board.board[int(board.row / 2)][c].color == "B") + (
                        board.board[int(board.row / 2) + 1][c].color == "B")  # count center

                if board.board[r][c].color == 'W':
                    if board.board[r][c].is_king:
                        wfeature[1] += 1  # count king
                    wfeature[2] += board.row - 1 - r  # count dis
                elif board.board[r][c].color == 'B':
                    if board.board[r][c].is_king:
                        bfeature[1] += 1  # count king
                    bfeature[2] += r  # count dis

    def wcount_bcount(self, board):
        return board.white_count, board.black_count

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
        # print(f"len(moves): {len(moves)}, eatable: {eatable}")
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
        # print(f"wedge: {wedge}, bedge: {bedge}")
        return wedge, bedge

    def wcenter_bcenter(self, board):
        wcenter = sum((board.board[int(board.row / 2)][i].color == "W") + \
                      (board.board[int(board.row / 2) + 1][i].color == "W") for i in range(board.col))
        bcenter = sum((board.board[int(board.row / 2)][i].color == "B") + \
                      (board.board[int(board.row / 2) + 1][i].color == "B") for i in range(board.col))
        # print(f"wcenter: {wcenter}, bcenter: {bcenter}")
        return wcenter, bcenter

    def wdiagonal_bdiagonal(self, board):
        bdiagonal = sum(board.board[i][i].color == "B" for i in range(board.row // 4, 3 * board.row // 4)) + \
                    sum(board.board[board.row - 1 - i][board.row - 1 - i].color == "B" for i in range(board.row))
        wdiagonal = sum(board.board[i][i].color == "W" for i in range(board.row)) + \
                    sum(board.board[board.row - 1 - i][board.row - 1 - i].color == "W" for i in range(board.row))
        # print(f"wdiagonal: {wdiagonal}, bdiagonal: {bdiagonal}")
        return wdiagonal, bdiagonal

    def wdiag_bdiag(self, board):
        bc, wc = 0, 0
        for r in range(board.row - 1):
            bc += (board.board[r][r].color == "B") + (board.board[r + 1][r].color == "B") + (
                    board.board[r][r + 1].color == "B") \
                  + (board.board[r][board.col - 1 - r].color == "B") + (
                          board.board[r + 1][board.col - 1 - r].color == "B") + \
                  (board.board[r][board.col - 2 - r].color == "B")

            wc += (board.board[r][r].color == "W") + (board.board[r + 1][r].color == "W") + (
                    board.board[r][r + 1].color == "W") \
                  + (board.board[r][board.col - 1 - r].color == "W") + (
                          board.board[r + 1][board.col - 1 - r].color == "W") + \
                  (board.board[r][board.col - 2 - r].color == "W")
        bc += (board.board[board.row - 1][0].color == "B") + (board.board[board.row - 1][board.row - 1].color == "B")
        wc += (board.board[board.row - 1][0].color == "W") + (board.board[board.row - 1][board.row - 1].color == "W")

        # print(f"wdiag: {wc}, bdiag: {bc}")
        return wc, bc

    def wdog_bdog(self, board):
        wc = (board.board[board.row - 1][board.col - 1].color == "." and board.board[board.row - 1][
            board.col - 2].color == "W" \
              and board.board[board.row - 2][board.col - 1].color == "B") + \
             (board.board[board.row - 1][0].color == "." and board.board[board.row - 1][1].color == "W" \
              and board.board[board.row - 2][0].color == "B")

        bc = (board.board[0][0].color == "." and board.board[0][1].color == "B" \
              and board.board[1][0].color == "W") + \
             (board.board[0][board.col - 1].color == "." and board.board[0][board.col - 2].color == "B" \
              and board.board[1][board.col - 1].color == "W")
        # print(f"wdog: {wc}, bdog: {bc}")
        return wc, bc

    def wbridge_bbridge(self, board):
        bc = sum(board.board[0][c].color == "B" and board.board[0][c + 2].color == "B" for c in range(1, board.col - 3))
        wc = sum(board.board[board.row - 1][c].color == "W" and board.board[board.row - 1][c + 2].color == "W" for c in
                 range(1, board.col - 3))
        # print(f"wbridge: {wc}, bbridge: {bc}")
        return wc, bc

    def wuptriangle_buptriangle(self, board):
        bcount, wcount = 0, 0
        for r in range(1, board.row - 1):
            for c in range(board.col - 2):
                if board.board[r][c].color == "B" and board.board[r - 1][c + 1].color == "B" and board.board[r][
                    c + 2].color == "B":
                    bcount += 1
                if board.board[r][c].color == "W" and board.board[r - 1][c + 1].color == "W" and board.board[r][
                    c + 2].color == "W":
                    wcount += 1
        # print(f"wuptriangle: {wcount}, buptriangle: {bcount}")
        return wcount, bcount

    def wdowntriangle_bdowntriangle(self, board):
        bcount, wcount = 0, 0
        for r in range(board.row - 1):
            for c in range(board.col - 2):
                if board.board[r][c].color == "B" and board.board[r + 1][c + 1].color == "B" and board.board[r][
                    c + 2].color == "B":
                    bcount += 1
                if board.board[r][c].color == "W" and board.board[r + 1][c + 1].color == "W" and board.board[r][
                    c + 2].color == "W":
                    wcount += 1
        # print(f"wdowntriangle: {wcount}, bdowntriangle: {bcount}")
        return wcount, bcount

    def woreo_boreo(self, board):
        '''
        :param board:
        :return: triangle pattern in the last row
        '''
        boreo = sum(board.board[0][c].color == "B" and board.board[1][c + 1].color == "B" \
                    and board.board[0][c + 2].color == "B" for c in range(0, board.col - 2))
        woreo = sum(board.board[board.row - 1][c].color == "W" and board.board[board.row - 2][c + 1].color == "W" \
                    and board.board[board.row - 1][c + 2].color == "W" for c in range(0, board.col - 2))
        # print(f"woreo: {woreo}, boreo: {boreo}")
        return woreo, boreo

    def wdis_bdis(self, board):
        wdis = sum(
            board.row - 1 - i for i in range(board.row) for j in range(board.col) if board.board[i][j].color == "W")
        bdis = sum(i for i in range(board.row) for j in range(board.col) if board.board[i][j].color == "B")
        return wdis, bdis
