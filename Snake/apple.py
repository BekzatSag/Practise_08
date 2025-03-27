import pygame 
import random

class Apple:
    def __init__(self,screen, colour, WIDTH, HEIGHT, size_of_one_square, snake):
        self.screen = screen
        self.colour = colour
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.size_of_one_square = size_of_one_square
        self.x = 0 
        self.y = 0
        self.respawn(snake)
        
    def draw(self):
        self.rect = pygame.Rect(self.x, self.y, self.size_of_one_square, self.size_of_one_square)
        pygame.draw.rect(self.screen, self.colour, self.rect)

    def respawn(self, snake):
        while True:
                new_x = random.choice(range(0+self.size_of_one_square*2, self.WIDTH-self.size_of_one_square*2, self.size_of_one_square))
                new_y = random.choice(range(0+self.size_of_one_square*2, self.HEIGHT-self.size_of_one_square*2, self.size_of_one_square))
                if snake.body[0] != (new_x, new_y):
                    self.x = new_x
                    self.y = new_y
                    break
    
