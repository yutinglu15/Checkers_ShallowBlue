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
        self.simulate_times = 100
        self.file = f"{self.col}-{self.row}-{self.color}-data.txt"
        # self.file = open(f"{self.col}-{self.row}-data.txt", "a")



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
        bf, wf = self.board_to_feature(self.board, self.color)
        self.write_to_file(bf, wf, win/simulate_times*100)
        self.board.undo()
        return win

    def board_to_feature(self, board, color):

        # result = ""
        # result += f"{board.white_count/self.total} {board.black_count/self.total} "
        #
        # wking,bking  = self.wking_bking(board)
        # result += f"{wking/self.total} {bking/self.total} "
        #
        # wback, bback = self.wback_bback(board)
        # result += f"{wback/self.total} {bback/self.total} "
        #
        # wedge, bedge = self.wedge_bedge(board)
        # result += f"{wedge/self.total} {bedge/self.total} "
        #
        # wdiagonal, bdiagonal = self.wdiagonal_bdiagonal(board)
        # result += f"{wdiagonal/self.total} {bdiagonal/self.total} "
        #
        # wdis, bdis = self.wdis_bdis(board)
        # result += f"{wdis/self.total} {bdis/self.total} "
        #
        # result += str(self.movecount)

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

        wmoveable, weatable = self.moveables(board, 2)
        bmoveable, beatable = self.moveables(board, 1)

        return [wcount, wking, wdis, wback, wedge,
                wcenter, wdiag, wdog, wbridge, wuptriangle,
                wdowntriangle, woreo, wmoveable, weatable],\
                [bcount, bking, bdis, bback, bedge,
                 bcenter, bdiag, bdog, bbridge, buptriangle,
                 bdowntriangle, boreo, bmoveable, beatable]


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
        return wedge , bedge


    def wcenter_bcenter(self, board):
        wcenter = sum((board.board[int(board.row/2)][i].color =="W")+ \
                      (board.board[int(board.row/2)+1][i].color =="W") for i in range(board.col))
        bcenter = sum((board.board[int(board.row/2)][i].color == "B")+ \
                      (board.board[int(board.row/2)+1][i].color =="B") for i in range(board.col))
        # print(f"wcenter: {wcenter}, bcenter: {bcenter}")
        return wcenter, bcenter

    def wdiagonal_bdiagonal(self, board):
        bdiagonal = sum(board.board[i][i].color == "B"  for i in range(board.row//4, 3*board.row//4)) + \
                    sum(board.board[board.row - 1 - i][board.row - 1 - i].color == "B"  for i in range(board.row))
        wdiagonal = sum(board.board[i][i].color == "W"  for i in range(board.row)) + \
                    sum(board.board[board.row - 1 - i][board.row - 1 - i].color == "W" for i in range(board.row))
        # print(f"wdiagonal: {wdiagonal}, bdiagonal: {bdiagonal}")
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

        # print(f"wdiag: {wc}, bdiag: {bc}")
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
        # print(f"wdog: {wc}, bdog: {bc}")
        return wc, bc


    def wbridge_bbridge(self, board):
        bc = sum(board.board[0][c].color == "B" and board.board[0][c+2].color == "B" for c in range(1, board.col - 3))
        wc = sum(board.board[board.row-1][c].color == "W" and board.board[board.row-1][c + 2].color == "W" for c in range(1, board.col - 3))
        # print(f"wbridge: {wc}, bbridge: {bc}")
        return wc, bc

    def wuptriangle_buptriangle(self, board):
        bcount, wcount = 0, 0
        for r in range(1, board.row-1):
            for c in range(board.col-2):
                if board.board[r][c].color == "B" and board.board[r-1][c+1].color == "B" and board.board[r][c+2].color == "B":
                    bcount += 1
                if board.board[r][c].color == "W" and board.board[r-1][c+1].color == "W" and board.board[r][c+2].color == "W":
                    wcount += 1
        # print(f"wuptriangle: {wcount}, buptriangle: {bcount}")
        return wcount, bcount

    def wdowntriangle_bdowntriangle(self, board):
        bcount, wcount = 0, 0
        for r in range(board.row-1):
            for c in range(board.col-2):
                if board.board[r][c].color == "B" and board.board[r+1][c+1].color == "B" and board.board[r][c+2].color == "B":
                    bcount += 1
                if board.board[r][c].color == "W" and board.board[r+1][c+1].color == "W" and board.board[r][c+2].color == "W":
                    wcount += 1
        # print(f"wdowntriangle: {wcount}, bdowntriangle: {bcount}")
        return wcount, bcount


    def woreo_boreo(self, board):
        '''
        :param board:
        :return: triangle pattern in the last row
        '''
        boreo = sum(board.board[0][c].color == "B" and board.board[1][c+1].color == "B" \
                    and board.board[0][c+2].color == "B" for c in range(0, board.col-2))
        woreo = sum(board.board[board.row-1][c].color == "W" and board.board[board.row-2][c+1].color == "W" \
                    and board.board[board.row-1][c+2].color == "W" for c in range(0, board.col-2))
        # print(f"woreo: {woreo}, boreo: {boreo}")
        return woreo, boreo


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

    def write_to_file(self, wfeatures, bfeatures, win_rate):
        with open(self.file, "a") as f:
            w = ' '.join(str(x) for x in wfeatures)
            b = ' '.join(str(x) for x in bfeatures)
            f.write(w + ' ' + b + ' ' + str(win_rate) + '\n')