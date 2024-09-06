import pygame as pg
import pygame.freetype as pgtype
from settings import *
import player
import bot

pg.init()




class Game:
    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Битва магов")
        self.player = player.Player(self)
        self.player2 = bot.Bot(self)
        self.game_over = False
        self.text = ""
        self.font = pgtype.Font("images/Acumin Pro (RUS by Slavchansky)/Acumin-ItPro_RUS.ttf", 20)
        self.background = load_image("images/background.png", SCREEN_WIDTH, SCREEN_HEIGHT)

        self.clock = pg.time.Clock()
        self.run()

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

    def update(self):
        if self.game_over == False:
            self.player.update()
            self.player2.update()
        if self.player.hp <= 0:
            self.game_over = True
            self.text = "Player 2 Win"
        if self.player2.hp <= 0:
            self.game_over = True
            self.text = "Player 1 Win"

    def draw(self):
        # Отрисовка интерфейса
        self.screen.blit(self.background, (0, 0))
        self.player.draw()
        self.player2.draw()
        self.font.render_to(self.screen, [SCREEN_WIDTH//2, SCREEN_HEIGHT//2], self.text, [0, 0, 0], )
        pg.display.flip()


if __name__ == "__main__":
    Game()