from Button import Button
import pygame

class IconButton(Button):
    def __init__(self, id,iconPath, parent, pos, size, borderColor, borderThickness, fillColor, padding=None):
        super().__init__(id, parent, pos, size, borderColor, borderThickness, fillColor, padding)
        self.iconPath = iconPath
        
    def draw(self, useCustomShape=False, plotFunc=None):
        super().draw()
        try:
            self.icon = pygame.image.load(self.iconPath)
            paddingX = self.padding[0] if self.padding != None else 0
            paddingY = self.padding[1] if self.padding != None else 0
            xCalc = self.pos[0] + (self.icon.get_size()[0] // 2) + paddingX
            yCalc = self.pos[1] + (self.icon.get_size()[1] // 2) + paddingY
            self.parent.blit(self.icon, (xCalc, yCalc))
        except Exception:
            print("IconButton :: iconPath = " + self.iconPath + " could not be loaded.")