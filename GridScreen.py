from Screen import Screen
from CellUI import CellUI
from TextButton import TextButton
from IconButton import IconButton
from BoardGenerator import BoardGenerator
from pygame.font import SysFont
from pygame.surface import Surface
import pygame, pygame.gfxdraw

class GridScreen(Screen):
    def __init__(self, size, paths, colors, codes, display):
        super().__init__("Grid", size)
        self.display = display
        self.paths = paths
        self.colors = colors
        self.codes = codes
        self.colors = colors
        self.cellTextLocations = dict()
        self.selectedCell = None
        self.selectionsMade = 0
        self.cellToProcess = None
        self.fixedCellClicked = False
        self.storedKey = -1
        self.makableSelections = -1
        self.actionCode = self.codes["IDLE"]
        self.paddingX = 640 // 9
        self.paddingY = 480 // 9

    def init(self):

        # Generate a board from difficulty selected on start screen and cache that information.
        gen = BoardGenerator()
        print(self.util.inherited["difficulty"])
        board, dispatcher = gen.generate(n=9, difficulty=self.util.inherited["difficulty"])
        self.dispatcher = dispatcher
        self.board = board

        # Compute the number of empty cells there are at the start.
        for a in range(self.dispatcher.rows):
            for b in range(self.dispatcher.cols):
                if self.dispatcher.board[a][b].val == 0:
                    self.makableSelections += 1

    """
    UpdateBoard(newBoard) is a mutator function that mutates the current board to parameter, 'newBoard'.
    """
    def updateBoard(self, newBoard):
        self.board = newBoard
        
    """
    PlotHeaderShape(target) plots a common header shape used for this application as a filled polygon.
    """
    def plotHeaderShape(self, target):

        pt1 = (220, 100)
        pt2 = (230, 60)
        pt3 = (859, 60)
        pt4 = (859, 100)
        pygame.gfxdraw.filled_polygon(target.parent, (pt1, pt2, pt3, pt4), self.colors["BLUE"])

    def draw(self):

        # Change background
        bg = pygame.image.load(self.paths[0])
        self.display.blit(bg, (0, 0))
    
        # Draw grid outline
        gridSurface = Surface((640, 480))
        gridSurface.fill(self.colors["WHITE"])
        pygame.draw.rect(gridSurface, self.colors["LIGHTBLUE"], (0, 0, 640, 480), 2)

        # Draw each row
        for i in range(self.dispatcher.rows):
            yOffset = (i + 1) * self.paddingY
            pygame.draw.line(gridSurface, self.colors["LIGHTBLUE"], (0, yOffset), (640, yOffset), 2)

        # Draw each column
        for j in range(self.dispatcher.cols):
            xOffset = (j + 1) * self.paddingX
            pygame.draw.line(gridSurface, self.colors["LIGHTBLUE"], (xOffset, 0), (xOffset, 640), 2)

        # Blit screen; copy pixels
        self.display.blit(gridSurface, (220, 100))

        # Draw numbers in each cell
        for m in range(self.dispatcher.rows):
            for n in range(self.dispatcher.cols):
                item = self.dispatcher.board[m][n].val
                xOffset = (n + 1) * (self.paddingX) + 175
                yOffset = (m + 1) * (self.paddingY) + 55
                sTemp = str(m) + str(n)
                if sTemp not in self.cellTextLocations:
                    block = CellUI(0, self.display, (xOffset - 24, yOffset - 6), (69, 51), self.colors["WHITE"], self.colors["GRAY"])
                    block.fixed = self.dispatcher.board[m][n].fixed
                    block.row = m
                    block.col = n
                    block.draw()
                    self.cellTextLocations[sTemp] = block
                if item > 0:
                    fontObj = SysFont('segoeui', 30)
                    textField = fontObj.render(str(item), True, self.colors["BLACK"])
                    self.display.blit(textField, (xOffset, yOffset))

        solveButton = TextButton(0, "Solve", self.colors["WHITE"], 'segoeui', 25, self.display, (460, 620), (150, 50), self.colors["BLUE"], 1, self.colors["BLUE"], (-17, 5))
        refreshButton = IconButton(1, self.paths[1], self.display, (1010, 10), (60, 53), self.colors["LIGHT_GRAY"], 2, self.colors["LIGHT_GRAY"], (-5, -8))
        backButton = IconButton(2, self.paths[3], self.display, (10, 10), (60, 53), self.colors["LIGHT_GRAY"], 2, self.colors["LIGHT_GRAY"], (-40, -25))
        stepText = TextButton(3, "No activity. Solve the puzzle!", self.colors["WHITE"], 'segoeui', 18, self.display, (220, 35), (0, 0), self.colors["LIGHTBLUE"], 2, self.colors["WHITE"], (-30, 32))
        self.sprites = [solveButton, stepText, refreshButton, backButton]

        for sprite in self.sprites:   
            if sprite.id == 3:
                sprite.draw(useCustomShape=True, plotFunc=self.plotHeaderShape(sprite))
                continue
            sprite.draw()

        pygame.display.update()

    def handle_event(self):
        running = True
        self.draw()

        while running == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                # If a mouse click occurred..
                if event.type == pygame.MOUSEBUTTONDOWN and self.disabled == False:
                    mousePos = pygame.mouse.get_pos()
                    btns = [s for s in self.sprites if s.intersects(mousePos)] 
                    if len(btns) > 0:

                        # Solve button
                        if btns[0].id == 0 and self.actionCode != self.codes["ACTION_DISABLE_ALL"]:
                            print("Solve button clicked")
                            self.actionCode = self.codes["ACTION_SOLVE"]
                            self.selectionsMade = self.makableSelections
                            self.update()

                        # Refresh button
                        if btns[0].id == 1 and self.selectionsMade > 0:
                            self.actionCode = self.codes["ACTION_REFRESH"]
                            self.selectionsMade = 0
                            self.update()

                        # Back button
                        if btns[0].id == 2 and self.selectionsMade >= self.makableSelections:
                            self.util.START.disabled = False
                            self.disabled = True
                            self.switchScreen("Start")
                            running = False

                    temp = [self.cellTextLocations[key] for key in self.cellTextLocations if self.cellTextLocations[key].intersects(mousePos)]

                    # Did we click a cell? If so, apply a color for distinction purposes.
                    if len(temp) > 0 and self.disabled == False:
                        if temp[0].fixed == True:
                            self.fixedCellClicked = True
                        else:
                            self.cellToProcess = temp[0]
                            self.actionCode = self.codes["ACTION_SELECT"]
                        self.update()

                elif event.type == pygame.KEYDOWN and event.key >= 49 and event.key <= 57 and self.selectedCell != None and self.disabled == False:
                    self.actionCode = self.codes["ACTION_KEYPRESS"]
                    self.storedKey = event.key
                    self.update()
                    
    def update(self):
         # Buttons
        backButtonColor = self.colors["RED"] if self.selectionsMade >= self.makableSelections else self.colors["LIGHT_GRAY"]
        backButton = IconButton(2, self.paths[3], self.display, (10, 10), (60, 53), backButtonColor, 2, backButtonColor, (-40, -25))
        refreshFillColor = self.colors["BLUE"] if self.selectionsMade > 0 else self.colors["LIGHT_GRAY"]
        refreshBorderColor = self.colors["BLUE"] if self.selectionsMade > 0 else self.colors["LIGHT_GRAY"]
        solveFillColor = self.colors["LIGHT_GRAY"] if self.actionCode == self.codes["ACTION_DISABLE_ALL"] or self.selectionsMade == self.makableSelections else self.colors["BLUE"]
        solveBorderColor = self.colors["DARKBLUE"] if self.actionCode != self.codes["ACTION_DISABLE_ALL"] or self.selectionsMade < self.makableSelections else self.colors["LIGHT_GRAY"]
        solveButton = TextButton(0, "Solve", self.colors["WHITE"], 'segoeui', 25, self.display, (460, 620), (150, 50), solveBorderColor, 1, solveFillColor, (-17, 5))
        refreshButton = IconButton(1, self.paths[1], self.display, (1010, 10), (60, 53), refreshBorderColor, 2, refreshFillColor, (-5, -8))
        stepText = TextButton(3, "No activity. Solve the puzzle!", self.colors["WHITE"], 'segoeui', 18, self.display, (220, 35), (0, 0), self.colors["LIGHTBLUE"], 2, self.colors["WHITE"], (-30, 32))
        self.sprites = [solveButton, stepText, refreshButton, backButton]

        for sprite in self.sprites:  
            if sprite.id == 3:
                sprite.text = sprite.text if self.actionCode != self.codes["ACTION_DISABLE_ALL"] else "Sudoku puzzle solved!" 
                sprite.draw(useCustomShape=True, plotFunc=self.plotHeaderShape(sprite))
                continue
            sprite.draw()

        if self.actionCode == self.codes["ACTION_SOLVE"]:
            for key in self.cellTextLocations:
                row = int(key[0])
                col = int(key[1])

                if self.board[row][col].fixed == True:
                    continue
                obj = self.cellTextLocations[key]
                posTuple = obj.pos
                sizeTuple = obj.size
                answer = self.board[row][col].val
                greenSurface = Surface(sizeTuple)
                greenSurface.fill(self.colors["GREEN"])
                greenFontObj = SysFont('segoeui', 40)
                resTF = greenFontObj.render(str(answer), True, self.colors["WHITE"])
                self.display.blit(greenSurface, posTuple)
                self.display.blit(resTF, (posTuple[0] + 25, posTuple[1] - 5))

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
                self.display.blit(whiteSurface, (pos[0], pos[1]))
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
            kpFont = SysFont('segoeui', 40)
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
            self.display.blit(higherSurface, pos)
            self.display.blit(kpRender, (pos[0] + 25, pos[1] - 5))
            btn[0].text = btn[0].text if bSuccess == False else "Value " + str(offset) + " was successfully inserted on row " + str(row) + ", column " + str(col)
            btn[0].draw(useCustomShape=True, plotFunc=self.plotHeaderShape(btn[0]))

            if self.selectionsMade >= self.makableSelections:
                self.actionCode = self.codes["ACTION_DISABLE_ALL"]
                self.update()

        # Update display
        pygame.display.update()
