from pygame.surface import Surface
import pygame

class Button:
    def __init__(self, id, parent, pos, size, borderColor, borderThickness, fillColor, padding=None):
        self.id = id
        self.parent = parent
        self.pos = pos
        self.size = size
        self.borderColor = borderColor
        self.fillColor = fillColor
        self.surface = Surface(size)
        self.borderThickness = borderThickness
        self.padding = padding
        self.drawn = False
        self.custom = False

    def draw(self, useCustomShape=False, plotFunc=None):
        self.surface.fill(self.fillColor)
        if useCustomShape == True and plotFunc != None or self.custom == True:
            self.custom = True
            plotFunc()
        else:
            self.borderColor = self.borderColor if self.borderColor != None else self.fillColor
            self.borderThickness = 1 if self.borderThickness == None else self.borderThickness
            pygame.draw.rect(self.surface, self.borderColor, (0, 0, self.size[0], self.size[1]), self.borderThickness)

        self.parent.blit(self.surface, self.pos)
        self.drawn = True

    def brighten(self):
        clr = self.fillColor
        red = clr[0]
        blue = clr[1]
        green = clr[2]
        moddedColor = None
        if red == max(red, max(blue, green)):
            newRed = red + (255 - red)
            moddedColor = (newRed, green, blue)
        elif blue == max(blue, max(red, green)):
            newGreen = (green + ((255 - green) // 8))
            moddedColor = (red, newGreen, blue)
        else:
            newBlue = (blue + ((255 - blue) // 8))
            moddedColor = (red, green, newBlue)
        self.surface.fill(moddedColor)
        pygame.draw.rect(self.surface, self.borderColor, (0, 0, self.size[0], self.size[1]), self.borderThickness)
        self.parent.blit(self.surface, self.pos)

    """
    Intersects(target) returns true if the position of this Button instance intersects parameter, 'target'. Where
    parameter 'target' is a (x, y) coordinate tuple. And otherwise, false.
    """
    def intersects(self, target):
        if(self.drawn):
            x = self.pos[0]
            y = self.pos[1]
            w = self.size[0]
            h = self.size[1]
            inXBounds = target[0] >= x and target[0] <= (x + w)
            inYBounds = target[1] >= y and target[1] <= (y + h)
            if inXBounds and inYBounds:
                return True
        return False

        