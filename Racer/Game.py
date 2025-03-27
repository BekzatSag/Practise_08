import pygame, sys
from pygame.locals import *
import random, time
import csv

pygame.init()

#
with open("table_of_records.csv","r") as f:
    reader = csv.reader(f)
    records = list(reader)
    
#FPS 
FPS = 60
FramePerSec = pygame.time.Clock()

#Colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GREY = (200, 200, 200)
DARK_BLUE = (0, 0, 139)

#Variables
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
RECORD = int(records[1][0])
RECORD_COIN = int(records[1][1])
COIN_SCORE = 0
GAME_OVER = True

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40), 0)
        self.speed = SPEED

      def move(self):
        global SCORE
        self.rect.move_ip(0,self.speed)
        if (self.rect.bottom > 600):
            SCORE+=1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                  

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_0 = pygame.image.load("gold-token-icon-cartoon-style-vector-removebg-preview.png")
        self.image = pygame.transform.scale(self.image_0, (40, 40))
        self.coordinates = (random.randint(40, SCREEN_WIDTH-40), 0)
        self.rect = self.image.get_rect(center = self.coordinates)

    def respawn(self):
        self.coordinates = (random.randint(40, SCREEN_WIDTH-40), 0)
        self.rect = self.image.get_rect(center = self.coordinates)
    def move(self):
        self.rect.move_ip(0, 5) 
        if self.rect.bottom > 600:
            self.respawn()


class Button:
    def __init__(self, screen, x, y, WIDTH, HEIGHT, text, font):
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)
        self.text = text
        self.font = pygame.font.SysFont("Verdana", font)
        self.screen = screen


    def draw(self):
        pygame.draw.rect(self.screen, LIGHT_GREY, self.rect, border_radius = 5)
        text_surface = self.font.render(self.text, True, DARK_BLUE)
        text_rect = text_surface.get_rect(center = self.rect.center)
        self.screen.blit(text_surface, text_rect)


    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)



def game():
    global RECORD, RECORD_COIN, SCORE, COIN_SCORE
    COIN_SCORE = 0
    SCORE = 0
    #Button
    R = Button(DISPLAYSURF, SCREEN_WIDTH//2-SCREEN_WIDTH//5//2, 340, SCREEN_WIDTH//5, 50, "RESTART", 15)

    #Sprites        
    P1 = Player()
    E1 = Enemy()
    C = Coin()

    #Sprites Groups
    enemies = pygame.sprite.Group()
    enemies.add(E1)
    coins = pygame.sprite.Group()
    coins.add(C)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(E1)
    all_sprites.add(C)
    

    #User event 
    INC_SPEED = pygame.USEREVENT + 1
    pygame.time.set_timer(INC_SPEED, 1000)

    #Game Loop

    while True:
        
        #Cycles
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                E1.speed += 0.5      
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
        #drawings
        DISPLAYSURF.blit(background, (0,0))
        scores = font_small.render(f"Score: {SCORE}", True, BLACK)
        DISPLAYSURF.blit(scores, (10,10))
        record = font_small.render(f"Record: {RECORD}",True, BLACK)
        DISPLAYSURF.blit(record, (10, 35))
        coin_score = font_small.render(f"Coins : {COIN_SCORE}", True, BLACK)
        DISPLAYSURF.blit(coin_score, (10, 60))
        record_coin = font_small.render(f"Record (coin): {RECORD_COIN}",True, BLACK)
        DISPLAYSURF.blit(record_coin, (10, 85))

        #Moves
        for entity in all_sprites:
            entity.move()
            DISPLAYSURF.blit(entity.image, entity.rect)

        if pygame.sprite.spritecollideany(P1, coins):
           C.respawn()
           pygame.mixer.Sound("coin.wav").play()
           COIN_SCORE+=1
           


        #Collisions
        if pygame.sprite.spritecollideany(P1, enemies):
            pygame.mixer.Sound('crash.wav').play()
            time.sleep(1)


            for entity in all_sprites:
                    entity.kill()    
            DISPLAYSURF.fill(RED)
            DISPLAYSURF.blit(game_over, (30,250))
            R.draw() 
            pygame.display.update()


            while GAME_OVER:
                with open("table_of_records.csv","w", newline="") as f:
                            writer = csv.writer(f)
                            if RECORD < SCORE:
                                RECORD = SCORE
                                
                            if RECORD_COIN < COIN_SCORE:
                                RECORD_COIN = COIN_SCORE
                            writer.writerows([["RECORD", "RECORD_COIN"], [RECORD, RECORD_COIN]])
        
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if R.is_clicked(event):
                        game()
            
        pygame.display.update()

        FramePerSec.tick(FPS)


game()