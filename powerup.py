import pygame

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, pos, p_type, groups):
        super().__init__(groups)
        self.type = p_type  # 'shield', 'triple_shot', 'rapid_boost'
        self.speed = 150
        
        # Create a surface and draw a glowing circular indicator
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
        
        if self.type == 'shield':
            color = (39, 174, 96)        # Emerald green
            border_color = (168, 255, 168)
            symbol = "+"
        elif self.type == 'triple_shot':
            color = (41, 128, 185)       # Cobalt blue
            border_color = (173, 216, 230)
            symbol = "3"
        else: # 'rapid_boost'
            color = (243, 156, 18)       # Sun yellow
            border_color = (255, 235, 156)
            symbol = "L"                 # Lightning icon
            
        # Draw circular glowing shapes
        pygame.draw.circle(self.image, color, (16, 16), 14)
        pygame.draw.circle(self.image, border_color, (16, 16), 14, 2)
        
        # Render a simple text symbol inside the power-up icon
        try:
            font = pygame.font.Font("Rustic_Barn.ttf", 16)
        except Exception:
            font = pygame.font.SysFont("arial", 16, bold=True)
            
        text_surf = font.render(symbol, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(16, 16))
        self.image.blit(text_surf, text_rect)
        
        self.rect = self.image.get_frect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self, dt):
        self.rect.y += self.speed * dt
        # Clean up if it travels off screen
        if self.rect.top > 720:
            self.kill()
