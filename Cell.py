class Cell:
    def __init__(self, row, col, val, fixed):
        self.row = row
        self.col = col
        self.val = val
        self.fixed = fixed

    """
    UpdateValue(val) is a mutator function that modifies the value that is
    assigned to this cell.
    """
    def updateValue(self, val):
        self.val = val
