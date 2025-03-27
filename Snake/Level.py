import pygame

pygame.init()

class Level:
    def __init__(self, screen, colour, speed_of_the_game, space_for_extra_information, WIDTH, HEIGHT):
        self.screen = screen
        self.lvl = 1
        self.text_level = f"{self.lvl} Level"
        self.score = 0
        self.text_score = f"Score: {self.score}"
        self.font = pygame.font.SysFont("Verdana", 15)
        self.colour = colour
        self.speed_of_the_game = speed_of_the_game
        self.space_for_extra_information = space_for_extra_information
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
    def draw(self):
        self.text_level_surface = self.font.render(self.text_level, True, self.colour)
        self.text_level_rect = self.text_level_surface.get_rect(topleft=(self.WIDTH+self.space_for_extra_information//12, self.HEIGHT//15))
        self.screen.blit(self.text_level_surface, self.text_level_rect) 

        self.text_score_surface = self.font.render(self.text_score, True, self.colour)
        self.text_score_rect = self.text_score_surface.get_rect(topleft=(self.WIDTH+self.space_for_extra_information//12, self.HEIGHT//15 + 25))
        self.screen.blit(self.text_score_surface, self.text_score_rect)
    def level_up(self):
        self.score+=1
        self.text_score = f"Score: {self.score}"
        if self.score%4==0: 
            self.lvl +=1
            self.text_level = f"{self.lvl} Level"
            self.speed_of_the_game+=1
        return self.speed_of_the_game
