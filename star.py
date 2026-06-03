import pygame
from random import randint

class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf, screen_width, screen_height, depth=2):
        super().__init__(groups)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.depth = depth # 1 = Foreground, 2 = Midground, 3 = Background
        
        # Scale and adjust opacity of star based on its depth layer for 3D parallax effect
        if self.depth == 1:
            self.image = pygame.transform.scale_by(surf, 1.2)
            self.speed = randint(140, 220)
        elif self.depth == 2:
            self.image = pygame.transform.scale_by(surf, 0.8)
            self.image.set_alpha(180)
            self.speed = randint(70, 120)
        else:
            self.image = pygame.transform.scale_by(surf, 0.4)
            self.image.set_alpha(100)
            self.speed = randint(25, 60)
            
        self.rect = self.image.get_frect(center=(randint(0, screen_width), randint(0, screen_height)))

    def update(self, dt):
        self.rect.y += self.speed * dt
        # If star scrolls past the bottom, wrap it around to the top
        if self.rect.top > self.screen_height:
            self.rect.bottom = 0
            self.rect.x = randint(0, self.screen_width)
