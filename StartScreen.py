from typing import Text
from Screen import Screen
from TextButton import TextButton
from GridScreen import GridScreen
from pygame.surface import Surface
from pygame.font import SysFont
import pygame

class StartScreen(Screen):
    def __init__(self, title, size, paths, colors):
        super().__init__("Start", size)
        self.title = title
        self.display = None
        self.paths = paths
        self.colors = colors
        self.target = None
        self.difficultyLabels = ["Easy", "Normal", "Hard"]
        self.curDifficulty = None
        self.prevDifficulty = None
        self.handleClick = False

    def draw(self):
        self.display = pygame.display.set_mode(self.size)
        logo = pygame.image.load(self.paths[2])
        logo = pygame.transform.scale(logo, (logo.get_width() - 100, logo.get_height() - 20))
        bg = pygame.image.load(self.paths[0])
        self.display.blit(bg, (0, 0))
        self.display.blit(logo, (340, 20))
        centerBox = Surface((400, 250))
        centerBox.fill(self.colors["BLUE"])
        self.display.blit(centerBox, (340, 260))
        topCol = Surface((380, 80))
        topCol.fill(self.colors["DARKBLUE"])
        self.display.blit(topCol, ((350, 270)))
        pygame.draw.rect(self.display, self.colors["BLUE"], pygame.Rect(340, 260, 400, 250),  2, 3)
        newBoardButton = TextButton(0, "New Board", self.colors["WHITE"], 'segoeui', 25, self.display, (450, 285), (180, 50), self.colors["LIGHTBLUE"], 2, self.colors["BLUE"], padding=(-3,5))
        newBoardButton.draw()
        colDetail = Surface((380, 30))
        colDetail.fill(self.colors["LIGHTBLUE"])
        cdFont = SysFont('segoeui', 16, bold=True)
        cdObj = cdFont.render("Developed by Robert Guy", True, self.colors["WHITE"])
        self.display.blit(colDetail, (350, 215))
        self.display.blit(cdObj, (442, 218))
        colDetail2 = Surface((380, 30))
        colDetail2.fill(self.colors["DARKBLUE"])
        self.display.blit(colDetail2, (350, 360))
        detailTf = SysFont('segoeui', 16)
        detailObj = detailTf.render("Algorithmically generate a dynamic Sudoku board", True, self.colors["WHITE"])
        self.display.blit(detailObj, (365, 362))
        colDiff = Surface((385, 100))
        colDiff.fill(self.colors["DARKBLUE"])
        self.display.blit(colDiff, (348, 400))
        easyButton = TextButton(0, "Easy", self.colors["BLUE"], 'segoeui', 22, self.display, (360, 425), (120, 50), self.colors["GRAY"], 2, self.colors["WHITE"], padding=(-12,7))
        normalButton = TextButton(1, "Normal", self.colors["WHITE"], 'segoeui', 22, self.display, (480, 425), (120, 50), self.colors["LIGHTBLUE"], 2, self.colors["LIGHTBLUE"], padding=(2,7))
        hardButton = TextButton(2, "Hard", self.colors["BLUE"], 'segoeui', 22, self.display, (600, 425), (120, 50), self.colors["GRAY"], 2, self.colors["WHITE"], padding=(-10,7))
        easyButton.draw()
        normalButton.draw()
        hardButton.draw()
        self.sprites = [newBoardButton, easyButton, normalButton, hardButton]
        self.curDifficulty = self.sprites[2]
        self.util.inherited["difficulty"] = "-n"
        self.prevDifficulty = self.curDifficulty
        pygame.display.update()

    def handle_event(self):
        running = True
        pygame.display.set_caption(self.title)
        pygame.init()
        self.draw()
        while running == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN and self.disabled == False:
                    mousePos = pygame.mouse.get_pos()
                    btns = [s for s in self.sprites if s.intersects(mousePos)]

                    if len(btns) > 0:
                        # Difficulty button
                        if btns[0].text in self.difficultyLabels:
                            self.util.inherited["difficulty"] = "-" + btns[0].text[0].lower()
                            self.curDifficulty = btns[0]
                            self.handleClick = True
                            self.update()
                        # The new board button was clicked; we need to render a new screen.
                        else:
                            if self.util.GRID == None:
                                self.util.GRID = GridScreen((640, 480), self.util.data["paths"], self.util.data["colors"], self.util.data["codes"], self.util.START.display)   
                                self.util.GRID.setUtil(self.util.START.util)
                            self.util.GRID.init()
                            self.disabled = True
                            self.util.GRID.disabled = False
                            self.switchScreen("Grid")

                elif event.type == pygame.MOUSEMOTION and self.disabled == False:
                    mousePos = pygame.mouse.get_pos()
                    btns = [s for s in self.sprites if s.intersects(mousePos)]
                    if self.target != None and self.target[0] not in btns:
                        self.target[0].hovered = False
                        self.update()

                    if len(btns) > 0:
                        self.target = (btns[0], btns[0].text in self.difficultyLabels)
                        self.target[0].hovered = True
                        self.update()

    def update(self):
        
        if self.handleClick == True:
            oldFillColor = self.curDifficulty.fillColor
            oldTextColor = self.curDifficulty.textColor
            oldBorderColor = self.curDifficulty.borderColor
            self.prevDifficulty.selected = False
            self.prevDifficulty.fillColor = self.colors["WHITE"]
            self.prevDifficulty.borderColor = self.colors["GRAY"]
            self.prevDifficulty.textColor = self.colors["BLUE"]
            self.prevDifficulty.draw()
            self.curDifficulty.fillColor = self.colors["LIGHTBLUE"]
            self.curDifficulty.borderColor = self.colors["LIGHTBLUE"]
            self.curDifficulty.textColor = self.colors["WHITE"]
            self.curDifficulty.draw()
            self.curDifficulty.fillColor = oldFillColor
            self.curDifficulty.borderColor = oldBorderColor
            self.curDifficulty.textColor = oldTextColor
            self.curDifficulty.selected = True
            self.prevDifficulty = self.curDifficulty
            self.util.inherited["difficulty"] = "-" + self.curDifficulty.text[0].lower()
            self.handleClick = False
        elif self.target != None and self.target != self.curDifficulty and self.target[0].selected == False:
            oldFillColor = self.target[0].fillColor
            oldTextColor = self.target[0].textColor
            oldBorderColor = self.target[0].borderColor
            if self.target[0].hovered == True:
                isDifficultyButton = self.target[1] == True
                if isDifficultyButton == True:
                    self.target[0].fillColor = self.colors["BLUE"]
                    self.target[0].borderColor = self.colors["BLUE"]
                    self.target[0].textColor = self.colors["WHITE"]
                else:
                    self.target[0].fillColor = self.colors["LIGHTBLUE"]
                self.target[0].draw()
                self.target[0].fillColor = oldFillColor
                self.target[0].textColor = oldTextColor
                self.target[0].borderColor = oldBorderColor
            else:
                self.target[0].draw()

        pygame.display.update()