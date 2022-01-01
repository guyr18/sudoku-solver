from copy import copy, deepcopy
from random import randint
import random
from Dispatcher import Dispatcher
from Cell import Cell

class BoardGenerator:
    def __init__(self):
        self.curFixedCells = 0
        self.DIFF_EASY = "-e"
        self.DIFF_NORMAL = "-n"
        self.DIFF_HARD = "-h"
        self.minsCellPerDiff = {self.DIFF_EASY: 51, self.DIFF_NORMAL: 34, self.DIFF_HARD: 17}

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
    GetRandomCellPositions(minCells, n) returns a list of random 2D positions as tuples. The cardinality of this
    list is equivalent to parameter minCells. Each position is unique.
    """

    def getRandomCellPositions(self, minCells, n):
        count = 0
        data = {}

        # Loop from 0 to minCells.
        while count < minCells:

            # Get random integer for row position.
            row = randint(0, n - 1)

            # Get random integer for column position.
            col = randint(0, n - 1)

            # Build key string.
            temp = str(row) + "-" + str(col)

            # Check if it is in our Dictionary object, if it is not make a key for it
            # and increment count.
            if temp not in data:
                data[temp] = (row, col)
                count += 1

        # Convert each key into a valid tuple association and append it into a new list.
        # Then return it.
        record = []
        for key in data:
            dataAsTuple = (int(key[0]), int(key[2]))
            record.append(dataAsTuple)
        return record

    def generate(self, n, difficulty=None):

        # Create a 2D array of zeroes that has dimensions n x n.
        solved = [[0] * n for _ in range(n)]

        # Using set comprehension, we create a list of values
        # from 1 to 9. Then, we shuffle them by type-casting to
        # a list object.
        validNumbers = list({x for x in range(1, n + 1)})
        random.shuffle(validNumbers)

        # We iterate through the shuffled values and assign each to a cell
        # within the first row.
        for i in range(n):
            solved[0][i] = validNumbers[i]

        # Shift the values in each row, in a [3, 3, 1, 3, 3, 1, 3, 3] pattern.
        for row in range(1, n):
            numShift = 1 if row % 3 == 0 else 3
            start = 0

            while start < n:
                solved[row][start] = solved[row - 1][start - numShift]
                start += 1

        # Convert each value to a corresponding Cell instance that the Dispatcher
        # object can work with.
        self.cellulize(solved, n)
        cloneSolved = deepcopy(solved)

        # Associate it with a Dispatcher object and return the result and dispatcher.
        dispatcher = Dispatcher(cloneSolved)

        # Compute the number of cells we need to remove.
        difficultyKey = self.DIFF_NORMAL if difficulty == None else difficulty
        minCells = (n ** 2) - self.minsCellPerDiff[difficultyKey]

        # Obtain a random list of cells.
        randomCells = self.getRandomCellPositions(minCells, n)
        start = 0
        copyDispatcher = Dispatcher(deepcopy(cloneSolved))

        # Loop from 0 to minCells.
        while start < minCells:

            # We maintain two Dispatcher objects: The copy dispatcher allows us to check if
            # there exists a solution, but when we do this check, internally we attempt
            # to find a solution and update the board. By maintaining two, we can revert
            # back to the previoius state when needed. Additionally, we skip this position
            # and go to the next as we couldn't use it.
            if copyDispatcher.solve() == False:
                copyDispatcher.board = dispatcher.board
                copyDispatcher.board[row][col].fixed = True
                dispatcher.board[row][col].fixed = True
                solved[row][col].fixed = True
                start += 1
                continue

            # This block implies that our solution is currently valid. We pick the
            # coordinates at the current start index and update that position to
            # a value of zero. 
            row = randomCells[start][0]
            col = randomCells[start][1]
            dispatcher.board[row][col].val = 0
            dispatcher.board[row][col].fixed = False
            copyDispatcher.board[row][col].val = 0
            copyDispatcher.board[row][col].fixed = False
            solved[row][col].fixed = False
            start += 1
        
        return solved, dispatcher
            


        




