from pygame.font import SysFont
from Button import Button
import pygame

class TextButton(Button):
    def __init__(self, id, text, textColor, fontFamily, fontSize, parent, pos, size, borderColor, borderThickness, fillColor, padding=None, useBold=False):
        super().__init__(id, parent, pos, size, borderColor, borderThickness, fillColor, padding)
        self.text = text
        self.textColor = textColor
        self.fontFamily = fontFamily
        self.fontSize = fontSize
        self.DEFAULT_FONT = 'arial'
        self.useBold = useBold

    def draw(self, useCustomShape=False, plotFunc=None):
        super().draw()
        fontName = self.fontFamily if len([fnt for fnt in pygame.font.get_fonts() if fnt == self.fontFamily]) > 0 else self.DEFAULT_FONT
        fontObj = SysFont(fontName, self.fontSize, bold=self.useBold)
        textField = fontObj.render(self.text, True, self.textColor)
        paddingX = self.padding[0] if self.padding != None else 0
        paddingY = self.padding[1] if self.padding != None else 0
        xCalc = self.pos[0] + (self.size[1] // 2) - paddingX
        yCalc = self.pos[1] + paddingY
        self.parent.blit(textField, (xCalc, yCalc))