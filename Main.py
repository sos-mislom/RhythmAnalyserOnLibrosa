import pygame
import os
import random
import time
from collections import deque
from Helpers import PATH, MousePointer
from Song import Song
from Beat import Beat
from Text import Text


class PygameGame(object):
    def __init__(self, width=900, height=900, fps=60, title="My Game"):
        (self.width, self.height) = (width, height)
        self.fps = fps
        self.title = title
        self.PLAYBACK_END = pygame.USEREVENT + 1
        self.audioDelay = -1.45
        self.endDelay = 2.0
        self.timeElapsed = 0 + self.audioDelay
        self.audio_path = ""
        self.countdown = None

        pygame.mixer.pre_init(buffer=1024)
        pygame.mixer.init()
        pygame.init()
        pygame.font.init()

        self.initGame()

    def initGame(self):
        self.inGame = True

        self.initBeats()
        self.initTracking()
        pygame.mixer.init()

        self.initSong(PATH)
        pygame.mixer.music.play()

    def initTracking(self):
        self.combo = 0
        self.maxCombo = 0
        self.score = 0
        self.prevAddition = 0
        self.lastBeatHit = (0, 0)
        self.hits = pygame.sprite.Group()
        self.hitKill = 0.5
    def mistake(self, beat):
        if (self.combo > self.maxCombo): self.maxCombo = self.combo
        #Only play noise when the player has a decent-sized combo.
        #Otherwise it's annoying as hell.
        if (self.combo >= 10):
            self.soundMiss.play()

        self.combo = 0

        xColor = (255, 0, 0)
        (x, y) = beat.getPos()
        text = "x"
        size = 100
        missText = Text(self.screen, text, size, x, y, "center", xColor)
        missText.add(self.hits)

        self.misses += 1
    def initBeats(self):
        self.r = 50
        self.beats = pygame.sprite.Group()

        # Having a separate queue allows for indexing (so we can pull the most
        # recent beat)
        self.beatQueue = deque()

        # Choices of color for beats: Red, Blue, Green, Orange
        self.colorChoices = [(255, 0, 0), (0, 0, 255), (24, 226, 24), (247, 162, 15)]
        self.beatColor = (0, 0, 0)
        self.shuffleColor()

        # Needed in order to properly randomize beat positions.
        self.prevX = 0
        self.prevY = 0
        self.maxDist = 200
        self.minDist = 100
        self.beatNum = 1
        self.beatNumMax = 4

    def initSong(self, path):
        startTime = time.time()
        self.song = Song(PATH)
        self.times = self.song.getBeatTimes()
        self.nextBeat = self.times.pop(0)
        self.audio_path = self.song.getPath()

        pygame.mixer.music.load(PATH)
        endTime = time.time()

        loadTime = abs(endTime - startTime)
        self.timeElapsed -= loadTime

    def run(self):
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        while self.inGame:
            self.songLoop(clock)

        pygame.font.quit()
        pygame.mixer.quit()
        pygame.quit()

    def songLoop(self, clock):
        tick = clock.tick_busy_loop(self.fps) / 1000 

        pygame.mixer.music.unpause()
        self.timeElapsed += tick
        self.gameTimerFired(self.timeElapsed, tick)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.inGame = False

        if self.countdown != None:
            self.countdown -= tick
            if self.countdown <= 0:
                self.inGame = False

        self.songLoopUpdate()
        pygame.display.flip()
        
    def addHit(self, beat):
        colorPerfect = (125, 200, 255)
        colorGood = (88, 255, 88)
        colorBad = (255, 226, 125)
    
        (x, y) = beat.getPos()
        text = str(self.prevAddition)
        if (self.prevAddition == self.scorePerfect):
            color = colorPerfect
        elif (self.prevAddition == self.scoreGood):
            color = colorGood
        elif (self.prevAddition == self.scoreBad):
            color = colorBad
        else: return
        size = 50
        hitText = Text(self.screen, text, size, x, y, "center", color)
        hitText.add(self.hits)
    def songLoopUpdate(self):
        BLACK = (0, 0, 0)
        self.screen.fill(BLACK)
        self.printText()
        self.hits.draw(self.screen)
        self.beats.draw(self.screen)
        
    def initBeatTiming(self):
        self.beatApproach = 1.0
        self.windowWidth = 0.06
    
        self.goodLate = self.beatApproach + self.windowWidth
        self.badLate = self.goodLate + self.windowWidth
        self.missLate = self.badLate + self.windowWidth
        self.beatKill = self.missLate + self.windowWidth
    
        self.perfectEarly = self.beatApproach - self.windowWidth
        self.goodEarly = self.perfectEarly - self.windowWidth
        self.badEarly = self.goodEarly - self.windowWidth
        self.missEarly = self.badEarly - self.windowWidth
    
    def gameTimerFired(self, time, tick):
        if (time + 1.0) >= self.nextBeat:
            if len(self.times) > 0:
                self.addBeat()
                self.nextBeat = self.times.pop(0)
        for hit in self.hits:
            hit.update(tick)
            if ((hit.killClock == None) and (hit.clock >= self.hitKill)):
                hit.dying()
        for beat in self.beats:
            beat.update(tick)
            if ((beat.killClock == None) and (beat.clock >= 1.5)):
                beat.dying()
                self.beatQueue.remove(beat)

        if len(self.times) == 0 and len(self.beats) == 0 and self.countdown == None:
            self.endGame()

    def endGame(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        self.inGame = False

    def addBeat(self):
        #Can't let beat go off-screen.
        (offsetW, offsetH) = (self.width-self.r, self.height-self.r)
        if (self.prevX == None) and (self.prevY == None):
            x = random.randint(0+self.r, offsetW)
            y = random.randint(0+self.r, offsetH)
        else:
            if (self.prevX < self.width // 4): xMult = 1
            elif (self.prevX > 3*(self.width // 4)): xMult = -1
            else: xMult = random.choice([-1, 1])

            if (self.prevY < self.height // 4): yMult = 1
            elif (self.prevY > 3*(self.height // 4)): yMult = -1
            else: yMult = random.choice([-1, 1])

            dx = random.randint(self.minDist, self.maxDist) * xMult
            dy = random.randint(self.minDist, self.maxDist) * yMult
            (x, y) = (self.prevX + dx, self.prevY + dy)

        (self.prevX, self.prevY) = (x, y)
        beat = Beat(x, y, self.beatColor, self.beatNum)
        beat.add(self.beats)
        self.beatQueue.append(beat)
        self.updateOrdinal()
    def updateOrdinal(self):
        self.beatNum += 1
        if self.beatNum > self.beatNumMax:
            self.beatNum = 1
            self.shuffleColor()
    def shuffleColor(self):
        color = random.choice(self.colorChoices)
        self.beatColor = color

    def printText(self):
        WHITE = (255, 255, 255)
        # print("Combo: " + str(self.combo) + "     Score: " + str(self.score),
        #       (0.1 * self.width, 0.9 * self.height), WHITE, 50)

    def beatPressed(self):
        if (len(self.beatQueue) == 0):
            return
        (x, y) = pygame.mouse.get_pos()
        click = MousePointer(x, y)

        #Only the oldest beat placed can be clicked on.
        beat = self.beatQueue[0]
        if (pygame.sprite.collide_circle(beat, click)):
            mistake = self.addScore(beat.clock, beat)
            if (mistake == None):
                return
            elif mistake:
                self.mistake(beat)
            else:
                self.combo += 1
            beat.dying()
            self.beatQueue.popleft()
    @staticmethod
    def main():
        game = PygameGame()
        game.run()

if __name__ == "__main__":
    PygameGame.main()
