# Sudoku Solver
**Sudoku Solver** is an educational project with two goals:
  - Solving any valid Sudoku puzzle.
  - Dynamic generation of valid Sudoku puzzles.
  
# Running Sudoku Solver
In order to run **Sudoku Solver* you will need to install **Python 3.8** or higher on your local machine.
Secondly, you will need to install **PyGame** as it is the graphical dependency used for this project.
You can do so as follows:
```
pip install pygame
```

As a final recommendation, this application utilizes the **SegoeUI** font. If you do not have it installed on your machine
the text may not look as optimal in certain scenarios. The application will revert to the **Arial** font.
You may install it via the following link:

https://www.cufonfonts.com/font/segoe-ui-4

# Running Sudoku Solver
This application can be run by first cloning or downloading the project files, navigating to the "sudoku-solver" directory and running the "main.py"
file, such as:
```
cd sudoku-solver
python3 main.py
```

# Documentation

Aside from the graphical interface provided, there are two standard APIs that you may find useful for future projects. The **Sudoku Solver**
API allows you solve a valid Sudoku puzzle and generate one as well. First, I will discuss how to utilize the API for solving a puzzle.
Below is some sample code:

```python
from Dispatcher import Dispatcher
from BoardGenerator import BoardGenerator
board = [[ 3, 1, 6, 5, 7, 8, 4, 9, 2 ],
         [ 5, 2, 9, 1, 3, 4, 7, 6, 8 ],
         [ 4, 8, 7, 6, 2, 9, 5, 3, 1 ],
         [ 2, 6, 3, 0, 1, 5, 9, 8, 7 ],
         [ 9, 7, 4, 8, 6, 0, 1, 2, 5 ],
         [ 8, 5, 1, 7, 9, 2, 6, 4, 3 ],
         [ 1, 3, 8, 0, 4, 7, 2, 0, 6 ],
         [ 6, 9, 2, 3, 5, 1, 8, 7, 4 ],
         [ 7, 4, 5, 0, 8, 6, 3, 1, 0 ]
         ]
gen = BoardGenerator()
n = len(board)
board = gen.cellulize(board, n)
dispatcher = Dispatcher(board)
if dispatcher.solve() == True:
  dispatcher.printBoard()
else:
  print("No solution exists!")
```
First, we import the **Dispatcher** and **BoardGenerator** module(s) and declare a 2D array that represents a Sudoku board. Non-zero values 
represents the fixed cells, where zeroed values are cells that need to be solved by our algorithm. We instantiate a **BoardGenerator** object 
in order to use its .cellulize() method. This method will convert all board integers into corresponding **Cell** objects that our **Dispatcher** 
object can in turn work with. We declare a **Dispatcher** object and feed it the board as a parameter so it is accessible. The **Dispatcher** 
instance(s) .solve() method is then invoked. It will return true, if the board is successfully solved, and otherwise false. If it happens to 
be true, we call the .printBoard method to log a more user-friendly textual representation of the board to the console / terminal / command prompt.

Regarding the latter goal of dynamic puzzle generation, we may accomplish this as follows:
```python
from BoardGenerator import BoardGenerator
gen = BoardGenerator()
solved, dispatcher = gen.generate(n=9, difficulty=gen.DIFF_EASY)
```

We import the **BoardGenerator** module and then create a corresponding instance. Subsequently, we call the .generate() method with parameter n,
which is representative of the size of the Sudoku board (n x n = 9 x 9). The **BoardGenerator** object currently supports three levels of difficulties
which can also be retrieved using the BoardGenerator.getDifficulties() method. They are defined as constants within the module:

  - Easy => DIFF_EASY
  - Normal => DIFF_NORMAL
  - Hard => DIFF_HARD
  
The algorithm consists of several steps which I will attempt to explain:
  1) A set of the numbers 1-9 is generated and their locations are shuffled.
  2) The previous numbers are set as the first row of the puzzle.
  3) Each subsequent rows (1 -> n - 1) entries are shifted by the following number of values [3, 3, 1, 3, 3, 1, 3, 3].
  4) A Dictionary object is created for each difficulty level in which we specify the number of cells to be filled for each level.
     It can briefly be described as {DIFF_EASY: 51, DIFF_NORMAL: 34, DIFF_HARD: 17}.
  5) At this point, we have a completely valid Sudoku board and we need to decide what cells to erase such that can be challenging
     for a prospective user. The number of cells that we would maximally erase can be computed as: **y = (n * n) - x** where **x** is the
     value derived from the preceding Dictionary object.
  6) We invoke a function to build a list of **y** random positions as tuples in the form of **(row, col)**.
  7) Using these positions, we attempt to set each one to zero. Following each change, we use our **Dispatcher** to verify if there exists
     a valid solution for the puzzle at some state **z**. If no solution exists for state **z**, then we revert our change, and continue
     to the next position in the list. 

Step (3) is the computationally, most expensive step. It requires that all entries of the last n - 1 rows are shifted by either 1 or 3. 
Therefore, we must mutate the row in-place and this yields a precise time complexity of **O(n-1<sup>2</sup>)**. Following common reduction to lower
order terms we get **O(n<sup>2</sup>)**. In the case of Sudoku, this means we will always have a run-time complexity of **O(81)**; considering n = 9.

The .generate() method returns two values: The first is the solved, cellulized board and the second is the **Dispatcher** object associated with the
generation process. The .board property within the **Dispatcher** object represents the board in an unsolved state. It is present with zeroed values.

# How to Play
As previously mentioned, a graphical interface is provided to showcase what the before-mentioned APIs can do. Initially, the user brought to a Start screen
which is pretty self explanatory. When you click new board, a puzzle will be dynamically generated. The subsequent screen is referred to as the Grid screen.
Instructions for this screen are as follows:
   
   1) You can click any empty cell.
   2) It accepts digit 1-9 through a keypress. If the value you key is invalid (according to Sudoku criteria) it
      will turn red to indicate this. Conversely, a valid value changes the cell color to green. 
      
Some other options are the Solve button, Refresh button, and Back button. The solve button instanteously solves the puzzle. The refresh button will
reset the puzzle to its original state, and the Back button will return you to the Start screen. This will in turn allow you to generate a new
Sudoku board.
