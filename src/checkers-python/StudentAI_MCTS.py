from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
import copy
import time

class Node():
    def __init__(self, board, parent, turn):
        self.board = copy.deepcopy(board)
        self.parent = parent
        self.win = 0
        self.visit = 0
        self.turn = turn
        self.move = None


    def ucb(self, c):
        return self.win/self.visit + c*math.sqrt(math.log(self.parent.visit)/self.visit)


class MonteCarloTree():
    def __init__(self, board, moves, color, opponent):
        self.board = board
        self.moves = moves
        self.color = color
        self.opponent = opponent
        self.root = Node(board, None, self.color)
        self.states = {str(self.board.board): self.root} # {board: node}

    def get_action(self, simulate_time, reward):
        # curr_move = self.select(self.root, self.color)
        t = 0
        self.reward = reward
        start_time = time.time()
        children = self.select(self.root, self.color)
        while time.time() - start_time < simulate_time:
            select_node = self.best_child(children)
            # select_node = self.select(self.root, self.root.turn)
            w = self.simulate(select_node.board, select_node.turn, reward)
            self.backpropagate(select_node, w)
            t += 1
        print(t)
        # select the best child
        best_move = self.best_child(children).move

        return best_move



    # random roll a move
    def rollout(self, moves):
        # index = randint(0,len(moves)-1)
        # inner_index = randint(0,len(moves[index])-1)
        # move = moves[index][inner_index]
        return moves[randint(0, len(moves)-1)]



    def best_child(self, children):
        best_ucb = 0
        best_node = None
        for child in children:
            ucb = child.ucb(1.4)
            if ucb > best_ucb:
                best_ucb = ucb
                best_node = child
        return best_node


    def select(self, node, turn):
        board = node.board
        moves = board.get_all_possible_moves(turn)

        # explore all possible children
        children = []
        for chess in moves:
            for move in chess:
                board.make_move(move, turn)
                child = Node(board, node, turn)
                child.move = move # get the board with which move
                children.append(child)
                self.states[str(board.board)+str(turn)] = child

                win = self.simulate(board, turn, self.reward)
                child.win = win
                child.visit = 1
                self.backpropagate(child, win)

                board.undo()
        return children
 #       return self.best_child(children)


    # simulate the game with a start move
    def simulate(self, board, color, reward):
        curr_turn = self.opponent[color]
        t = 0
        moves = [m for chess in board.get_all_possible_moves(curr_turn) for m in chess]
        while len(moves) == 0 and t < 30:
            move = self.rollout(moves)
            board.make_move(move, curr_turn)
            curr_turn = self.opponent[curr_turn]
            moves = [m for chess in board.get_all_possible_moves(curr_turn) for m in chess]
            t += 1
        self.undo(board, t)
        return reward[0] if curr_turn == self.opponent[color] else reward[2] if t < 30 else reward[1]


    def backpropagate(self, node, win):
        if not node.parent:
            return
        node.parent.win += win
        node.parent.visit += 1
        self.backpropagate(node.parent, win)


    def undo(self, board, times):
        for _ in range(times):
            board.undo()



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
        # index = randint(0,len(moves)-1)
        # inner_index =  randint(0,len(moves[index])-1)
        # move = moves[index][inner_index]
        mct = MonteCarloTree(self.board, moves, self.color, self.opponent)
        move = mct.get_action(10, (1,0,0))
        self.board.make_move(move, self.color)
        return move
