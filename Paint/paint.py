import pygame
import sys
import math

import pygame.display

WIDTH = 1000
HEIGHT = 1000

#Colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

HEIGHT_MENU = 100

#init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

# our circle
class Circle:
    def __init__(self, screen, x, y, r, font):
        self.x = x
        self.y = y
        self.r = r
        self.screen = screen
        self.font = font
    def draw(self):
        pygame.draw.circle (self.screen, BLACK, (self.x, self.y), self.r, self.font)
    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and (event.pos[0] - self.x)**2 + (event.pos[1] - self.y)**2 <=self.r**2 
#rectangle
class Rectangle:
    def __init__(self, screen, x, y, w, h, font):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.font = font
    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect,  self.font)
    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
    

#colour selection
class Colour(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, w, h, colour):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.colour = colour
    def draw(self):
        pygame.draw.rect(screen, self.colour, self.rect)
    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
    

#colours
black = Colour(screen, WIDTH//2, 0, 50, 50, BLACK)
white = Colour(screen, WIDTH//2, 50, 50, 50, WHITE)
red = Colour(screen, WIDTH//2+50, 0, 50, 50, RED)
blue = Colour(screen, WIDTH//2+50, 50, 50, 50, BLUE)
yellow = Colour(screen, WIDTH//2+100, 0, 50, 50, YELLOW)
cyan = Colour(screen, WIDTH//2+100, 50, 50, 50, CYAN)
magneta = Colour(screen, WIDTH//2+150, 0, 50, 50, MAGENTA)
green = Colour(screen, WIDTH//2+150, 50, 50, 50, GREEN)




#sprites groups
colours = pygame.sprite.Group()
colours.add(white, black, red, blue, yellow, cyan, magneta, green)

#main figures
C = Circle(screen, WIDTH//2//2 + WIDTH//2//2//2, HEIGHT_MENU//2, 30, 5)
R = Rectangle(screen, WIDTH//2//2//2 - WIDTH//2//5//2, HEIGHT_MENU//2 - (HEIGHT_MENU-40)//2, WIDTH//2//5, HEIGHT_MENU-40, 5)
Eraser = Rectangle(screen, WIDTH//2+300, HEIGHT_MENU//2-29, 50, 60, 5)

#all rectangles variables
rectangle_is_clicked = False
drawing_rectangle = False
temp_rect = (0, 0, 0, 0, 0, 0)

#erasers variables
eraser_is_clicked = False
points_of_eraser = []

#circles variables
circle_is_clicked = False
drawing_circle = False
temp_circle = (0, 0, 0, 0, 0)

#main list to draw
figures = []

current_colour = BLACK

while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #rectnagle
        if R.is_clicked(event):
           if circle_is_clicked: circle_is_clicked = False
           if eraser_is_clicked: eraser_is_clicked = False
           rectangle_is_clicked = not rectangle_is_clicked
        #cirlce
        if C.is_clicked(event):
            if rectangle_is_clicked: rectangle_is_clicked = False
            if eraser_is_clicked: eraser_is_clicked = False
            circle_is_clicked = not circle_is_clicked
        #colours
        for i in colours:
            if i.is_clicked(event): current_colour = i.colour
        #eraser
        if Eraser.is_clicked(event):
            if rectangle_is_clicked: rectangle_is_clicked = False
            if circle_is_clicked: circle_is_clicked = False
            eraser_is_clicked = not eraser_is_clicked



        #all steps to draw rectangle
        if rectangle_is_clicked:
            if event.type == pygame.MOUSEBUTTONDOWN and event.pos[1] > HEIGHT_MENU:
                start = event.pos
                drawing_rectangle = True

        if drawing_rectangle and event.type == pygame.MOUSEMOTION:
            end_x, end_y = event.pos
            #this part calculate initial position and width and height of rectangeels
            end_x = max(0, min(end_x, WIDTH))  
            end_y = max(HEIGHT_MENU+2.5, min(end_y, HEIGHT))
            w = abs(end_x - start[0])
            h = abs(end_y - start[1])

            temp_rect = (min(start[0], end_x), min(start[1], end_y), w, h, current_colour)

        if drawing_rectangle and event.type == pygame.MOUSEBUTTONUP:
            end_x, end_y = event.pos
            end_x = max(0, min(end_x, WIDTH))  
            end_y = max(HEIGHT_MENU+2.5, min(end_y, HEIGHT))
            w = abs(end_x - start[0])
            h = abs(end_y - start[1])

            figures.append(("r", min(start[0], end_x), min(start[1], end_y), w, h, current_colour))
            drawing_rectangle = False
            temp_rect = (0, 0, 0, 0, 0, 0)



        #csteps to draw circle
        if circle_is_clicked:
            if event.type == pygame.MOUSEBUTTONDOWN and event.pos[1] > HEIGHT_MENU:
                center = event.pos
                drawing_circle = True

        if drawing_circle and event.type == pygame.MOUSEMOTION:
            x = event.pos[0]
            y = event.pos[1]
            r = round(math.sqrt((x - center[0])**2 + (y- center[1])**2)) #math function for circle
            if center[1] - r > HEIGHT_MENU+2.5:
                max_r = min(center[0], WIDTH - center[0], center[1] - HEIGHT_MENU, HEIGHT - center[1])
                r = min(r, max_r)
                temp_circle = ("c", center[0], center[1], r, current_colour)

        if drawing_circle and event.type==pygame.MOUSEBUTTONUP:
            x = event.pos[0]
            y = event.pos[1]
            drawing_circle = False
            figures.append(temp_circle)
            temp_circle = (0, 0, 0, 0, 0)

        #eraser
        if eraser_is_clicked:
            if event.type == pygame.MOUSEMOTION and pygame.mouse.get_pressed()[0]:
                if event.pos[1] > HEIGHT_MENU+2.5+10:
                    figures.append(("e", event.pos[0], event.pos[1], WHITE))
        

  

    #this part draw recyangles of our colours
    for colour in colours:
        colour.draw()

    #boundaries
    pygame.draw.line(screen, BLACK, (0, HEIGHT_MENU), (WIDTH, HEIGHT_MENU), 5)  
    pygame.draw.line(screen, BLACK, (WIDTH//2, 0), (WIDTH//2, HEIGHT_MENU), 5)
    pygame.draw.line(screen, BLACK, (WIDTH//2//2, 0), (WIDTH//2//2, HEIGHT_MENU), 5)
    pygame.draw.line(screen, BLACK, (WIDTH//2+200, 0), (WIDTH//2+200, HEIGHT_MENU), 5)
   

    #fonts to checking if figure is clicked by user
    if rectangle_is_clicked:
        R.font = 0
    else: R.font = 5

    if circle_is_clicked:
        C.font = 0
    else: C.font = 5

    if eraser_is_clicked:
        Eraser.font = 0
    else: Eraser.font = 5

    
    #simple function to draw icons of figures
    C.draw()
    R.draw()
    Eraser.draw()
    
    #i use first element in list to indicate is it rectangle or cicrle or eraser
    for i in figures:
        if i[0] =="r":
            pygame.draw.rect(screen,i[5], (i[1], i[2], i[3], i[4]))
        if i[0] == "c":
            pygame.draw.circle(screen, i[4], (i[1], i[2]), i[3])
        if i[0] == "e":
            pygame.draw.circle(screen, i[3], (i[1], i[2]), 10)


    #this part to draw temporary figures (when mouse is pressed)
    if drawing_rectangle:
        pygame.draw.rect(screen, temp_rect[4], (temp_rect[0], temp_rect[1], temp_rect[2], temp_rect[3]))

    if drawing_circle:
        pygame.draw.circle(screen, temp_circle[4], (temp_circle[1], temp_circle[2]), temp_circle[3])




    pygame.display.flip()  
