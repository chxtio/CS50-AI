"""
Tic Tac Toe Player
"""

import math
import copy
import random

# Possible moves
X = "X"
O = "O"
EMPTY = None
count = 0


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    count_x = count_o = 0
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == X:
                count_x += 1
            elif board[r][c] == O:
                count_o += 1

    if count_x <= count_o:
        return X
    else:
        return O



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == None:
                actions.add((i,j))

    # print('actions: ', actions)

    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board_copy = copy.deepcopy(board)
    if action not in actions(board):
        raise Exception("Invalid move")
        print("Invalid move")
    else:
        board_copy[action[0]][action[1]] = player(board)
        # print('result action: ', action)

    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #    j
    # i [0,0 | 0,1 | 0,2]
    #   [1,0 | 1,1 | 1,2]
    #   [2,0 | 2,1 | 2,2]

    # Horizontal Rows
    for r in range(len(board)):
        if board[r] == [X, X, X]:
            return X
        if board[r] == [O, O, O]:
            return O
        # Vertical Rows
        c = r
        if board[0][c] == board[1][c] == board[2][c] == X:
            return X
        if board[0][c] == board[1][c] == board[2][c] == O:
            return O

    # Diagonal
    if board[0][0] == board[1][1] == board[2][2] == X:
        return X
    if board[0][0] == board[1][1] == board[2][2] == O:
        return O

    if board[2][0] == board[1][1] == board[0][2] == X:
        return X
    if board[2][0] == board[1][1] == board[0][2] == O:
        return O

    return None



def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True

    # Check if board is filled
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == None:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0

def maxVal(board, alpha, beta):
    if terminal(board):
        return utility(board)

    v = float('-inf')
    for action in actions(board):
        v = max(v, minVal(result(board, action), alpha, beta))
        if v >= beta:
            # Alpha beta pruning: Since we are at a MAX node, the MIN node above would never choose this node, which is already at least higher than the previous MAX node
            # Therefore, we can skip evaluating the remaining successors
            return v

    return v

def minVal(board, alpha, beta):
    if terminal(board):
        return utility(board)

    v = float('inf')
    for action in actions(board):
        v = min(v, maxVal(result(board, action), alpha, beta))
        if v <= alpha:
            # Alpha beta pruning: Since we are at a MIN node, the MAX node above would never choose this node, which is already at most lower than the previous MIN node
            # Therefore, we can skip evaluating the remaining successors
            return v

    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # Random move
    # choices = (actions(board))
    # action = list(choices)[random.randrange(len(choices))]
    # print('minimax action: ', action)

    if terminal(board):
        return None

    # Select middle square if possible
    if board[1][1] == EMPTY:
        return (1,1)

    optimal_action = None

    if player(board) == O:

        bestVal = float('inf')
        alpha, beta = float('-inf'), float('inf')

        for action in actions(board):
            val = maxVal(result(board, action), alpha, beta)
            if val < bestVal:
                bestVal = val
                optimal_action = action
            beta = min(beta, bestVal)
            # print('[alpha, beta]: [{},{}]'.format(alpha, beta))

    else:
        bestVal = float('-inf')
        alpha, beta = float('-inf'), float('inf')

        for action in actions(board):
            val = minVal(result(board, action), alpha, beta)
            print('val: ', val)
            if val > bestVal:
                bestVal = val
                optimal_action = action
            alpha = max(alpha, bestVal)

    return optimal_action
