# from random import randint
# from BoardClasses import Move
# from BoardClasses import Board
# import math
# import copy
# import time
#
# class Node():
#     def __init__(self, board, parent, turn):
#         self.board = copy.deepcopy(board)
#         self.parent = parent
#         self.win = 0
#         self.visit = 0
#         self.turn = turn
#
#
#     def ucb(self, c):
#         return self.win/self.visit + c*math.sqrt(math.log(self.parent.visit)/self.visit)
#
#
# class MonteCarloTree():
#     def __init__(self, board, moves, color, opponent):
#         self.board = board
#         self.moves = moves
#         self.color = color
#         self.opponent = opponent
#         self.root = Node(board, None, self.color)
#         self.states = {str(self.board.board): self.root} # {board: node}
#
#     def get_action(self, simulate_time):
#         # curr_move = self.select(self.root, self.color)
#
#         start_time = time.time()
#         while time.time() - start_time < simulate_time:
#             select_node = self.select(self.root, self.root.turn)
#             w = self.simulate(select_node.board, select_node.turn)
#             self.backpropagate(select_node, w)
#
#         # select the best child
#         best_move = self.select(self.root, self.color).move
#
#         return best_move
#
#
#
#     # random roll a move
#     def rollout(self, moves):
#         index = randint(0,len(moves)-1)
#         inner_index = randint(0,len(moves[index])-1)
#         move = moves[index][inner_index]
#         return move
#
#
#
#     def best_child(self, children):
#         best_ucb = 0
#         best_node = None
#         for child in children:
#             ucb = child.ucb(1.4)
#             if ucb > best_ucb:
#                 best_ucb = ucb
#                 best_node = child
#         return best_node
#
#
#     def select(self, node, turn):
#         board = node.board
#         moves = board.get_all_possible_moves(turn)
#
#         # explore all possible children
#         children = []
#         for chess in moves:
#             for move in chess:
#                 board.make_move(move, turn)
#
#                 # if we have seen this board
#                 if str(board.board)+str(turn) in self.states:
#                     children.append(self.states[str(board.board)+str(turn)])
#                     board.undo()
#                     continue
#
#                 # else we expand and simulate
#                 child = Node(board, node, turn)
#                 child.move = move  # get the board with which move
#                 children.append(child)
#                 self.states[str(board.board)+str(turn)] = child
#
#                 win = self.simulate(board, turn)
#                 child.win = win
#                 child.visit = 1
#                 self.backpropagate(child, win)
#
#                 board.undo()
#
#         return self.best_child(children)
#
#
#     # # not sure about how to implement it yet...
#     # def expand(self):
#     #     board = self.board
#     #     t = 0
#     #     curr_node = self.get_node(board)
#     #     while curr_node:
#     #         moves = board.get_all_possible_moves(self.color)
#     #         move = self.rollout(moves)
#     #         board.make_move(move, self.color)
#     #         t += 1
#     #
#     #         moves = board.get_all_possible_moves(self.opponent[self.color])
#     #         move = self.rollout(moves)
#     #         board.make_move(move, self.opponent[self.color])
#     #         t += 1
#     #
#     #         curr_node = self.get_node(board)
#     #
#     #     # now curr_node is unexplored
#     #     curr_node = Node(board)
#     #
#     #     self.undo(board, t)
#
#
#     # simulate the game with a start move
#     def simulate(self, board, color):
#         win = 0
#         curr_turn = self.opponent[color]
#         t = 0
#         for turn in range(50):
#             if board.is_win(color) == color:
#                 win = 1
#                 self.undo(board,t)
#                 break
#             elif board.is_win(self.opponent[color]) == self.opponent[color]:
#                 self.undo(board, t)
#                 break
#             move = self.rollout(board.get_all_possible_moves(curr_turn))
#             board.make_move(move, curr_turn)
#             curr_turn = self.opponent[curr_turn]
#             t += 1
#         else:
#             win += 0
#             self.undo(board, t)
#         return win
#
#
#     def backpropagate(self, node, win):
#         if not node.parent:
#             return
#         node.parent.win += win
#         node.parent.visit += 1
#         self.backpropagate(node.parent, win)
#
#
#     def undo(self, board, times):
#         for _ in range(times):
#             board.undo()
#
#
#
# #The following part should be completed by students.
# #Students can modify anything except the class name and exisiting functions and varibles.
# class StudentAI():
#
#     def __init__(self,col,row,p):
#         self.col = col
#         self.row = row
#         self.p = p
#         self.board = Board(col,row,p)
#         self.board.initialize_game()
#         self.color = ''
#         self.opponent = {1:2,2:1}
#         self.color = 2
#     def get_move(self,move):
#         if len(move) != 0:
#             self.board.make_move(move,self.opponent[self.color])
#         else:
#             self.color = 1
#         moves = self.board.get_all_possible_moves(self.color)
#         # index = randint(0,len(moves)-1)
#         # inner_index =  randint(0,len(moves[index])-1)
#         # move = moves[index][inner_index]
#         mct = MonteCarloTree(self.board, moves, self.color, self.opponent)
#         move = mct.get_action(10)
#         self.board.make_move(move, self.color)
#         return move
