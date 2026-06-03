import pygame
import time
import sys
import os

HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def save_high_score(score):
    try:
        with open(HIGH_SCORE_FILE, "w") as f:
            f.write(str(score))
    except Exception as e:
        print(f"Error saving high score: {e}")

# Load the initial high score when the module loads
current_high_score = load_high_score()

def collision(player,meteor_sprites,game_over_sound,laser_sprites,AnimatedExplosion,explosion_frames,all_sprites,explosion_sound):
    global running
    collision_sprites=pygame.sprite.spritecollide(player,meteor_sprites,True,pygame.sprite.collide_mask) #setting it to true means it kills the meteor_sprites
    if collision_sprites:
        # Check and save high score
        current_score = pygame.time.get_ticks() // 100
        global current_high_score
        if current_score > current_high_score:
            current_high_score = current_score
            save_high_score(current_score)
        
        game_over_sound.play()
        time.sleep(2)
        running=False
        pygame.quit()
        sys.exit()
    for laser in laser_sprites:
        meteor_hit=pygame.sprite.spritecollide(laser,meteor_sprites,True) #dont use mask when not needed , becauase its very hardware intensive
        if meteor_hit: 
            laser.kill()
            AnimatedExplosion(explosion_frames,laser.rect.midtop,all_sprites)
            explosion_sound.play()
            
# Cache the high score font to avoid loading it on every frame
high_score_font = None

def get_high_score_font():
    global high_score_font
    if high_score_font is None:
        try:
            high_score_font = pygame.font.Font("Rustic_Barn.ttf", 30)
        except Exception:
            high_score_font = pygame.font.SysFont("arial", 30)
    return high_score_font

def display_score(font,screen_width,screen_height,display_surface):
    current_time=pygame.time.get_ticks()//100
    
    # Current score display
    text_surf=font.render(str(current_time),True,(0,254,0))
    text_rect=text_surf.get_frect(midbottom=(screen_width/2,screen_height-80))
    display_surface.blit(text_surf,text_rect)
    pygame.draw.rect(display_surface,(0,254,0),text_rect.inflate(20,20).move(0,-5),5,5)
    
    # High score display (below current score, smaller size 30)
    global current_high_score
    hi_score = max(current_time, current_high_score)
    hi_text = f"HIGH SCORE: {hi_score}"
    
    hi_font = get_high_score_font()
    hi_surf = hi_font.render(hi_text, True, (255, 223, 0)) # Vibrant gold
    hi_rect = hi_surf.get_frect(midbottom=(screen_width/2, screen_height-25))
    
    # Draw the text
    display_surface.blit(hi_surf, hi_rect)