import pygame
BLACK = (0, 0, 0)
GREY = (138, 128, 128)

class Button:
    def __init__(self, screen, x, y, WIDTH, HEIGHT, text, font):
        self.rect = pygame.Rect(x, y, WIDTH, HEIGHT)
        self.text = text
        self.font = pygame.font.SysFont("Verdana", font)
        self.screen = screen


    def draw(self):
        pygame.draw.rect(self.screen, GREY, self.rect, border_radius = 5)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center = self.rect.center)
        self.screen.blit(text_surface, text_rect)


    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)