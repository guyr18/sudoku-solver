from StartScreen import StartScreen

class Screens:
    def __init__(self, data):
        self.data = data
        self.inherited = {"difficulty": "-n"}
        self.START = StartScreen("Sudoku Solver", (1080, 720), data["paths"], data["colors"])
        self.START.setUtil(self)
        self.GRID = None
