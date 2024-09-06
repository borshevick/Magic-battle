import pygame as pg
import ball
import pygame.freetype as pgtype
from settings import *
import random
pg.init()


class Bot():
    def __init__(self, game):
        self.idle_list_right= []
        self.idle_list_left = []
        self.walk_list_right = []
        self.walk_list_left = []
        self.down_list_right = []
        self.down_list_left = []
        self.charge_list_right = []
        self.charge_list_left = []
        self.attack_list_right = []
        self.attack_list_left = []
        self.balls = []
        self.load()
        self.actual_animation = self.idle_list_right
        self.hitbox = pg.rect.Rect([600, 50], [player_width, player_high]) 
        self.hitbox2 = pg.rect.Rect([100, 50], [player_width//1.5, player_high//1.5]) 
        self.game = game
        self.ball = load_image('images/fire wizard/magicball.png', self.hitbox.width, self.hitbox.height//2)
        self.ball_left = pg.transform.flip(self.ball, True, False)
        self.kadr = 0
        self.timer = 0
        self.rl = 1
        self.block = False
        self.actual_picture = self.actual_animation[0]
        self.charge = 0
        self.attack = False
        self.attack_time = 0
        self.r = 255
        self.g = 0
        self.hp = 100
        self.font = pgtype.Font("images/Acumin Pro (RUS by Slavchansky)/Acumin-ItPro_RUS.ttf", 20)
        self.walk = False
        self.distance = 0 


    def load(self):
        for i in range(1, 4):
            picture = load_image("images/fire wizard/idle"+str(i)+".png", player_width, player_high)
            picture_left = pg.transform.flip(picture, True, False)
            for i in range(1, 13):
                self.idle_list_left.append(picture_left)
                self.idle_list_right.append(picture)
        for i in range(1, 5):
            picture = load_image("images/fire wizard/move"+str(i)+".png", player_width, player_high)
            picture_left = pg.transform.flip(picture, True, False)
            for i in range(1, 13):
                self.walk_list_left.append(picture_left)
                self.walk_list_right.append(picture)
        for i in range(1, 2):
            picture = load_image("images/fire wizard/down.png", player_width, player_high)
            picture_left = pg.transform.flip(picture, True, False)
            for i in range(1, 13):
                self.down_list_left.append(picture_left)
                self.down_list_right.append(picture)
        for i in range(1, 2):
            picture = load_image("images/fire wizard/charge.png", player_width, player_high)
            picture_left = pg.transform.flip(picture, True, False)
            for i in range(1, 13):
                self.charge_list_left.append(picture_left)
                self.charge_list_right.append(picture)
        for i in range(1, 2):
            picture = load_image("images/fire wizard/attack.png", player_width, player_high)
            picture_left = pg.transform.flip(picture, True, False)
            for i in range(1, 13):
                self.attack_list_left.append(picture_left)
                self.attack_list_right.append(picture)

    def animation(self):
        # if pg.time.get_ticks() - self.timer >= 200:
            if self.kadr < len(self.actual_animation):
                self.actual_picture = self.actual_animation[self.kadr]
                self.kadr = self.kadr + 1
            else:
                self.kadr = 0 
            self.timer = pg.time.get_ticks()

    def move(self):
        self.hitbox2.center = self.hitbox.center
        if self.attack == False:
            self.actual_animation = self.idle_list_left if self.rl == -1 else self.idle_list_right
        self.block = False
        for i in self.game.player.balls:
            if abs(self.hitbox2.centerx - i.hitbox2.centerx) <= 200 and i.chance == 1:
                self.actual_animation = self.down_list_left if self.rl == -1 else self.down_list_right
                self.walk = False
                self.block = True
            if i.hitbox2.colliderect(self.hitbox2) and self.block == False:
                self.game.player.balls.remove(i)
                self.hp  = self.hp - i.charge//2 
                print(self.hp)
        attack = random.randint(1, 1000)
        if attack <= 10 and self.attack != True and self.walk != True and self.block != True:
            if self.hitbox.centerx > self.game.player.hitbox.centerx:
                self.rl = -1
            else:
                self.rl = 1
            self.attack = True
            self.charge = (pg.time.get_ticks() - self.attack_time)//100 
            if self.rl == 1:
                magic_ball = ball.Ball(5*self.rl, [self.hitbox.x + 50, self.hitbox.y + 50], self.ball_left, self.charge)
            else:
                magic_ball = ball.Ball(5*self.rl, [self.hitbox.x, self.hitbox.y - 10], self.ball, self.charge)
            self.balls.append(magic_ball)
            self.attack_time = pg.time.get_ticks()
        if self.attack == True: 
            self.actual_animation = self.attack_list_left if self.rl == -1 else self.attack_list_right
            if pg.time.get_ticks() - self.attack_time >= 200:
                self.attack = False
        walk = random.randint(1, 1000)
        if walk <= 10 and self.attack == False and self.walk == False:
            self.walk = True
            self.rl = (-1)**random.randint(0, 1)
            self.distance = random.randint(50, 300)
        if self.walk == True:
            self.actual_animation = self.walk_list_left if self.rl == -1 else self.walk_list_right
            if self.rl == -1 and self.hitbox.left <= 0 or self.rl == 1 and self.hitbox.right >= SCREEN_WIDTH:
                self.walk = False
            else:
                self.hitbox.x = self.hitbox.x + self.rl*2
                self.distance = self.distance - 2
            if self.distance <= 0:
                self.walk = False

    def update(self):
        self.animation()
        self.move()
        for i in self.balls:
            i.move()
        if pg.time.get_ticks() - self.attack_time >= 200:
            self.attack = False

    def draw(self):
        pg.draw.rect(self.game.screen, [255, 0, 0], [SCREEN_WIDTH - 105, 55, 100, 20])
        pg.draw.rect(self.game.screen, [0, 255, 0], [SCREEN_WIDTH - 105, 55, self.hp, 20])
        pg.draw.rect(self.game.screen, [0, 0, 0], [SCREEN_WIDTH - 110, 50, 105, 30], 5)
        self.font.render_to(self.game.screen, [SCREEN_WIDTH - 105, 55], str(self.hp)+"%", [0, 0, 0], )
        self.game.screen.blit(self.actual_picture, self.hitbox)
        for i in self.balls:
            i.draw(self.game.screen)