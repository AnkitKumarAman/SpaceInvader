import pygame
from random import randint,uniform
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self,groups,screen_width,screen_height,laser_surf,laser_sound,all_sprites,laser_sprites,laser_mode,laser_sound_rapid_fire):
        super().__init__(groups)
        self.first_execution_time_rapid=None
        self.last_execution_time_rapid=None
        self.first_execution_time_single=None
        self.image=pygame.image.load("Images/player.png").convert_alpha()
        self.original_image=self.image
        self.rect=self.image.get_frect(center=(screen_width/2,screen_height/2))
        self.direction=pygame.Vector2()
        self.speed=300
        self.can_shoot=True
        self.laser_shoot_time=0
        self.cooldown_duration=4000
        self.screen_width=screen_width
        self.screen_height=screen_height
        self.laser_surf=laser_surf
        self.laser_sound=laser_sound
        self.all_sprites=all_sprites
        self.laser_sprites=laser_sprites
        self.laser_mode=laser_mode
        self.laser_sound_rapid_fire=laser_sound_rapid_fire
        
        # Shield and Invincibility
        self.max_shield=3
        self.shield=3
        self.invincible=False
        self.invincible_duration=1500 # 1.5 seconds
        self.invincible_time=0
        
        # Power-ups
        self.triple_shot_active=False
        self.triple_shot_duration=8000 # 8 seconds
        self.triple_shot_time=0
        
        self.mask=pygame.mask.from_surface(self.image)

    def laser_timer(self):
        if not self.can_shoot:  
            current_time=pygame.time.get_ticks() 
            if current_time-self.laser_shoot_time>=self.cooldown_duration:
                self.can_shoot=True

    def laser_timer_rapid(self):
        if not self.can_shoot:
            current_time=pygame.time.get_ticks()
            if current_time-self.last_execution_time>=5000:
                self.can_shoot=True

    def update(self,dt):
        keys=pygame.key.get_pressed()
        
        # Support both Arrow keys and A/D keys for horizontal movement
        dx = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        if dx == 0:
            dx = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
            
        # Support both Arrow keys and W/S keys for vertical movement
        dy = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        if dy == 0:
            dy = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
            
        self.direction.x = dx
        self.direction.y = dy
        self.direction=self.direction.normalize() if self.direction else self.direction
        self.rect.center+=self.direction*self.speed*dt
        
        # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height

        # Spawn thruster particles
        for _ in range(2):
            EngineParticle((self.rect.centerx, self.rect.bottom - 5), self.all_sprites)
            
        # Handle invincibility frames & blinking
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_time >= self.invincible_duration:
                self.invincible = False
                self.image.set_alpha(255)
            else:
                alpha = 100 if (current_time // 100) % 2 == 0 else 255
                self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

        # Handle Triple-Shot duration
        if self.triple_shot_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.triple_shot_time >= self.triple_shot_duration:
                self.triple_shot_active = False

        keys1=pygame.key.get_just_pressed()
        
        # Single Fire shoots once per tap, Rapid Fire shoots continuously while Space is held down
        if self.laser_mode == "single_fire":
            shoot_pressed = keys1[pygame.K_SPACE]
        else:
            shoot_pressed = keys[pygame.K_SPACE]
            
        if shoot_pressed and self.can_shoot==True:
            current_time=pygame.time.get_ticks()
            if self.laser_mode=="single_fire":
                if self.triple_shot_active:
                    Laser(self.laser_surf,self.rect.midtop,(self.all_sprites,self.laser_sprites), 0)
                    Laser(self.laser_surf,self.rect.midtop,(self.all_sprites,self.laser_sprites), -1)
                    Laser(self.laser_surf,self.rect.midtop,(self.all_sprites,self.laser_sprites), 1)
                else:
                    Laser(self.laser_surf,self.rect.midtop,(self.all_sprites,self.laser_sprites), 0)
                self.can_shoot=False
                self.laser_shoot_time=current_time
                self.first_execution_time_single=current_time
                self.laser_sound.play()
            elif self.laser_mode=="rapid_fire":
                # Enforce a 120ms delay between consecutive shots in rapid mode
                if current_time - self.laser_shoot_time >= 120:
                    if self.triple_shot_active:
                        Laser(self.laser_surf,self.rect.midtop,(self.all_sprites,self.laser_sprites), 0)
                        Laser(self.laser_surf,self.rect.midtop,(self.all_sprites,self.laser_sprites), -1)
                        Laser(self.laser_surf,self.rect.midtop,(self.all_sprites,self.laser_sprites), 1)
                    else:
                        Laser(self.laser_surf,self.rect.midtop,(self.all_sprites,self.laser_sprites), 0)
                    self.laser_shoot_time=current_time
                    if self.first_execution_time_rapid is None:
                        self.first_execution_time_rapid=current_time
                    if current_time-self.first_execution_time_rapid>=5000:
                        if self.last_execution_time_rapid is None:
                            self.last_execution_time_rapid=current_time
                        self.can_shoot=False
                    self.laser_sound_rapid_fire.play()
        if self.laser_mode=="rapid_fire" and self.can_shoot==False:
            current_time=pygame.time.get_ticks()
            if current_time-self.last_execution_time_rapid>=5000:
                self.can_shoot=True
                self.first_execution_time_rapid=None
                self.last_execution_time_rapid=None
        if self.laser_mode=="single_fire" and self.can_shoot==False:
            current_time=pygame.time.get_ticks()
            if self.first_execution_time_single is None:
                self.first_execution_time_single=pygame.time.get_ticks()
            if current_time-self.first_execution_time_single>=400:
                self.can_shoot=True
                self.first_execution_time_single=None
        if keys1[pygame.K_e] and self.laser_mode=="single_fire":
            self.laser_mode="rapid_fire"
            print(self.laser_mode)
        if keys1[pygame.K_q] and self.laser_mode=="rapid_fire":
            self.laser_mode="single_fire"
            print(self.laser_mode)

class EngineParticle(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        size = randint(4, 8)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        # Random fiery color: red/orange/yellow
        color = (randint(230, 255), randint(80, 180), 0)
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect(center=pos)
        self.velocity = pygame.Vector2(uniform(-0.5, 0.5), uniform(1.0, 2.0))
        self.speed = randint(80, 150)
        self.life = 255.0
        
    def update(self, dt):
        self.rect.center += self.velocity * self.speed * dt
        self.life -= 800 * dt  # decay over ~0.3s
        if self.life <= 0:
            self.kill()
        else:
            self.image.set_alpha(int(self.life))