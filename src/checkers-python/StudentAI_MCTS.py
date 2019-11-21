from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
import copy
import time
from collections import defaultdict

class Node():
    '''Node of Monte Carlo Tree'''
    def __init__(self, board, parent, turn):
        self.board = copy.deepcopy(board)
        self.parent = parent
        self.win = 0
        self.visit = 0
        self.turn = turn
        self.move = None

    def ucb(self, c, turn):
        # w = self.win if turn != self.turn else self.visit - self.win
        w = self.win
        return w/self.visit + c*math.sqrt(math.log(self.parent.visit)/self.visit)



class MonteCarloTree():
    '''
    Implement Monte Carlo Tree Search. Call get_action() to get the best move.
    '''
    def __init__(self, board, turn, opponent, reward):
        self.board = board
        self.turn = turn
        self.opponent = opponent
        self.reward = reward
        self.root = Node(board, None, self.turn)
        self.states = defaultdict(dict)
        self.states[str(self.board.board)][self.turn] = self.root
            # {board: {turn: node}} => s[str(board)][turn] = node
            # save the turn that this board can get move

    def get_action(self, simulate_time, depth):
        '''get the action'''
        t = 0
        start_time = time.time()
        children = self.expand(self.root) # get the children of root
        while time.time() - start_time < simulate_time:
            # select the best child
            best_child = self.best_child(children)
            # keep select the best way from the starting best child until reach a leaf
            select_node = self.select(best_child, depth)
            # simulate that leaf node
            w = self.simulate(select_node.board, select_node.turn)
            # update the information
            self.backpropagate(select_node, w)
            t += 1
        print(t)
        # select the best child
        best_move = self.best_child(children).move

        return best_move


    def select(self, node, depth):
        '''select the node'''
        if depth <= 0:
            return node
        child = self.best_child(self.expand(node))
        return self.select(child, depth - 1)

 #       return self.best_child(children)

    def expand(self, node):
        board = node.board
        turn = node.turn
        moves = self.get_moves(board, turn)

        # expand all possible children
        children = []
        for move in moves:
            board.make_move(move, turn)

            str_board = str(board.board)
            # if the board not states, simulate it
            if str_board not in self.states or turn not in self.states[str_board]:
                child = Node(board, node, self.opponent[turn])  # save the turn that can get move from this board
                child.move = move  # get the board with which move
                self.states[str_board][turn] = child
                win = self.simulate(board, turn)
                child.win = win
                child.visit = 1
                self.backpropagate(child, win)
            # else, get the board
            else:
                child = self.states[str_board][turn]
            children.append(child)

            board.undo()
        return children


    # simulate the game with a start move
    def simulate(self, board, turn):
        curr_turn = turn
        t = 1
        moves = self.get_moves(board, curr_turn)
        while len(moves) > 0 and t < 30:
            move = self.rollout(moves)
            board.make_move(move, curr_turn)
            curr_turn = self.opponent[curr_turn]
            moves = self.get_moves(board, curr_turn)
            t += 1
        self.undo(board, t-1)
        return self.reward[0] if curr_turn == self.opponent[turn] else self.reward[2] if t < 30 else self.reward[1]


    def backpropagate(self, node, win):
        '''Update the new information back to the parents and root'''
        if not node.parent:
            return
        node.parent.win += win
        node.parent.visit += 1
        self.backpropagate(node.parent, win)


    def best_child(self, children):
        '''Use ucb to select the best child'''
        best_ucb = 0
        best_node = []
        for child in children:
            ucb = child.ucb(1.4, child.turn)
            if ucb > best_ucb:
                best_ucb = ucb
                best_node = [child]
            elif ucb == best_ucb:
                best_node.append(child)
        return best_node[randint(0,len(best_node)-1)]


    def rollout(self, moves):
        '''Random roll a move from moves'''
        # index = randint(0,len(moves)-1)
        # inner_index = randint(0,len(moves[index])-1)
        # move = moves[index][inner_index]
        return moves[randint(0, len(moves)-1)]


    def get_moves(self, board, turn):
        return [m for chess in board.get_all_possible_moves(turn) for m in chess]

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
        mct = MonteCarloTree(self.board, self.color, self.opponent, (1,0.5,0))
        move = mct.get_action(10, 2)
        self.board.make_move(move, self.color)
        return move
