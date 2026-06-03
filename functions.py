import pygame
import time
import sys
import os
from random import random, choice, randint
from powerup import PowerUp
from debris import MeteorDebris

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
score = 0

def collision(player, meteor_sprites, laser_sprites, powerup_sprites, AnimatedExplosion, explosion_frames, all_sprites, explosion_sound, game_over_sound, powerup_sound, on_damage_callback, on_gameover_callback):
    global score, current_high_score
    
    # 1. Player vs Meteor collision (only if not invincible)
    if not player.invincible:
        collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask)
        if collision_sprites:
            # Spawn explosion at player position
            AnimatedExplosion(explosion_frames, player.rect.center, all_sprites)
            explosion_sound.play()
            
            # Reduce shield points
            player.shield -= 1
            on_damage_callback() # Trigger screen shake
            
            if player.shield <= 0:
                # Save high score
                if score > current_high_score:
                    current_high_score = score
                    save_high_score(score)
                game_over_sound.play()
                on_gameover_callback()
            else:
                # Set invincibility frames
                player.invincible = True
                player.invincible_time = pygame.time.get_ticks()
                
    # 2. Laser vs Meteor collision
    for laser in laser_sprites:
        meteor_hit = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if meteor_hit:
            laser.kill()
            for meteor in meteor_hit:
                AnimatedExplosion(explosion_frames, meteor.rect.center, all_sprites)
                explosion_sound.play()
                score += 50 # Add score for hitting meteor
                
                # Spawn meteor debris particles
                for _ in range(randint(8, 12)):
                    MeteorDebris(meteor.rect.center, all_sprites)
                
                # 15% drop rate for power-ups
                if random() < 0.15:
                    p_type = choice(['shield', 'triple_shot', 'rapid_boost'])
                    PowerUp(meteor.rect.center, p_type, (all_sprites, powerup_sprites))
                    
    # 3. Player vs Power-up collision
    collected_powerups = pygame.sprite.spritecollide(player, powerup_sprites, True, pygame.sprite.collide_mask)
    for powerup in collected_powerups:
        powerup_sound.play()
        if powerup.type == 'shield':
            player.shield = min(player.max_shield, player.shield + 1)
        elif powerup.type == 'triple_shot':
            player.triple_shot_active = True
            player.triple_shot_time = pygame.time.get_ticks()
        elif powerup.type == 'rapid_boost':
            player.can_shoot = True
            player.first_execution_time_rapid = None
            player.last_execution_time_rapid = None

def reset_game_state(player, meteor_sprites, laser_sprites, powerup_sprites, screen_width, screen_height):
    global score
    score = 0
    
    # Kill all current gameplay elements
    for m in list(meteor_sprites):
        m.kill()
    for l in list(laser_sprites):
        l.kill()
    for p in list(powerup_sprites):
        p.kill()
        
    # Reset player attributes
    player.rect.center = (screen_width / 2, screen_height / 2)
    player.shield = player.max_shield
    player.invincible = False
    player.triple_shot_active = False
    player.can_shoot = True
    player.first_execution_time_rapid = None
    player.last_execution_time_rapid = None
    player.first_execution_time_single = None
    player.laser_shoot_time = 0

# Cache high score font
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
    global score, current_high_score
    
    # Current score display
    text_surf=font.render(str(score),True,(0,254,0))
    text_rect=text_surf.get_frect(midbottom=(screen_width/2,screen_height-80))
    display_surface.blit(text_surf,text_rect)
    pygame.draw.rect(display_surface,(0,254,0),text_rect.inflate(20,20).move(0,-5),5,5)
    
    # High score display
    hi_score = max(score, current_high_score)
    hi_text = f"HIGH SCORE: {hi_score}"
    
    hi_font = get_high_score_font()
    hi_surf = hi_font.render(hi_text, True, (255, 223, 0)) # Vibrant gold
    hi_rect = hi_surf.get_frect(midbottom=(screen_width/2, screen_height-25))
    
    # Draw the text
    display_surface.blit(hi_surf, hi_rect)