import pygame
import sys
import math


pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Paint App")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill(WHITE)

class Button:
    def __init__(self, x, y, width, height, text, color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.action = action  # Function to execute when clicked

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.Font(None, 30)
        text_surface = font.render(self.text, True, WHITE)
        text_surface_rect = text_surface.get_rect(center = self.rect.center)
        screen.blit(text_surface, text_surface_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.action()

drawing = False
brush_color = BLACK  # Default color
circle_mode = False  # check for circle drawing
circle_start = None
circle_radius = 0
rectangle_mode = False # check for rectangle drawing
rectangle_start = None 
eraser_mode = False # check for eraser "drawing"
eraser_start = (0, 0)
start_eraser = None
start_drawing = None

# Functions for buttons
def set_color_black():
    global brush_color
    brush_color = BLACK

def set_color_red():
    global brush_color
    brush_color = RED

def set_color_green():
    global brush_color
    brush_color = GREEN

def set_color_blue():
    global brush_color
    brush_color = BLUE

def clear_screen():
    canvas.fill(WHITE)  

def exit_app():
    pygame.quit()
    sys.exit()

def toggle_circle_mode():
    global circle_mode, rectangle_mode, eraser_mode
    circle_mode = not circle_mode
    rectangle_mode = False  
    eraser_mode = False

#new functions
def rectangle_mode_set():
    global rectangle_mode, circle_mode, eraser_mode 
    rectangle_mode = not rectangle_mode
    circle_mode = False
    eraser_mode = False
    
def eraser_mode_set():
    global rectangle_mode, circle_mode, eraser_mode 
    rectangle_mode = False
    circle_mode = False
    eraser_mode = not eraser_mode



buttons = [
    Button(10, 10, 70, 30, "Black", BLACK, set_color_black),
    Button(90, 10, 70, 30, "Red", RED, set_color_red),
    Button(170, 10, 70, 30, "Green", GREEN, set_color_green),
    Button(250, 10, 70, 30, "Blue", BLUE, set_color_blue),
    Button(330, 10, 80, 30, "Clear", GRAY, clear_screen),
    Button(420, 10, 80, 30, "Exit", GRAY, exit_app),
    Button(510, 10, 80, 30, "Circle", BLUE, toggle_circle_mode), 
    Button(600, 10, 100, 30, "Rectangle", BLUE,  rectangle_mode_set), #button for ractangle
    Button(710, 10, 70, 30, "Eraser", BLUE,  eraser_mode_set) #button for eraser
]



# Main loop
while True:
    screen.fill(WHITE) 
    screen.blit(canvas, (0, 0))  # Redraw the persistent canvas

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  
                if circle_mode:
                    circle_start = pygame.mouse.get_pos()
                    circle_radius = 0  # Start growing/shrinking dynamically
                elif rectangle_mode:
                    rectangle_start = pygame.mouse.get_pos()
                    #default variables for rectangle
                    end_x = 0
                    end_y = 0
                    w = 0
                    h = 0
                elif eraser_mode: 
                    #default variables for rectangle
                    drawing = False
                elif not start_drawing:
                    drawing = True
                    start_drawing = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
                if circle_mode and circle_start:
                    # Save final circle with its color
                    pygame.draw.circle(canvas, brush_color, circle_start, circle_radius, 2)  # Draw on canvas
                    circle_start = None
                    circle_radius = 0  # Reset for next circle


                if rectangle_mode and rectangle_start:
                    #math steps to allow us to draw rectangle toward top-left, top-right, bottom-right (not only bottom-right)
                    end_x = max(0, min(end_x, WIDTH))  
                    end_y = max(50, min(end_y, HEIGHT))
                    w = abs(end_x - rectangle_start[0])
                    h = abs(end_y - rectangle_start[1])

                    pygame.draw.rect(canvas, brush_color, (min(rectangle_start[0], end_x), min(rectangle_start[1], end_y), w, h), 2)  # Draw on canvas
                    rectangle_start = None
                    w = 0
                    h = 0
                    end_y = 0
                    end_x = 0
                if start_drawing:
                    start_drawing = None

        #draw buttons           
        for button in buttons:
            button.check_click(event)


                     
    if circle_mode and circle_start and pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Calculate dynamic radius based on distance from initial click position
        circle_radius = int(math.sqrt((mouse_x - circle_start[0]) ** 2 + (mouse_y - circle_start[1]) ** 2))
        circle_max_radius = min(circle_start[0], WIDTH - circle_start[0], circle_start[1] - 50, HEIGHT - circle_start[1])
        circle_radius = min(circle_radius, circle_max_radius)
        screen.blit(canvas, (0, 0))  # Keep previous drawings visible
        pygame.draw.circle(screen, brush_color, circle_start, circle_radius, 2)  # Draw on screen (preview)
    

    if rectangle_mode and rectangle_start and pygame.mouse.get_pressed()[0]:
        # Calculate dynamic position of top-left corner and width, height
        end_x, end_y = pygame.mouse.get_pos()
        end_x = max(0, min(end_x, WIDTH))  
        end_y = max(50, min(end_y, HEIGHT))
        w = abs(end_x - rectangle_start[0])
        h = abs(end_y - rectangle_start[1])
        screen.blit(canvas, (0, 0)) 
        pygame.draw.rect(screen, brush_color, (min(rectangle_start[0], end_x), min(rectangle_start[1], end_y), w, h), 2)   

    if eraser_mode and pygame.mouse.get_pressed()[0]:
        eraser_x, eraser_y  = pygame.mouse.get_pos()
        if eraser_y > 50:  
            pygame.draw.circle(canvas, WHITE, (eraser_x, eraser_y), 5)  # Draw (Eraser) on canvas directly
    


    if drawing:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y > 50:  # Prevent drawing on buttons
            pygame.draw.line(canvas, brush_color, (mouse_x, mouse_y), start_drawing, 5)  # Draw on canvas directly
            start_drawing = (mouse_x, mouse_y)

    # Draw UI Buttons
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, 50))  # Top menu bar
    for button in buttons:
        button.draw(screen)






    pygame.display.flip()
