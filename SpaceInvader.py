import pygame
from random import randint
from star import Star
from player import Player
from meteor import Meteor
from AnimatedExplosion import AnimatedExplosion
import functions

#general setup
pygame.init() #for initialising the game
screen_width=1280
screen_height=720
display_surface=pygame.display.set_mode((screen_width,screen_height))
game_canvas=pygame.Surface((screen_width,screen_height))

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

#import assets
meteor_surf=pygame.image.load("Images/meteor.png").convert_alpha()
laser_surf=pygame.image.load("Images/laser.png").convert_alpha()
star_surf=pygame.image.load("Images/star.png").convert_alpha()
font=pygame.font.Font("Rustic_Barn.ttf",40) #(font style,size)
font_large=pygame.font.Font("Rustic_Barn.ttf",80)
font_small=pygame.font.Font("Rustic_Barn.ttf",25)

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
powerup_sound=load_sound("Sound/powerup.wav")
game_music=load_sound("Sound/game_music.wav")
game_music.set_volume(0.3)
game_music.play(loops=-1) #will play the music infinetely,as long as the code runs

#Sprites
all_sprites=pygame.sprite.Group()
meteor_sprites=pygame.sprite.Group()
laser_sprites=pygame.sprite.Group()
powerup_sprites=pygame.sprite.Group()

# Create depth-layered stars for parallax scrolling
for _ in range(10):
    Star(all_sprites, star_surf, screen_width, screen_height, depth=1)
for _ in range(15):
    Star(all_sprites, star_surf, screen_width, screen_height, depth=2)
for _ in range(15):
    Star(all_sprites, star_surf, screen_width, screen_height, depth=3)

player=Player(all_sprites,screen_width,screen_height,laser_surf,laser_sound,all_sprites,laser_sprites,"single_fire",laser_sound_rapid_fire)

#custom events (meteor events)
meteor_events=pygame.event.custom_type()
meteor_spawn_interval = 500
pygame.time.set_timer(meteor_events, meteor_spawn_interval) #here its 500 miliseconds (1/2 second)

# Game States
STATE_START = 0
STATE_PLAYING = 1
STATE_GAMEOVER = 2
game_state = STATE_START
current_level = 1

# Screenshake values
shake_intensity = 0
shake_duration = 0

def trigger_screenshake():
    global shake_intensity, shake_duration
    shake_intensity = 15
    shake_duration = 200  # 200 ms screen shake

def transition_to_gameover():
    global game_state
    game_state = STATE_GAMEOVER

def reset_game():
    global current_level, meteor_spawn_interval, game_state
    current_level = 1
    meteor_spawn_interval = 500
    pygame.time.set_timer(meteor_events, meteor_spawn_interval)
    functions.reset_game_state(player, meteor_sprites, laser_sprites, powerup_sprites, screen_width, screen_height)
    all_sprites.add(player)
    game_state = STATE_PLAYING

# Score accumulation timer (adds 10 points per second of survival)
score_timer = pygame.event.custom_type()
pygame.time.set_timer(score_timer, 100) # trigger every 100ms (0.1s)

def draw_hud(surf):
    # Level display
    lvl_text = font.render(f"LEVEL: {current_level}", True, (255, 255, 255))
    surf.blit(lvl_text, (20, 20))
    
    # Active weapon display
    mode_str = "RAPID" if player.laser_mode == "rapid_fire" else "SINGLE"
    mode_color = (243, 156, 18) if player.laser_mode == "rapid_fire" else (46, 204, 113)
    if not player.can_shoot and player.laser_mode == "rapid_fire":
        mode_str = "OVERHEAT"
        mode_color = (231, 76, 60)
    
    # Append active Triple Shot status if picked up
    if player.triple_shot_active:
        mode_str += " + TRIPLE"
        mode_color = (52, 152, 219)
        
    weapon_text = font_small.render(f"WEAPON: {mode_str}", True, mode_color)
    surf.blit(weapon_text, (20, 60))
    
    # Draw shield bar
    bar_width = 150
    bar_height = 20
    bar_x = screen_width - bar_width - 20
    bar_y = 20
    pygame.draw.rect(surf, (100, 100, 100), (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4), 2, 3)
    
    segment_width = bar_width // player.max_shield
    for i in range(player.shield):
        if player.shield == 3:
            hp_color = (46, 204, 113) # green
        elif player.shield == 2:
            hp_color = (241, 196, 15) # yellow
        else:
            hp_color = (231, 76, 60)  # red
        pygame.draw.rect(surf, hp_color, (bar_x + i * segment_width + 1, bar_y + 1, segment_width - 2, bar_height - 2))

    # Draw heat bar if in rapid fire mode
    if player.laser_mode == "rapid_fire":
        current_time = pygame.time.get_ticks()
        heat_val = 0
        if player.first_execution_time_rapid is not None:
            if player.can_shoot:
                heat_val = min(5000, current_time - player.first_execution_time_rapid)
            else:
                if player.last_execution_time_rapid is not None:
                    cooldown_elapsed = current_time - player.last_execution_time_rapid
                    heat_val = max(0, 5000 - cooldown_elapsed)
                else:
                    heat_val = 5000
        
        heat_bar_width = 150
        heat_bar_height = 10
        heat_bar_x = screen_width - heat_bar_width - 20
        heat_bar_y = 50
        
        # Label for heat
        heat_label = font_small.render("HEAT", True, (200, 200, 200))
        surf.blit(heat_label, (heat_bar_x - 65, heat_bar_y - 8))
        
        # Draw border
        pygame.draw.rect(surf, (100, 100, 100), (heat_bar_x - 1, heat_bar_y - 1, heat_bar_width + 2, heat_bar_height + 2), 1, 2)
        
        # Fill heat bar
        fill_width = int(heat_bar_width * (heat_val / 5000))
        fill_color = (231, 76, 60) if not player.can_shoot else (230, 126, 34)
        if fill_width > 0:
            pygame.draw.rect(surf, fill_color, (heat_bar_x, heat_bar_y, fill_width, heat_bar_height))

