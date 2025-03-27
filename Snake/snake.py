import pygame
import sys
import random




class Snake:
    def __init__(self, screen, colour, size_of_one_square, WIDTH, HEIGHT, speed):
        self.screen = screen
        self.colour = colour
        self.size_of_one_square = size_of_one_square
        self.x_boundary = WIDTH
        self.y_boundary = HEIGHT
        #I use "choice" to make the snake's position match the apple, I made a 20 by 20 square for 1 pixel
        self.x = random.choice(range(self.size_of_one_square*2, WIDTH - self.size_of_one_square*2, self.size_of_one_square))  
        self.y = random.choice(range(self.size_of_one_square*5, HEIGHT - 5*self.size_of_one_square, self.size_of_one_square))
        self.body = [(self.x, self.y), (self.x, self.y+self.size_of_one_square), (self.x, self.y+self.size_of_one_square*2)]
        self.speed = speed
        self.dy = -speed
        self.dx = 0

        self.apple_eaten = False

    def move(self):
        new_head = (self.body[0][0] + self.dx, self.body[0][1] + self.dy)
        self.body.insert(0, new_head)
        if not self.apple_eaten: 
            self.body.pop(-1)
        else: self.apple_eaten = False

    def directions(self, event): 
        if  event.type == pygame.KEYDOWN:
            #use d_=0 to check that it doesnot move in that direction and self.body[1][0] != self.body[0][0] - self.size_of_one_square to prevent rotation of 180 degrees that causes collisions
            if event.key == pygame.K_LEFT and self.body[1][0] != self.body[0][0] - self.speed:
                self.dy = 0
                self.dx = -self.speed
            if event.key == pygame.K_RIGHT and self.body[1][0] != self.body[0][0] + self.speed:
                self.dy = 0
                self.dx = self.speed
            if event.key == pygame.K_UP and self.body[1][1] != self.body[0][1] - self.speed:
                self.dx = 0
                self.dy = -self.speed
            if event.key == pygame.K_DOWN and self.body[1][1] != self.body[0][1] + self.speed:
                self.dx = 0
                self.dy = self.speed

    def eat(self, apple):
        if self.body[0][0] in range(apple.x, apple.x+self.size_of_one_square) and self.body[0][1] in range(apple.y, apple.y+self.size_of_one_square):
            self.apple_eaten = True
            return True
        return False

    def check_boundary(self):
        if self.body[0][0]>=self.x_boundary or self.body[0][0]<0:
            return True
        if self.body[0][1]>=self.y_boundary or self.body[0][1]<0:
            return True
        return False

    def check_collisions(self):
        for i in range(1, len(self.body)):
            if self.body[0][0] == self.body[i][0] and  self.body[0][1] == self.body[i][1]:
                return True
        return False
            

    def draw(self):
        for i in self.body:
            pygame.draw.rect(self.screen, self.colour, (i[0], i[1], self.size_of_one_square, self.size_of_one_square), border_radius = 0)

