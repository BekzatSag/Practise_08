import pygame
import sys
import random
from snake import Snake
from apple import Apple
from Level import Level
from Game_over import GameOver
from Buttons import Button
import csv

#open file 
with open("table_of_records.csv", "r") as f:
    reader = csv.DictReader(f)
    record = int(list(reader)[0]["Record"])




# Data for display
SPACE_FOR_EXTRA_INFORMATION = 103
HEIGHT_DISPLAY = 800
WIDTH_DISPLAY = 906
#Data for boundary
WIDTH_OF_BOUNDARY = 6

#Area of game
HEIGHT = HEIGHT_DISPLAY
WIDTH = WIDTH_DISPLAY - SPACE_FOR_EXTRA_INFORMATION -WIDTH_OF_BOUNDARY//2


#Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (138, 128, 128)

#"One pixel" of our game
SIZE_OF_SQUARE = 20



def game():
    
    #preperation
    pygame.init()
    screen = pygame.display.set_mode((WIDTH_DISPLAY, HEIGHT_DISPLAY))
    pygame.display.set_caption("Snake")

    background = pygame.image.load("Background.png")
    background_rect = background.get_rect(topleft=(0, 0))

    clock = pygame.time.Clock()

    pygame.mixer.music.load("background.mp3")
    pygame.mixer.music.play(-1)

    global record #i put this to put the final result in global variable

    #speed
    speed_of_the_game = 12
    speed = SIZE_OF_SQUARE


    #game's objects
    snake = Snake(screen, SIZE_OF_SQUARE, WIDTH, HEIGHT, speed) 
    apple = Apple(screen, RED, WIDTH, HEIGHT, SIZE_OF_SQUARE, snake)

    #our scores and level
    level = Level(screen, BLACK, speed_of_the_game, SPACE_FOR_EXTRA_INFORMATION, WIDTH, HEIGHT)

    #GameOver scene
    end_scene = GameOver(screen, WIDTH_DISPLAY, HEIGHT_DISPLAY, BLACK, RED, WIDTH//5)
    restart = Button(screen, WIDTH_DISPLAY//2 -WIDTH_DISPLAY//5//2 , HEIGHT_DISPLAY//2 - HEIGHT_DISPLAY//10//2 + HEIGHT_DISPLAY//7,  WIDTH_DISPLAY//5, HEIGHT_DISPLAY//10, "RESTART", 25)

    #specific boolean variables for check end game(collisions)
    end_of_the_game = False
    music_end_of_the_game = False


    while True:
        clock.tick(speed_of_the_game) #control speed of the game using this part
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if not end_of_the_game:
                snake.directions(event)
            if restart.is_clicked(event):
                game() #for restarting

        screen.fill(WHITE)
        screen.blit(background, background_rect)


        if not end_of_the_game:
            snake.move()
            apple.draw()
            snake.draw()


        if snake.eat(apple):
            apple.respawn(snake)
            speed_of_the_game=level.level_up() 
            
        

        #boundary
        pygame.draw.rect(screen, GREY, (WIDTH, 0, SPACE_FOR_EXTRA_INFORMATION, HEIGHT), 0)
        pygame.draw.line(screen, BLACK, (WIDTH, 0), (WIDTH, HEIGHT_DISPLAY), WIDTH_OF_BOUNDARY)
        level.draw()

        #record
        text_record = pygame.font.SysFont("Verdana", 15).render(f"Record: {record}", True, BLACK)
        text_record_rect = text_record.get_rect(topleft=(WIDTH+SPACE_FOR_EXTRA_INFORMATION//12, HEIGHT//15 + 25 + 25))
        screen.blit(text_record, text_record_rect)  

        #conditional statement to start end game scene
        if snake.check_boundary() or snake.check_collisions():
            end_of_the_game = True
            if not music_end_of_the_game: 
                pygame.mixer.music.stop()
                pygame.time.delay(900)
            end_scene.draw()
            restart.draw()
            if level.score > record:
                record = level.score
                with open("table_of_records.csv", "w", newline="") as f:
                    head = ["Record"]
                    writer = csv.DictWriter(f, fieldnames=head)
                    writer.writeheader()
                    writer.writerow({"Record":record})

        #conditional statement to play looser's song
        if end_of_the_game and not music_end_of_the_game:
            pygame.mixer.music.load("GameOver.mp3")
            pygame.mixer.music.play()
            music_end_of_the_game = True

        
        pygame.display.flip()

game()

