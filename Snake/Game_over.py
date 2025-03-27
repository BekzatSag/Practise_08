import pygame

class GameOver:
    def __init__(self, screen, WIDTH_DISPLAY, HEIGHT_DISPLAY, colour_screen, colour_text, font):
        self.screen = screen
        self.colour_screen = colour_screen
        self.colour_text = colour_text
        self.text = "Game Over"
        self.font = pygame.font.Font(None, font)
        self.WIDTH_DISPLAY = WIDTH_DISPLAY
        self.HEIGHT_DISPLAY = HEIGHT_DISPLAY
    def draw(self):
        self.text_surface = self.font.render(self.text, True, self.colour_text)
        self.text_rect = self.text_surface.get_rect(center=(self.WIDTH_DISPLAY//2, self.HEIGHT_DISPLAY//2))
        self.screen.fill(self.colour_screen)
        self.screen.blit(self.text_surface, self.text_rect)
