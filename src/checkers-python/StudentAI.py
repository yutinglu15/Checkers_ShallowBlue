from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
import copy

class Node():
    def __init__(self, board, parent):
        self.board = copy.deepcopy(board)
        self.parent = parent
        self.win = 0
        self.visit = 0


    def ucb(self, c):
        return self.win/self.visit + c*math.sqrt(math.log(self.parent.visit)/self.visit)


class MonteCarloTree():
    def __init__(self, board, moves, color, opponent):
        self.board = board
        self.moves = moves
        self.color = color
        self.opponent = opponent
        self.root = Node(board, None)
        self.states = {str(self.board.board): self.root} # {board: node}

    def get_action(self, simulate_time):
        # simulate each child once
        children = []
        for move in self.moves:
            self.board.make_move(move, self.color)
            child = Node(self.board, self.root)
            child.move = move # get the board with which move
            children.append(child)
            self.states[str(self.board.board)] = child
            win = self.simulate(self.board, move)
            child.win = win
            child.visit = 1
            self.backpropagate(child, win)
            self.board.undo()

        # expand and simulate (if the board is unexplored, simulate and backpropagate
        # if the board is explored, rollout and move to one of its child)
        # ** should we consider the opponent's move as node in our board?
        # ** how can we include that? simply treat it as a normal node?
        for _ in simulate_time:
            move = self.rollout(self, self.board, self.color)
            if str(self.board.board) not in self.states:
                self.simulate()
            else:
                pass

        # select the best child
        best_ucb = 0
        best_move = None
        for child in children:
            ucb = child.ucb(1.4)
            if ucb > best_ucb:
                best_ucb = ucb
                best_move = child.move

        return best_move



    # random roll a move
    def rollout(self, moves):
        index = randint(0,len(moves)-1)
        inner_index =  randint(0,len(moves[index])-1)
        move = moves[index][inner_index]
        return move

    def get_node(self, board):
        return self.states[str(board.board)] if str(board.board) not in self.states else None


    # not sure about how to implement it yet...
    def expand(self):
        board = self.board
        t = 0
        curr_node = self.get_node(board)
        while curr_node:
            moves = board.get_all_possible_moves(self.color)
            move = self.rollout(moves)
            board.make_move(move, self.color)
            t += 1

            moves = board.get_all_possible_moves(self.opponent[self.color])
            move = self.rollout(moves)
            board.make_move(move, self.opponent[self.color])
            t += 1

            curr_node = self.get_node(board)

        # now curr_node is unexplored
        curr_node = Node(board)

        self.undo(board, t)


    # simulate the game with a start move
    def simulate(self, board, move):
        board.make_move(move, self.color)
        win = 0
        curr_turn = self.opponent[self.color]
        t = 0
        for turn in range(20):
            if board.is_win(self.color) == self.color:
                win = 1
                self.undo(board,t)
                break
            elif board.is_win(self.opponent[self.color]) == self.opponent[self.color]:
                self.undo(board, t)
                break
            move = self.rollout(board.get_all_possible_moves(curr_turn))
            board.make_move(move, curr_turn)
            curr_turn = self.opponent[curr_turn]
            t += 1
        else:
            win += 0.5
            self.undo(board, t)
        return win


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
        move = mct.get_action(20)
        self.board.make_move(move,self.color)
        return move
