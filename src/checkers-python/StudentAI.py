from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
import copy
import random

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
        self.movecount = 0

    def get_move(self, move):
        #print(self.color)
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)
        self.train()

        #index = randint(0,len(moves)-1)
        #inner_index =  randint(0,len(moves[index])-1)
        #move = moves[index][inner_index]
        #print(moves)
        move = self.minimax_move(moves)
        #move = self.monte_carlo_tree([m for chess in moves for m in chess], 10, 10)
        self.board.make_move(move, self.color)
        self.movecount += 1
        return move

    def minimax_move(self, moves: [list]) :
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
        if len(best) == 1:
            return best[randint(0,len(best)-1)]
        #print(len(best))
        return self.monte_carlo_tree(best, 10, 10)

    def monte_carlo_tree(self, moves: [], simulate_times: int, s_parent: int):
        best_uct = 0
        best_move = 0
        for move in moves:
            wins = self.simulate(move, simulate_times)
            uct = wins/simulate_times + math.sqrt(2*math.log(s_parent)/simulate_times)
            if uct > best_uct:
                best_move = move
        return best_move

    def simulate(self, move, s):
        wins = 0
        board = copy.deepcopy(self.board)
        board.make_move(move, self.color)
        for i in range(s):
            curr_turn = self.opponent[self.color]
            t = 0
            for turn in range(20):
                if board.is_win(self.color) == self.color:
                    wins = 1
                    self.undo(board,t)
                    break
                elif board.is_win(self.opponent[self.color]) == self.opponent[self.color]:
                    self.undo(board, t)
                    break
                moves = board.get_all_possible_moves(curr_turn)
                index = randint(0,len(moves)-1)
                inner_index =  randint(0,len(moves[index])-1)
                board.make_move(moves[index][inner_index], curr_turn)
                curr_turn = self.opponent[curr_turn]
                t += 1
            else:
                wins = 0.5
                self.undo(board, t)

        return wins

    def undo(self, board, times):
        for _ in range(times):
            board.undo()

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
        bking, wking = 0, 0
        for r in range(self.board.row):
            for c in range(self.board.col):
                if self.board.board[r][c].color == "B":
                    bking += self.board.board[r][c].is_king
                elif self.board.board[r][c].color == "W":
                    wking += self.board.board[r][c].is_king

        bback = sum(self.board.board[0][i].color == "B" for i in range(self.board.col))
        wback = sum(self.board.board[self.board.row-1][i].color == "W" for i in range(self.board.col))

        bedge = sum(self.board.board[i][0].color == "B"+self.board.board[i][self.board.col-1].color == "B" for i in range(self.board.row))
        wedge = sum(self.board.board[i][0].color == "W"+self.board.board[i][self.board.col-1].color == "W" for i in range(self.board.row))

        time_param = math.log(self.movecount)
        b = 3*self.board.black_count + bking * time_param + bback * (1/time_param) + bedge * (1/time_param)
        w = 3*self.board.white_count + wking * time_param + wback * (1/time_param) + wedge * (1/time_param)
        # b = self.board.black_count
        # w = self.board.white_count
        #print("black:",b," white:",w)
        return b-w if self.color == 1 else w-b


    ####################################################
    ### Training heuristics using Linear Regression ####
    ####################################################

    def get_X(self, board):
        bking, wking = 0, 0
        for r in range(self.board.row):
            for c in range(self.board.col):
                if self.board.board[r][c].color == "B":
                    bking += self.board.board[r][c].is_king
                elif self.board.board[r][c].color == "W":
                    wking += self.board.board[r][c].is_king

        bback = sum(self.board.board[0][i].color == "B" for i in range(self.board.col))
        wback = sum(self.board.board[self.board.row-1][i].color == "W" for i in range(self.board.col))

        bedge = sum(self.board.board[i][0].color == "B"+self.board.board[i][self.board.col-1].color == "B" for i in range(self.board.row))
        wedge = sum(self.board.board[i][0].color == "W"+self.board.board[i][self.board.col-1].color == "W" for i in range(self.board.row))

        X_black = [self.board.black_count, bking, bback, bedge, self.movecount]
        X_white = [self.board.white_count, wking, wback, wedge, self.movecount]

        return (X_black, X_white)

    def model(self, X, thetas):
        # X = [count, king, back, edge, time]
        # thetas = [t1, t2, t3, t4, t5]
        return thetas[0] * X[0] + thetas[1] * X[1] + thetas[2] * X[2] + thetas[3] * X[3] + thetas[4] * X[4]


    def train(self):
        thetas = [random.random() for i in range(5)]

        epoch = 0.01
        alpha = 0.05

        while True:
            thetas = thetas - self.Gradient() * alpha
            if self.Gradient() * alpha < epoch:
                break

        return thetas




    def MSE(self, thetas):
        # get mean square error by simulation
        mse = 0
        new_board = copy.deepcopy(self.board)

        utility = self.model(self.get_X(self.board), thetas)

        return mse

    def Gradient(self, mse):
        # calculate gradient according to mse
        pass
