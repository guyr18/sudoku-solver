from pygame.surface import Surface
from pygame import font
from TextButton import TextButton
from IconButton import IconButton
from CellUI import CellUI
import pygame, os, pygame.gfxdraw

class Renderer:
    def __init__(self, size, colors, codes, board, dispatcher):
        self.WIDTH = size[0]
        self.HEIGHT = size[1]
        self.colors = dict()
        self.paths = ["/sudoku-solver/images/bgs/grid.png", "/sudoku-solver/images/icons/refresh.png"]
        self.firstTime = True
        self.cellTextLocations = dict()
        self.selectedCell = None
        self.selectionsMade = 0
        self.cellToProcess = None
        self.fixedCellClicked = False
        self.storedKey = -1
        self.makableSelections = -1

        for a in range(dispatcher.rows):
            for b in range(dispatcher.cols):
                if dispatcher.board[a][b].val == 0:
                    self.makableSelections += 1

        for k in range(len(self.paths)):
            self.paths[k] = os.getcwd() + self.paths[k]

        for i in range(len(colors)):
            self.colors[colors[i][0]] = colors[i][1:4]
        self.sprites = []
        self.codes = dict()

        for j in range(len(codes)):
            self.codes[codes[j][0]] = codes[j][1]
        self.actionCode = self.codes["IDLE"]
        self.dispatcher = dispatcher

    """
    PlotHeaderShape(target) plots a common header shape used for this application as a filled polygon.
    """
    def plotHeaderShape(self, target):

        pt1 = (220, 100)
        pt2 = (230, 60)
        pt3 = (859, 60)
        pt4 = (859, 100)
        pygame.gfxdraw.filled_polygon(target.parent, (pt1, pt2, pt3, pt4), self.colors["BLUE"])

    """
    Render() draws all neccessary components to the screen as needed.
    """
    def render(self):

        paddingX = 640 // 9
        paddingY = 480 // 9

        if self.firstTime == True:

            # Initialize screen
            screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

            # Change background
            bg = pygame.image.load(self.paths[0])
            screen.blit(bg, (0, 0))
    
            # Draw grid outline
            gridSurface = Surface((640, 480))
            gridSurface.fill(self.colors["WHITE"])
            pygame.draw.rect(gridSurface, self.colors["LIGHTBLUE"], (0, 0, 640, 480), 2)

            # Draw each row
            for i in range(self.dispatcher.rows):
                yOffset = (i + 1) * paddingY
                pygame.draw.line(gridSurface, self.colors["LIGHTBLUE"], (0, yOffset), (640, yOffset), 2)

            # Draw each column
            for j in range(self.dispatcher.cols):
                xOffset = (j + 1) * paddingX
                pygame.draw.line(gridSurface, self.colors["LIGHTBLUE"], (xOffset, 0), (xOffset, 640), 2)

            # Blit screen; copy pixels
            screen.blit(gridSurface, (220, 100))
            self.screen = screen

            # Draw numbers in each cell
            for m in range(self.dispatcher.rows):
                for n in range(self.dispatcher.cols):
                    item = self.dispatcher.board[m][n].val
                    cond = item > -1 if self.actionCode == self.codes["ACTION_SOLVE"] else item != 0
                    xOffset = (n + 1) * (paddingX) + 175
                    yOffset = (m + 1) * (paddingY) + 55
                    sTemp = str(m) + str(n)
                    if sTemp not in self.cellTextLocations:
                        block = CellUI(0, screen, (xOffset - 24, yOffset - 6), (69, 51), self.colors["WHITE"], self.colors["GRAY"])
                        block.fixed = self.dispatcher.board[m][n].fixed
                        block.row = m
                        block.col = n
                        block.draw()
                        self.cellTextLocations[sTemp] = block
                    if cond:
                        fontObj = font.SysFont('segoeui', 30)
                        textField = fontObj.render(str(item), True, self.colors["BLACK"])
                        screen.blit(textField, (xOffset, yOffset))
            
        screen = self.screen
        # Buttons
        # Have logic to draw back button when solved; no screen so wait to implement
        refreshFillColor = self.colors["BLUE"] if self.selectionsMade > 0 else self.colors["GRAY_SHADE"]
        refreshBorderColor = self.colors["DARKBLUE"] if self.selectionsMade > 0 else self.colors["BORDER_GRAY"]
        solveFillColor = self.colors["GRAY_SHADE"] if self.actionCode == self.codes["ACTION_DISABLE_ALL"] or self.selectionsMade == self.makableSelections else self.colors["BLUE"]
        solveBorderColor = self.colors["DARKBLUE"] if self.actionCode != self.codes["ACTION_DISABLE_ALL"] or self.selectionsMade < self.makableSelections else self.colors["BORDER_GRAY"]
        solveButton = TextButton(0, "Solve", self.colors["WHITE"], 'segoeui', 25, screen, (460, 620), (150, 50), solveBorderColor, 1, solveFillColor, (-17, 5))
        refreshButton = IconButton(1, self.paths[1], screen, (1010, 10), (60, 53), refreshBorderColor, 2, refreshFillColor, (-5, -8))
        stepText = TextButton(3, "No activity. Solve the puzzle!", self.colors["WHITE"], 'segoeui', 18, screen, (220, 35), (0, 0), self.colors["LIGHTBLUE"], 2, self.colors["WHITE"], (-30, 32))
        temp = [solveButton, stepText, refreshButton]

        for btn in temp:   
            if btn.id == 3:
                btn.text = btn.text if self.actionCode != self.codes["ACTION_DISABLE_ALL"] else "Sudoku puzzle solved!" 
                btn.draw(useCustomShape=True, plotFunc=self.plotHeaderShape(btn))
                self.sprites.append(btn)
                continue
            btn.draw()
            if btn not in self.sprites:
                self.sprites.append(btn)

        if self.actionCode == self.codes["ACTION_SOLVE"]:
            for key in self.cellTextLocations:
                row = int(key[0])
                col = int(key[1])

                if self.dispatcher.board[row][col].fixed == True:
                    continue
                obj = self.cellTextLocations[key]
                posTuple = obj.pos
                sizeTuple = obj.size
                answer = self.dispatcher.board[row][col].val
                greenSurface = Surface(sizeTuple)
                greenSurface.fill(self.colors["GREEN"])
                greenFontObj = font.SysFont('segoeui', 40)
                resTF = greenFontObj.render(str(answer), True, self.colors["WHITE"])
                screen.blit(greenSurface, posTuple)
                screen.blit(resTF, (posTuple[0] + 25, posTuple[1] - 5))

        elif self.actionCode == self.codes["ACTION_REFRESH"]:
            for key in self.cellTextLocations:
                row = int(key[0])
                col = int(key[1])
                if self.dispatcher.board[row][col].fixed == True:
                    continue
                obj = self.cellTextLocations[key]
                pos = obj.pos
                size = obj.size
                whiteSurface = Surface(size)
                whiteSurface.fill(self.colors["WHITE"])
                screen.blit(whiteSurface, (pos[0], pos[1]))
                for r in range(self.dispatcher.rows):
                    for s in range(self.dispatcher.cols):
                        if self.dispatcher.board[r][s].fixed == False:
                            self.dispatcher.board[r][s].updateValue(0)

                if self.selectedCell != None:
                    self.selectedCell.selected = False
                    self.selectedCell.draw()
                    self.selectedCell = None
                    self.actionCode = self.codes["IDLE"]

        elif self.actionCode == self.codes["ACTION_SELECT"]:
            btn = [b for b in self.sprites if b.id == 3]
            sameCellClick = False
            if self.fixedCellClicked == True:
                btn[0].text = "Preset cell(s) cannot be selected!"
                self.fixedCellClicked = False
                if self.selectedCell != None:
                    self.selectedCell.toggleSelect()
                    self.selectedCell.draw()
                    self.selectedCell = None
            elif self.selectedCell == self.cellToProcess and self.selectedCell.success == False:
                btn[0].text = "Cell already selected! Select another cell if you would like to change it."
                sameCellClick = True
            else:
              row = self.cellToProcess.row + 1
              col = self.cellToProcess.col + 1
              btn[0].text = "Cell selected on row " + str(row) + ", column " + str(col)
              self.cellToProcess.toggleSelect()
              self.cellToProcess.draw()
              
            # Prevent multiple cells from being selected.
            if self.selectedCell != None and sameCellClick == False:
                self.selectedCell.toggleSelect()
                if self.selectedCell.success == False:
                    self.selectedCell.draw()
                else:
                    self.dispatcher.board[self.selectedCell.row][self.selectedCell.col].updateValue(0)
                    
            btn[0].draw(useCustomShape=True, plotFunc=self.plotHeaderShape(btn[0]))
            self.selectedCell = self.cellToProcess
            self.cellToProcess = None
            self.actionCode = self.codes["IDLE"]

        elif self.actionCode == self.codes["ACTION_KEYPRESS"]:
            btn = [b for b in self.sprites if b.id == 3]
            offset = self.storedKey - 48
            row = self.selectedCell.row + 1
            col = self.selectedCell.col + 1
            btn[0].text = "Value " + str(offset) + " failed on row " + str(row) + ", column " + str(col)
            obj = self.cellTextLocations[str(row - 1) + str(col - 1)]
            pos = obj.pos
            kpFont = font.SysFont('segoeui', 40)
            higherSurface = Surface(obj.size)
            fillToUse = self.colors["GRAY"]
            textToUse = self.colors["RED"]
            bSuccess = False
            if self.dispatcher.validateAttempt(row - 1, col - 1, offset)[0] == True:
                self.selectionsMade += 1
                self.selectedCell.success = True
                self.selectedCell.toggleSelect()
                bSuccess = True
                fillToUse = self.colors["GREEN"]
                textToUse = self.colors["WHITE"]
                self.dispatcher.board[row - 1][col - 1].updateValue(offset)
                self.actionCode = self.codes["IDLE"]
            else:
                self.selectedCell.success = False
            higherSurface.fill(fillToUse)
            kpRender = kpFont.render(str(offset), True, textToUse)
            screen.blit(higherSurface, pos)
            screen.blit(kpRender, (pos[0] + 25, pos[1] - 5))
            btn[0].text = btn[0].text if bSuccess == False else "Value " + str(offset) + " was successfully inserted on row " + str(row) + ", column " + str(col)
            btn[0].draw(useCustomShape=True, plotFunc=self.plotHeaderShape(btn[0]))

            if self.selectionsMade >= self.makableSelections:
                self.actionCode = self.codes["ACTION_DISABLE_ALL"]
                self.render()

        # Update display
        pygame.display.update()

    """
    Run(title) manages an infinite loop throughout the lifetime of the application. The objective
    of this method is render all new visual additions to the screen and update properties accordingly.
    """
    def run(self, title):
        running = True
        pygame.display.set_caption(title)
        pygame.init()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                # If a mouse click occurred..
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mousePos = pygame.mouse.get_pos()
                    btns = [s for s in self.sprites if s.intersects(mousePos)] 
                    if len(btns) > 0:

                        # Solve button
                        if btns[0].id == 0 and self.actionCode != self.codes["ACTION_DISABLE_ALL"]:
                            self.actionCode = self.codes["ACTION_SOLVE"]
                            self.selectionsMade = self.dispatcher.rows * self.dispatcher.cols

                        if btns[0].id == 1:
                            self.actionCode = self.codes["ACTION_REFRESH"]
                            self.selectionsMade = 0
                       
                    temp = [self.cellTextLocations[key] for key in self.cellTextLocations if self.cellTextLocations[key].intersects(mousePos)]

                    # Did we click a cell? If so, apply a color for distinction purposes.
                    if len(temp) > 0:
                        if temp[0].fixed == True:
                            self.fixedCellClicked = True
                        else:
                            self.cellToProcess = temp[0]
                        self.actionCode = self.codes["ACTION_SELECT"]

                elif event.type == pygame.KEYDOWN and event.key >= 49 and event.key <= 57 and self.selectedCell != None:
                        self.actionCode = self.codes["ACTION_KEYPRESS"]
                        self.storedKey = event.key

            # We provide a guard so infinite renders aren't occurring, putting tremendous stress on
            # CPU and ultimately causing lag as function stack is overwhelmed..
            if (self.actionCode != self.codes["IDLE"] and self.actionCode != self.codes["ACTION_DISABLE_ALL"]) or self.firstTime == True:
                self.dispatcher.dispatch(self)
                self.render()
            self.firstTime = False if self.firstTime == True else False


    """
    UpdateBoard(newBoard) is a mutator function that mutates the current board to parameter, 'newBoard'.
    """
    def updateBoard(self, newBoard):
        self.board = newBoard
