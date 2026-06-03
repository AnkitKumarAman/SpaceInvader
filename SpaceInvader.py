import pygame
from random import randint
from star import Star
from player import Player
from meteor import Meteor
from AnimatedExplosion import AnimatedExplosion
from functions import collision
from functions import display_score
#general setup
pygame.init() #for initialising the game
screen_width=1280
screen_height=720
display_surface=pygame.display.set_mode((screen_width,screen_height))
# Dummy Sound Class to handle missing sound files
class DummySound:
    def play(self, loops=0, maxtime=0, fade_ms=0):
        return None
    def stop(self):
        pass
    def fadeout(self, time):
        pass
    def set_volume(self, value):
        pass
    def get_volume(self):
        return 0.0
    def get_num_channels(self):
        return 0
    def get_length(self):
        return 0.0
    def get_raw(self):
        return b""

def load_sound(path):
    try:
        return pygame.mixer.Sound(path)
    except Exception as e:
        print(f"Warning: Could not load sound {path}. Using fallback dummy sound. Error: {e}")
        return DummySound()

game_icon=pygame.image.load("Images/game_icon.png")
pygame.display.set_icon(game_icon)
pygame.display.set_caption("Space Invader") # sets the title of the game to be space invader
pygame.display.get_window_size()
running=True
clock=pygame.time.Clock()
#import
meteor_surf=pygame.image.load("Images/meteor.png").convert_alpha()
laser_surf=pygame.image.load("Images/laser.png").convert_alpha()
star_surf=pygame.image.load("Images/star.png").convert_alpha()
font=pygame.font.Font("Rustic_Barn.ttf",40) #(font style,size)
explosion_frames=[]
for i in range(20):
    image_path=f"explosion/explosion/{i}.png"
    try:
        image=pygame.image.load(image_path).convert_alpha()
        explosion_frames.append(image)
    except pygame.error as e:
        print(f"Could not load image {image_path}:{e}") 
laser_sound=load_sound("Sound/laser.wav")
laser_sound.set_volume(0.5)
laser_sound_rapid_fire=load_sound("Sound/rapid_fire_sound.wav")
explosion_sound=load_sound("Sound/explosion.wav")
game_over_sound=load_sound("Sound/game_over.wav")
game_music=load_sound("Sound/game_music.wav")
game_music.set_volume(0.3)
game_music.play(loops=-1) #will play the music infinetely,as long as the code runs
#Sprites
all_sprites=pygame.sprite.Group()
meteor_sprites=pygame.sprite.Group()
laser_sprites=pygame.sprite.Group()
for i in range (30):
    Star(all_sprites,star_surf,screen_width-100,screen_height-100) #the all sprites is a group and star_surf is a surface of the star
player=Player(all_sprites,screen_width,screen_height,laser_surf,laser_sound,all_sprites,laser_sprites,"rapid_fire",laser_sound_rapid_fire)
#custom events (meteor events)
meteor_events=pygame.event.custom_type()
pygame.time.set_timer(meteor_events,500) #here its 500 miliseconds (1/2 second)
while running: 
    dt= clock.tick(300)/1000
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==meteor_events:
            x,y=randint(0,screen_width),randint(-200,-100)
            Meteor(meteor_surf,(x,y),(all_sprites,meteor_sprites))
    display_surface.fill("#3a2e2f")
    all_sprites.update(dt)
    collision(player,meteor_sprites,game_over_sound,laser_sprites,AnimatedExplosion,explosion_frames,all_sprites,explosion_sound)
    #drawing the game
    display_surface.blit(player.image,player.rect)
    display_score(font,screen_width,screen_height,display_surface)
    all_sprites.draw(display_surface)
    pygame.display.update() #pygame.diplay.flip() is also pretty much same
pygame.quit()  #opposite of pygame.init() , deinitilises everything