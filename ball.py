import pygame as pg
import random
from settings import *


class Ball():
    def __init__(self, speed, xy, picture, charge):
        self.speed = speed
        self.xy = xy
        self.picture = picture
        self.hitbox = pg.Rect(xy, self.picture.get_size())
        self.hitbox2 = pg.Rect(xy,[40, 120])
        self.chance = random.randint(0, 1)
        self.charge = charge
    def draw(self, screen):
        screen.blit(self.picture, self.hitbox)

    def move(self):
        self.hitbox2.center = self.hitbox.center
        self.hitbox.x = self.hitbox.x + self.speed
        # if self.hitbox >= SCREEN_WIDTH:
    