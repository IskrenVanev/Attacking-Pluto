from imports import *
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.explosion_images = [
            pygame.image.load("img/Explosions/Expl1.png"),
            pygame.image.load("img/Explosions/Expl2.png"),
            pygame.image.load("img/Explosions/Expl3.png"),
            pygame.image.load("img/Explosions/Expl4.png"),
            pygame.image.load("img/Explosions/Expl5.png"),
            pygame.image.load("img/Explosions/Expl6.png"),
            # Add more explosion frames as needed
        ]
        self.image_index = 0  # Current image index for animation
        self.image = self.explosion_images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame_delay = 5  # Delay between animation frames
        self.frame_counter = 0  # Counter to control frame change

    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.image_index += 1
            if self.image_index >= len(self.explosion_images):
                self.kill()  # Remove the explosion sprite after the animation
            else:
                self.image = self.explosion_images[self.image_index]
                self.frame_counter = 0
