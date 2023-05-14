import pygame
import sys
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
WHITE = (255, 255, 255)



class RetryButton(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("img\Buttons\RetryButton.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.5), int(self.image.get_height() * 0.5)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    

class QuitButton(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("img\Buttons\QuitButton.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.5), int(self.image.get_height() * 0.5)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)