while running: 
    dt= clock.tick(300)/1000
    
    # Update screenshake timer
    if shake_duration > 0:
        shake_duration -= dt * 1000
        if shake_duration <= 0:
            shake_intensity = 0
            
    # Handle inputs/events
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
            
        if game_state == STATE_START:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()
                
        elif game_state == STATE_PLAYING:
            if event.type==meteor_events:
                x,y=randint(0,screen_width),randint(-200,-100)
                Meteor(meteor_surf,(x,y),(all_sprites,meteor_sprites), current_level)
            if event.type == score_timer:
                functions.score += 1 # 10 points per second
                
        elif game_state == STATE_GAMEOVER:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                elif event.key == pygame.K_q:
                    running = False

    # DRAW & UPDATE
    game_canvas.fill("#3a2e2f")
    
    if game_state == STATE_START:
        # Update background stars
        all_sprites.update(dt)
        # Remove laser and meteor updates in start screen
        for s in all_sprites:
            if not isinstance(s, Star) and not isinstance(s, Player):
                s.kill()
        all_sprites.draw(game_canvas)
        
        # Render title screen text
        title_surf = font_large.render("SPACE INVADER", True, (46, 204, 113))
        title_rect = title_surf.get_rect(center=(screen_width/2, screen_height/2 - 100))
        game_canvas.blit(title_surf, title_rect)
        
        # Blinking prompt text
        if (pygame.time.get_ticks() // 400) % 2 == 0:
            prompt_surf = font.render("PRESS SPACE TO PLAY", True, (241, 196, 15))
            prompt_rect = prompt_surf.get_rect(center=(screen_width/2, screen_height/2 + 50))
            game_canvas.blit(prompt_surf, prompt_rect)
            
        # Controls info
        ctrl_text1 = font_small.render("Move: Arrows / WASD  |  Shoot: Space", True, (200, 200, 200))
        ctrl_text2 = font_small.render("Weapon Modes: Q (Single Fire)  |  E (Rapid Fire)", True, (200, 200, 200))
        game_canvas.blit(ctrl_text1, ctrl_text1.get_rect(center=(screen_width/2, screen_height/2 + 150)))
        game_canvas.blit(ctrl_text2, ctrl_text2.get_rect(center=(screen_width/2, screen_height/2 + 190)))
        
        # Show lifetime highscore
        hi_score = functions.current_high_score
        hi_text = font.render(f"HIGH SCORE: {hi_score}", True, (255, 223, 0))
        game_canvas.blit(hi_text, hi_text.get_rect(center=(screen_width/2, screen_height - 80)))
        
    elif game_state == STATE_PLAYING:
        # Scale difficulty every 500 points
        new_level = 1 + (functions.score // 500)
        if new_level != current_level:
            current_level = new_level
            meteor_spawn_interval = max(150, 500 - (current_level - 1) * 50)
            pygame.time.set_timer(meteor_events, meteor_spawn_interval)
            
        all_sprites.update(dt)
        functions.collision(
            player, meteor_sprites, laser_sprites, powerup_sprites,
            AnimatedExplosion, explosion_frames, all_sprites,
            explosion_sound, game_over_sound, powerup_sound,
            trigger_screenshake, transition_to_gameover
        )
        
        # Drawing
        all_sprites.draw(game_canvas)
        functions.display_score(font,screen_width,screen_height,game_canvas)
        draw_hud(game_canvas)
        
    elif game_state == STATE_GAMEOVER:
        # Draw background elements frozen
        all_sprites.draw(game_canvas)
        functions.display_score(font,screen_width,screen_height,game_canvas)
        
        # Semi-transparent overlay
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        game_canvas.blit(overlay, (0, 0))
        
        # Render Game Over text
        go_surf = font_large.render("GAME OVER", True, (231, 76, 60))
        go_rect = go_surf.get_rect(center=(screen_width/2, screen_height/2 - 100))
        game_canvas.blit(go_surf, go_rect)
        
        # Final Score
        score_surf = font.render(f"FINAL SCORE: {functions.score}", True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(screen_width/2, screen_height/2))
        game_canvas.blit(score_surf, score_rect)
        
        # Prompts
        prompt_surf = font.render("PRESS R TO REPLAY  |  Q TO QUIT", True, (241, 196, 15))
        prompt_rect = prompt_surf.get_rect(center=(screen_width/2, screen_height/2 + 100))
        game_canvas.blit(prompt_surf, prompt_rect)

    # Blit game_canvas onto display surface with screenshake offset
    offset_x = 0
    offset_y = 0
    if shake_duration > 0:
        offset_x = randint(-int(shake_intensity), int(shake_intensity))
        offset_y = randint(-int(shake_intensity), int(shake_intensity))
        
    display_surface.fill((0,0,0))
    display_surface.blit(game_canvas, (offset_x, offset_y))
    pygame.display.update()
    
pygame.quit()  #opposite of pygame.init() , deinitilises everything