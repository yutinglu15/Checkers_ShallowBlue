from random import randint
from BoardClasses import Move
from BoardClasses import Board
import math
import copy
import random
import numpy as np
import random

#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.

class QLearning():
    def __init__(self):
        self.epsilon = 0.2
        self.lr = 0.05
        self.gamma = 0.1

        self.state_size = 0
        self.action_size = 0
        self.color = ''

        # TODO: considering changing Q input to other things
        self.Q = np.zeros((self.state_size, self.action_size))
        self.Q_table = {}

    def make_action(self,state):
        # TODO: implement this
        for a in get_all_action(state):
            return action with max(self.Q_table[state, action])



    def explore(self, state):
        epsilon = 0.2
        if random.uniform(0,1) < epsilon:
            # TODO : implement select random move
        else:
            # TODO: implement explore max reward

        pass

    def train(self, epoch):
        for _ in epoch:
            self.train_one_episode()
            # TODO: kind of visualize the learning result here
            print("in epoch ", _, "learning performance")


    def train_one_episode(self):
        new_board = Board()
        new_board.initialize_game()
        turn = ''

        while True:
            if new_board.is_win(self.color):
                break
            elif new_board.is_win(self.opponent[self.color]):
                break

            action = self.explore(new_board, self.color)
            state = new_board
            new_state = new_board.make_move(action, turn)
            self.Q_table[state, action] = self.Q_table[state, action] + self.lr * \
                                          (self.reward(state, action) + self.gamma * np.max(self.Q_tableQ[new_state, :])\
                                           - self.Q_table[state, action])
            state = new_state


    def reward(self, state, action):
        bking, wking = 0, 0
        for r in range(self.board.row):
            for c in range(self.board.col):
                if self.board.board[r][c].color == "B":
                    bking += self.board.board[r][c].is_king
                elif self.board.board[r][c].color == "W":
                    wking += self.board.board[r][c].is_king


        b = 3*self.board.black_count + bking
        w = 3*self.board.white_count + wking

        # TODO: implement punishment with a tie

        return b-w if self.color == 1 else w-b

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

    def get_move(self, move):
        #print(self.color)
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)

        #self.train()
        self.simulate_lr(self.color)

        #index = randint(0,len(moves)-1)
        #inner_index =  randint(0,len(moves[index])-1)
        #move = moves[index][inner_index]
        #print(moves)
        ql = QLearning()
        move = ql.make_action(self.board, moves)
        #move = self.monte_carlo_tree([m for chess in moves for m in chess], 10, 10)
        self.board.make_move(move, self.color)
        self.movecount += 1
        return move