from Renderer import Renderer
from Dispatcher import Dispatcher
from Cell import Cell
from copy import deepcopy

board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

"""
DeepCopyBoard(board) takes in a 2D sudoku board array and converts it into a
new copy. It will return this copy.
"""
def deepCopyBoard(board):
    return deepcopy(board)

"""
Cellulize(board) takes a 2D array of integers as input, and converts
them into the corresponding Cell instance.
"""
def cellulize(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            isFixed = board[i][j] != 0
            board[i][j] = Cell(i, j, board[i][j], isFixed)
        
cellulize(board)
solvedBoardCache = []
objDispatcher = Dispatcher(deepCopyBoard(board))
colors = [("DARKRED", 162, 0, 0), ("DARKBLUE", 0, 100, 185), ("BORDER_GRAY", 100, 100, 100), ("GRAY_SHADE", 170, 170, 170), ("GREEN", 0, 255, 0), ("BLACK", 0, 0, 0), ("WHITE", 255, 255, 255), ("GRAY", 230, 230, 230), ("BLUE", 0, 162, 237), ("LIGHTBLUE", 41, 187, 255), ("GREEN", 0, 255, 0), ("RED", 199, 62, 29), ("LIGHTRED", 255, 88, 85)]
codes = [("IDLE", -1), ("ACTION_SOLVE", 0), ("ACTION_REFRESH", 1), ("ACTION_DISABLE_ALL", 2), ("ACTION_SELECT", 3), ("ACTION_KEYPRESS", 4)]
objRenderer = Renderer((1080, 720), colors, codes, board, objDispatcher)
objRenderer.run("Sudoku Solver")
