import pygame as pg
import ball
import pygame.freetype as pgtype
from settings import *
pg.init()


class Player():
    def __init__(self, game):
        self.pictures = game.player_1
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
        self.hitbox = pg.rect.Rect([100, 50], [player_width, player_high]) 
        self.hitbox2 = pg.rect.Rect([100, 50], [player_width//1.5, player_high//1.5]) 
        self.game = game
        self.ball = load_image('images/'+self.pictures+'/magicball.png', self.hitbox.width, self.hitbox.height//3)
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
        self.font = pgtype.Font("images/Acumin Pro (RUS by Slavchansky)/Acumin-ItPro_RUS.ttf", 20)
        self.hp = 100

    def load(self):
        for i in range(1, 4):
            picture = load_image("images/"+self.pictures+"/idle"+str(i)+".png", player_width, player_high)
            picture_left = pg.transform.flip(picture, True, False)
            for i in range(1, 13):
                self.idle_list_left.append(picture_left)
                self.idle_list_right.append(picture)
        for i in range(1, 5):
            picture = load_image("images/"+self.pictures+"/move"+str(i)+".png", player_width, player_high)
            picture_left = pg.transform.flip(picture, True, False)
            for i in range(1, 13):
                self.walk_list_left.append(picture_left)
                self.walk_list_right.append(picture)
        for i in range(1, 2):
            picture = load_image("images/"+self.pictures+"/down.png", player_width, player_high)
            picture_left = pg.transform.flip(picture, True, False)
            for i in range(1, 13):
                self.down_list_left.append(picture_left)
                self.down_list_right.append(picture)
        for i in range(1, 2):
            picture = load_image("images/"+self.pictures+"/charge.png", player_width, player_high)
            picture_left = pg.transform.flip(picture, True, False)
            for i in range(1, 13):
                self.charge_list_left.append(picture_left)
                self.charge_list_right.append(picture)
        for i in range(1, 2):
            picture = load_image("images/"+self.pictures+"/attack.png", player_width, player_high)
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
        for i in self.game.player2.balls:
            if i.hitbox2.colliderect(self.hitbox2) and self.block == False:
                self.game.player2.balls.remove(i)
                self.hp  = self.hp - i.charge//2 
                print(self.hp)
        self.hitbox2.center = self.hitbox.center
        if self.attack == False:
            self.actual_animation = self.idle_list_left if self.rl == -1 else self.idle_list_right
        self.block = False
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.actual_animation = self.walk_list_left
            self.hitbox.x = self.hitbox.x - 1
            self.rl = -1
        elif keys[pg.K_d]:
            self.actual_animation = self.walk_list_right
            self.hitbox.x = self.hitbox.x + 1
            self.rl = 1
        elif keys[pg.K_s]:
            self.actual_animation = self.down_list_left if self.rl == -1 else self.down_list_right
            self.block = True
        elif keys[pg.K_SPACE] and self.attack == False:
            self.actual_animation = self.charge_list_left if self.rl == -1 else self.charge_list_right
            if self.charge < 100:
                self.charge = self.charge + 1
                if self.r > 5:
                    self.r = self.r - 5
                if self.g < 250:
                    self.g = self.g + 5
            else:
                self.attack = True
                self.attack_time = pg.time.get_ticks()
                self.r = 255
                self.g = 0
                self.actual_animation = self.attack_list_left if self.rl == -1 else self.attack_list_right
                if self.rl == 1:
                    magic_ball = ball.Ball(5*self.rl, [self.hitbox.x + 50, self.hitbox.y + 30], self.ball, self.charge)
                else:
                    magic_ball = ball.Ball(5*self.rl, [self.hitbox.x, self.hitbox.y - 10], self.ball, self.charge)
                    magic_ball.picture = pg.transform.flip(magic_ball.picture, True, False)
                self.charge = 0
                self.balls.append(magic_ball)
        if keys[pg.K_SPACE] == False  and self.charge > 0:
            self.attack = True
            self.attack_time = pg.time.get_ticks()
            self.r = 255
            self.g = 0
            self.actual_animation = self.attack_list_left if self.rl == -1 else self.attack_list_right
            if self.rl == 1:
                magic_ball = ball.Ball(5*self.rl, [self.hitbox.x + 50, self.hitbox.y + 30], self.ball, self.charge)
            else:
                magic_ball = ball.Ball(5*self.rl, [self.hitbox.x, self.hitbox.y - 10], self.ball, self.charge)
                magic_ball.picture = pg.transform.flip(magic_ball.picture, True, False)
            self.charge = 0
            self.balls.append(magic_ball)

    def update(self):
        self.animation()
        self.move()
        for i in self.balls:
            i.move()
        if pg.time.get_ticks() - self.attack_time >= 200:
            self.attack = False

    def draw(self):
        pg.draw.rect(self.game.screen, [255, 0, 0], [10, 55, 100, 20])
        pg.draw.rect(self.game.screen, [0, 255, 0], [10, 55, self.hp, 20])
        pg.draw.rect(self.game.screen, [0, 0, 0], [10, 50, 105, 30], 5)
        self.font.render_to(self.game.screen, [20, 55], str(self.hp)+"%", [0, 0, 0], )
        self.game.screen.blit(self.actual_picture, self.hitbox)
        if self.charge > 0:
            if self.rl == 1:
                self.font.render_to(self.game.screen, [self.hitbox.x + 75, self.hitbox.y + 75], str(self.charge)+"%", [self.r, self.g, 0], [0, 0, 0])
            else:
                self.font.render_to(self.game.screen, [self.hitbox.x + 95, self.hitbox.y + 75], str(self.charge)+"%", [self.r, self.g, 0], [0, 0, 0])
        for i in self.balls:
            i.draw(self.game.screen)
       
class Player2():
    def __init__(self, game):
        self.pictures = game.player_2
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
        self.ball = load_image('images/'+self.pictures+'/magicball.png', self.hitbox.width, self.hitbox.height//3)
        self.ball_left = pg.transform.flip(self.ball, True, False)
        self.kadr = 0
        self.timer = 0
        self.rl = -1
        self.block = False
        self.actual_picture = self.actual_animation[0]
        self.charge = 0
        self.attack = False
        self.attack_time = 0
        self.r = 255
        self.g = 0
        self.font = pgtype.Font("images/Acumin Pro (RUS by Slavchansky)/Acumin-ItPro_RUS.ttf", 20)
        self.hp = 100

    def load(self):
        for i in range(1, 4):
            picture = load_image("images/"+self.pictures+"/idle"+str(i)+".png", player_width, player_high)
            picture_left = pg.transform.flip(picture, True, False)
            for i in range(1, 13):
                self.idle_list_left.append(picture_left)
                self.idle_list_right.append(picture)
        for i in range(1, 5):
            picture = load_image("images/"+self.pictures+"/move"+str(i)+".png", player_width, player_high)
            picture_left = pg.transform.flip(picture, True, False)
            for i in range(1, 13):
                self.walk_list_left.append(picture_left)
                self.walk_list_right.append(picture)
        for i in range(1, 2):
            picture = load_image("images/"+self.pictures+"/down.png", player_width, player_high)
            picture_left = pg.transform.flip(picture, True, False)
            for i in range(1, 13):
                self.down_list_left.append(picture_left)
                self.down_list_right.append(picture)
        for i in range(1, 2):
            picture = load_image("images/"+self.pictures+"/charge.png", player_width, player_high)
            picture_left = pg.transform.flip(picture, True, False)
            for i in range(1, 13):
                self.charge_list_left.append(picture_left)
                self.charge_list_right.append(picture)
        for i in range(1, 2):
            picture = load_image("images/"+self.pictures+"/attack.png", player_width, player_high)
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
        for i in self.game.player.balls:
            if i.hitbox2.colliderect(self.hitbox2) and self.block == False:
                self.game.player.balls.remove(i)
                self.hp  = self.hp - i.charge//2 
                print(self.hp)
        self.hitbox2.center = self.hitbox.center
        if self.attack == False:
            self.actual_animation = self.idle_list_left if self.rl == -1 else self.idle_list_right
        self.block = False
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.actual_animation = self.walk_list_left
            self.hitbox.x = self.hitbox.x - 1
            self.rl = -1
        elif keys[pg.K_RIGHT]:
            self.actual_animation = self.walk_list_right
            self.hitbox.x = self.hitbox.x + 1
            self.rl = 1
        elif keys[pg.K_DOWN]:
            self.actual_animation = self.down_list_left if self.rl == -1 else self.down_list_right
            self.block = True
        elif keys[pg.K_PAGEDOWN] and self.attack == False:
            self.actual_animation = self.charge_list_left if self.rl == -1 else self.charge_list_right
            if self.charge < 100:
                self.charge = self.charge + 1
                if self.r > 5:
                    self.r = self.r - 5
                if self.g < 250:
                    self.g = self.g + 5
            else:
                self.attack = True
                self.attack_time = pg.time.get_ticks()
                self.r = 255
                self.g = 0
                self.actual_animation = self.attack_list_left if self.rl == -1 else self.attack_list_right
                if self.rl == 1:
                    magic_ball = ball.Ball(5*self.rl, [self.hitbox.x + 50, self.hitbox.y + 30], self.ball, self.charge)
                else:
                    magic_ball = ball.Ball(5*self.rl, [self.hitbox.x, self.hitbox.y - 10], self.ball, self.charge)
                    magic_ball.picture = pg.transform.flip(magic_ball.picture, True, False)
                self.charge = 0
                self.balls.append(magic_ball)
        if keys[pg.K_PAGEDOWN] == False  and self.charge > 0:
            self.attack = True
            self.attack_time = pg.time.get_ticks()
            self.r = 255
            self.g = 0
            self.actual_animation = self.attack_list_left if self.rl == -1 else self.attack_list_right
            if self.rl == 1:
                magic_ball = ball.Ball(5*self.rl, [self.hitbox.x + 50, self.hitbox.y + 30], self.ball, self.charge)
            else:
                magic_ball = ball.Ball(5*self.rl, [self.hitbox.x, self.hitbox.y - 10], self.ball, self.charge)
                magic_ball.picture = pg.transform.flip(magic_ball.picture, True, False)
            self.charge = 0
            self.balls.append(magic_ball)

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
        if self.charge > 0:
            if self.rl == 1:
                self.font.render_to(self.game.screen, [self.hitbox.x + 75, self.hitbox.y + 75], str(self.charge)+"%", [self.r, self.g, 0], [0, 0, 0])
            else:
                self.font.render_to(self.game.screen, [self.hitbox.x + 95, self.hitbox.y + 75], str(self.charge)+"%", [self.r, self.g, 0], [0, 0, 0])
        for i in self.balls:
            i.draw(self.game.screen)
       