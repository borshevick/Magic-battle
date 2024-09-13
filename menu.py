import pygame as pg 
import pygame_menu as pg_menu
from settings import *
import main


class Menu():
    def __init__(self):
        self.player_1 = "earth monk"
        self.player_2 = "earth monk"
        self.screen = pg.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.menu = pg_menu.Menu(title = "Magic battle", width = self.screen.get_width(), height = self.screen.get_height(), theme = pg_menu.themes.THEME_DEFAULT)
        self.menu.add.label(title = "Режим одного")
        self.menu.add.selector("Противник:", [("fire wizard", 1), ("lightning wizard", 2), ("earth monk", 3)], onchange = self.select_player2)
        self.menu.add.button("Играть", self.play)
        self.menu.add.label(title = "Режим двоих")
        self.menu.add.selector("Левый игрок", [("fire wizard", 1), ("lightning wizard", 2), ("earth monk", 3)], onchange = self.select_player)
        self.menu.add.selector("Правый игрок", [("fire wizard", 1), ("lightning wizard", 2), ("earth monk", 3)], onchange = self.select_player2)
        self.menu.add.button("Играть", self.play2)
        self.menu.add.button("Выход", pg_menu.events.EXIT)
        self.menu.mainloop(self.screen)
    def add(self, input):
        print(input)
    def select_player(self, input, index):
        print(input)
        print(index)
        self.player_1 = input[0][0]
    def select_player2(self, input, index):
        print(input)
        print(index)
        self.player_2 = input[0][0]
    def play(self):
        game = main.Game(1, self.player_1, self.player_2)
    def play2(self):
        game = main.Game(2, self.player_1, self.player_2)
menu = Menu()