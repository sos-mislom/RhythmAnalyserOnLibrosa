import pygame
import os
import random
import time
from collections import deque

PATH = r"C:\Users\User\Desktop\JackieO_-_The_World_Without_Logos_-_One_Hellsing_opening_rus_66445413.mp3"

class MousePointer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(MousePointer, self).__init__()
        self.radius = 1
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius,
                                2 * self.radius, 2 * self.radius)
