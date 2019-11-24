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
        self.movecount = 0
        self.simulate_times = 1000
        self.file = open(f"{self.col}-{self.row}-data.txt", "a")



    def get_move(self,move):
        self.movecount += 1
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        moves = self.get_moves(self.board, self.color)
        move = self.monte_carlo_tree(moves, self.simulate_times)
        self.board.make_move(move, self.color)
        return move

    def monte_carlo_tree(self, moves: [], simulate_times: int):
        s_parent = simulate_times * len(moves)
        best_uct = - math.inf
        best_move = 0
        for move in moves:
            wins = self.simulate(move, simulate_times)
            uct = wins/simulate_times + math.sqrt(2*math.log(s_parent)/simulate_times)
            if uct > best_uct:
                best_move = move
        return best_move

    def simulate(self, move, simulate_times):
        win = 0
        self.board.make_move(move, self.color)
        for _ in range(simulate_times):
            curr_turn = self.opponent[self.color]
            t = 0
            moves = self.get_moves(self.board, curr_turn)
            while len(moves) > 0 and t < 50:
                move = self.rollout(moves)
                self.board.make_move(move, curr_turn)
                curr_turn = self.opponent[curr_turn]
                moves = self.get_moves(self.board, curr_turn)
                t += 1
            win += 1 if curr_turn != self.color else 0 if t != 50 else 0.5
            self.undo(self.board, t)
        print(win/simulate_times * 100)
        self.file.write(f"{self.board_to_feature(self.board)} {win/simulate_times * 100}\n")
        self.board.undo()
        return win

    def board_to_feature(self, board):
        result = ""
        result += f"{board.black_count} {board.white_count} "

        wking,bking  = self.wking_bking(board)
        result += f"{wking} {bking} "

        wback, bback = self.wback_bback(board)
        result += f"{wback} {bback} "

        wedge, bedge = self.wedge_bedge(board)
        result += f"{wedge} {bedge} "

        wdiagonal, bdiagonal = self.wdiagonal_bdiagonal(board)
        result += f"{wdiagonal} {bdiagonal} "

        wdis, bdis = self.wdis_bdis(board)
        result += f"{wdis} {bdis} "

        result += str(self.movecount)

        return result


    def wking_bking(self, board):
        bking, wking = 0, 0
        for r in range(self.board.row):
            for c in range(self.board.col):
                if self.board.board[r][c].color == "B":
                    bking += self.board.board[r][c].is_king
                elif self.board.board[r][c].color == "W":
                    wking += self.board.board[r][c].is_king
        return wking, bking

    def wback_bback(self, board):
        bback = sum(board.board[0][i].color == "B" for i in range(board.col))
        wback = sum(board.board[board.row - 1][i].color == "W" for i in range(board.col))
        return wback, bback

    def wedge_bedge(self, board):
        bedge = sum(
            board.board[i][0].color == "B" + board.board[i][board.col - 1].color == "B" for i in
            range(board.row))
        wedge = sum(
            board.board[i][0].color == "W" + board.board[i][board.col - 1].color == "W" for i in
            range(board.row))
        return wedge, bedge

    def wdiagonal_bdiagonal(self, board):
        bdiagonal = sum(board.board[i][i].color == "B"  for i in range(board.row//4, 3*board.row//4)) + \
                    sum(board.board[board.row - 1 - i][board.row - 1 - i].color == "B"  for i in range(board.row))
        wdiagonal = sum(board.board[i][i].color == "W"  for i in range(board.row)) + \
                    sum(board.board[board.row - 1 - i][board.row - 1 - i].color == "W" for i in range(board.row))
        return wdiagonal, bdiagonal


    def wdis_bdis(self, board):
        wdis = sum(board.row - 1 - i for i in range(board.row) for j in range(board.col) if board.board[i][j].color == "W")
        bdis = sum(i for i in range(board.row) for j in range(board.col) if board.board[i][j].color == "B")
        return wdis, bdis



    ######### help function #########
    def rollout(self, moves):
        '''Random roll a move from moves'''
        return moves[randint(0, len(moves)-1)]

    def get_moves(self, board, turn):
        return [m for chess in board.get_all_possible_moves(turn) for m in chess]

    def undo(self, board, times):
        for _ in range(times):
            board.undo()