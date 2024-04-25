import pygame


class Beat(pygame.sprite.Sprite):
    #RGB numbers for white
    WHITE = (255, 255, 255)
    def __init__(self, x, y, color, ordinal):
        super(Beat, self).__init__()
        self.clock = 0.1
        self.radius = 50
        self.rOuter = self.radius * 5
        self.rRing = self.rOuter
        self.ringWidth = 3
        self.dRadius = (self.rOuter // 60) - (self.radius // 60)
        self.outline = 4
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x - self.rOuter, self.y - self.rOuter,
                                2 * self.rOuter, 2 * self.rOuter)
        self.image = pygame.Surface((2 * self.rOuter, 2 * self.rOuter),
                                    pygame.SRCALPHA|pygame.HWSURFACE)
        self.ord = ordinal
        self.fontSize = 50
        self.killTime = 0.2
        self.killClock = None
        self.color = color
        self.draw()

    def update(self, tick):
        self.clock += tick
        if self.killClock != None:
            self.killClock -= tick
            if self.killClock <= 0:
                self.kill()
        if (self.rRing > self.radius):
            self.rRing -= self.dRadius
        self.draw()

    def draw(self):
        self.image.fill((255,255,255,0))
        pygame.draw.circle(self.image, Beat.WHITE, (self.rOuter, self.rOuter),
                           self.rRing, self.ringWidth)
        (radius, outline) = (2 * self.radius, 2 * self.outline)
        surface = pygame.Surface((2 * radius, 2 * radius),
                                 pygame.SRCALPHA|pygame.HWSURFACE)
        pygame.draw.circle(surface, Beat.WHITE, (radius, radius), radius)
        pygame.draw.circle(surface, self.color, (radius, radius),
                           radius-outline)
        (width, height) = (2 * self.radius, 2 * self.radius)
        surface = pygame.transform.smoothscale(surface, (width, height))
        startPoint = self.rOuter - self.radius
        self.image.blit(surface, (startPoint,startPoint))


        if self.killClock != None:
            alpha = max(int((self.killClock/self.killTime) * 255), 0)
            alpha = max(alpha, 0)
            rectToFill = (startPoint, startPoint, width, height)
            self.image.fill((255, 255, 255, alpha), rectToFill,
                            pygame.BLEND_RGBA_MIN)

    def drawText(self):
        font = pygame.font.Font(None, self.fontSize)
        text = font.render(str(self.ord), 1, Beat.WHITE)
        pos = text.get_rect()
        pos.centerx = self.image.get_rect().centerx
        pos.centery = self.image.get_rect().centery
        self.image.blit(text, pos)

    def getPos(self):
        return (self.x, self.y)

    def dying(self):
        self.killClock = self.killTime
