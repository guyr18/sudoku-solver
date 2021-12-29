from Button import Button
import pygame

class CellUI(Button):
    def __init__(self, id, parent, pos, size, fillColor, selectedColor):
        super().__init__(id,  parent=parent, pos=pos, size=size, borderColor=None, borderThickness=None, fillColor=fillColor)
        self.selectedColor = selectedColor
        self.selected = False
        self.fixed = False
        self.row = -1
        self.col = -1
        self.success = False

    def draw(self):
        oldFill = self.fillColor
        oldColor = self.fillColor if self.selected == False else self.selectedColor
        self.fillColor = oldColor
        super().draw()
        self.fillColor = oldFill

    def toggleSelect(self):
        self.selected = False if self.selected == True else True

