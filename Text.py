import os

import pygame


class Text(pygame.sprite.Sprite):
    WHITE = (255, 255, 255)
    FONT = os.path.normpath("Fonts/Nunito-Regular.ttf")
    def __init__(self, surface, text, size, x, y, anchor="nw",
                 color=WHITE, fontType=FONT):
        super(Text, self).__init__()
        (self.x, self.y) = (x, y)
        self.text = text
        self.anchor = anchor
        self.color = color
        self.clock = 0

        #Font downloaded from http://google.com/fonts
        self.font = pygame.font.Font(fontType, size)

        (self.width, self.height) = self.font.size(self.text)
        self.initPos()
        self.rect = pygame.Rect(self.rectX, self.rectY,
                                self.width, self.height)
        self.image = pygame.Surface((self.width, self.height), pygame.HWSURFACE)
        self.killTime = 0.2
        self.killClock = None
        self.draw()
        self.target = surface
        self.target.blit(self.image, (self.rectX, self.rectY))

    def initPos(self):
        if (self.anchor == "nw"):
            self.rectX = self.x
            self.rectY = self.y
        elif (self.anchor == "ne"):
            self.rectX = self.x - self.width
            self.rectY = self.y
        elif (self.anchor == "sw"):
            self.rectX = self.x
            self.rectY = self.y - self.height
        elif (self.anchor == "se"):
            self.rectX = self.x - self.width
            self.rectY = self.y - self.height
        elif (self.anchor == "center"):
            self.rectX = self.x - self.width//2
            self.rectY = self.y - self.height//2

    def draw(self):
        text = self.font.render(self.text, 1, self.color)
        self.image.blit(text, (0, 0))

        if self.killClock != None:
            alpha = int((self.killClock/self.killTime) * 255)
            alpha = max(alpha, 0)
            self.image.set_alpha(alpha)

    def update(self, tick=0):
        self.clock += tick
        if self.killClock != None:
            self.killClock -= tick
            if self.killClock <= 0:
                self.kill()
        self.draw()
        self.target.blit(self.image, (self.rectX, self.rectY))

    def dying(self):
        self.killClock = self.killTime