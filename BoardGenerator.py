from copy import deepcopy
from random import randint
from Dispatcher import Dispatcher
from Cell import Cell

class BoardGenerator:
    def __init__(self):
        self.curFixedCells = 0
        self.DIFF_EASY = "-e"
        self.DIFF_NORMAL = "-n"
        self.DIFF_HARD = "-h"

    """
    GetDifficulties() returns a list of valid difficulty strings.
    """
    def getDifficulties(self):
        return [self.DIFF_EASY, self.DIFF_NORMAL, self.DIFF_HARD]

    """
    Cellulize(board) takes a 2D array of integers as input, and converts
    them into the corresponding Cell instance.
    """
    def cellulize(self, board, n):
        for i in range(n):
            for j in range(n):
                isFixed = board[i][j] != 0
                board[i][j] = Cell(i, j, board[i][j], isFixed)

    """
    Sync_dispatcher_and_board(dsp, board, x, y, z) ensures that the 2D board array and the
    2D board array that is associated with the relative Dispatcher object, 'dsp', are
    both in sync. 
    """
    def sync_dispatcher_and_board(self, dsp, board, x, y, z):
        board[x][y].fixed = True
        board[x][y].val = z
        dsp.board = board

    """
    FindValidNumber(start, end, row, col, dsp) finds a valid number between the interval => [start, end]
    on the specified row, 'row', and column 'col'. If such a number exists, we return it. Otherwise,
    we return -1.
    """
    def findValidNumber(self, start, end, row, col, dsp):
        for x in range(start, end + 1):
            success = dsp.validateAttempt(row, col, x)[0]
            if success == True:
                return x
        return -1

    """
    GetDifficultyStringAsInteger(d) returns a corresponding integer that can be map to each difficulty level.
    If an unknown difficulty, d, is provided, this algorithm assumes a normal difficulty.
    """
    def getDifficultyStringAsInteger(self, d):
        if d == self.DIFF_EASY:
            return 1
        elif d == self.DIFF_NORMAL:
            return 2
        elif d == self.DIFF_HARD:
            return 3
        else:
            return 2

    """
    Generate(n, difficulty) generates and returns a sudoku puzzle (2D array) of difficulty, 'difficulty'.
    If 'difficulty' is set to None, we assign it the 'DIFF_NORMAL' difficulty.
    """
    def generate(self, n, difficulty=None):
        result = []
        for i in range(n):
            result.append([])
            for j in range(n):
                result[i].append(0)
        self.cellulize(result, n)
        objDispatcher = Dispatcher(result)

        # Loop across each row
        for x in range(n):
            # Loop across each column
            for y in range(n):

                # Produce a random integer between two intervals: [0, intDiff] where
                # intDiff is the integer associated with the difficulty, d.
                # Harder difficulties get a larger value, thus making it less
                # likely that a random integer is equal to it. Subsequently, it
                # would be less likely that a cell is set as well.
                intDiff = self.getDifficultyStringAsInteger(difficulty)
                prob = randint(0, intDiff)
                if prob == intDiff:
                    r = self.findValidNumber(1, n, x, y, objDispatcher)
                    if r != -1:
                        self.curFixedCells += 1
                        self.sync_dispatcher_and_board(objDispatcher, result, x, y, r)

        # Check if this board is valid, if it isn't, generate a new one.
        if objDispatcher.solve() == False:
            print("Invalid board!")
            return self.generate(n, difficulty)
        else:
            print("Valid board!")
            solved = deepcopy(result)
            for a in range(n):
                for b in range(n):
                    if objDispatcher.board[a][b].fixed == False:
                        objDispatcher.board[a][b].val = 0
            return solved, objDispatcher


