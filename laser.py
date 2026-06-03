import pygame
class Laser(pygame.sprite.Sprite):
    def __init__(self,surf,pos,groups):
        super().__init__(groups)
        self.image=surf
        self.rect=self.image.get_frect(midbottom=pos)
        self.mask=pygame.mask.from_surface(self.image)
        self.direction=pygame.Vector2()
    def update(self,dt):
        keys=pygame.key.get_pressed()
        self.direction.x=int(keys[pygame.K_d])-int(keys[pygame.K_a])
        self.rect.centerx+=self.direction.x*800*dt
        self.rect.centery-=400*dt
        if self.rect.bottom<0:
            self.kill()