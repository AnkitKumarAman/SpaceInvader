import pygame
from random import randint, uniform

class MeteorDebris(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        size = randint(6, 12)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        # Earthy dark brown/grey colors for rock fragments
        color = (randint(110, 140), randint(90, 110), randint(80, 100))
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2)
        self.rect = self.image.get_frect(center=pos)
        
        # Random initial velocity vector in any direction
        self.velocity = pygame.Vector2(uniform(-1, 1), uniform(-1, 1))
        if self.velocity.length() == 0:
            self.velocity = pygame.Vector2(0, 1)
        self.velocity = self.velocity.normalize() * randint(120, 280)
        
        # Gravity to pull debris downwards slightly over time
        self.gravity = 120
        self.life = 255.0
        self.decay_speed = randint(450, 750) # disappear over ~0.3 - 0.5s

    def update(self, dt):
        # Apply gravity drift
        self.velocity.y += self.gravity * dt
        # Move
        self.rect.center += self.velocity * dt
        # Fade out
        self.life -= self.decay_speed * dt
        if self.life <= 0:
            self.kill()
        else:
            self.image.set_alpha(int(self.life))
