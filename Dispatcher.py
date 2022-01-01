class Dispatcher:
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])

    """
    InclusivelyBetween(i, lower, upper) returns true if lower <= i <= upper.
    And false otherwise.
    """

    def inclusivelyBetween(self, i, lower, upper):
        return i >= lower and i <= upper

    """
    GetInitialEmptySlot() returns the location, (row, column), of the first empty slot on the 
    sudoku board.
    """
    def getInitialEmptySlot(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j].val == 0:
                    return (i, j)
        return (-1, -1)

    """
    GetInvalidationFlagString(flag) returns an expanded string for each
    invalidation flag. Invalidation flags are as follows:
        1. -r => For some attempt a on row i, there exists another value a
                 on row i.
        2. -c => For some attempt a on column j, there exists another a on
                 column j.
        3. -s => For some attempt a, there exists another value a within
                 the section that corresponds to the row - column pair (i, j). 

    These flags hold the sudoku correctness criteria; valid gameplay.
    """
    def getInvalidationFlagString(self, flag):
        if flag == "-r":
            return "row flag"
        elif flag =="-c":
            return "column flag"
        else:
            return "section flag"

    """
    ValidateAttempt(i, j, attempt) performs validation on an attempt, 'attempt', at the cell
    that is located on the ith row and jth column. It validates from standard sudoku board criteria.
    There are three conditions:

        1. The attempted value is unique to the ith row.
        2. The attempted value is unique to the jth column
        3. The attempted value is unique to the section that
           pertains to the ith row and jth column.

    """
    def validateAttempt(self, i, j, attempt):

        # Check if row is invalid, if it is we're done. All conditions must be met.
        for cell in self.board[i]:
            if cell.val == attempt:
                return (False, "-r", cell)
    
        # Check if column is valid
        for k in range(0, self.cols, 1):
            cell = self.board[k][j]
            if cell.val == attempt:
                return (False, "-c", cell)

        # To validate the section, we must first locate the section and populate it.
        start = 0 if self.inclusivelyBetween(i, 0, 2) else 3 if self.inclusivelyBetween(i, 3, 5) else 6
        end = 2 if self.inclusivelyBetween(j, 0, 2) else 5 if self.inclusivelyBetween(j, 3, 5) else 8
        offset = end - 2 
        section = [self.board[start][offset:end+1], self.board[start+1][offset:end+1], self.board[start+2][offset:end+1]]

        # Check if section is valid
        for m in range(len(section)):
            for n in range(len(section)):
                if section[m][n].val == attempt:
                    return (False, "-s", section[m][n])
        return (True, "", self.board[i][j])
      
    """
    Solve() attempts to solve the parameterized 2D array, 'board' that is associated
    with this Dispatcher instance. When successful, a true boolean value is returned.
    """

    def solve(self):
        emptySlot = self.getInitialEmptySlot()
        row = emptySlot[0]
        col = emptySlot[1]

        if emptySlot == (-1, -1):
            return True

        for i in range(1, self.cols + 1):
            validationData = self.validateAttempt(row, col, i)
            if validationData[0] == True:
                self.board[row][col].updateValue(i)

                if self.solve() == True:
                    return True

                self.board[row][col].updateValue(0)

        return False
   
    """
    PrintBoard() prints a textual representation of the current 2D board array that
    is associated with this Dispatcher instance.
    """
    def printBoard(self):
        for i in range(self.rows):
            if i % 3 == 0:
                print("---------------------")
            for j in range(self.cols):
                item = self.board[i][j]
                if j % 3 == 0 and j != 0 and j != self.cols - 1:
                    print("|", end="")
                print(str(item.val) + " ", end="")
                if j == self.cols - 1:
                    print("\n")