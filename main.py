# Space Shooter - Survival Game

import pygame
import random

from enemy import Enemy
from player import Player
from particle import Particle


# FUNCTIONS
# RENDERING FUNCTION FOR GRAPHICS ON SCREEN
def draw_game(
        screen, 
        player, 
        bullets, 
        enemies, 
        particles,
        stars, 
        score, 
        player_health, 
        level, 
        score_font
    ):

    screen.fill((10, 10, 25))

    draw_stars(
        screen,
        stars
    )

    player.draw(screen)

    for bullet in bullets:
        pygame.draw.rect(
            screen,
            (100, 220, 255),
            bullet
        )

    for enemy in enemies:
        enemy.draw(screen) 

    for particle in particles:
        particle.draw(screen)


    score_surface = score_font.render(
        f"Score: {score}",
        True,
        (255, 255, 255)
    )

    health_surface = score_font.render(
        f"Health: {player_health}",
        True,
        (255, 255, 255)
    )

    level_surface = score_font.render(
        f"Level: {level}",
        True,
        (255, 255, 255)
    )

    screen.blit(
        score_surface,
        (20, 20)
    )

    screen.blit(
        health_surface,
        (20, 60) 
    )

    screen.blit(
        level_surface,
        (20, 100)
    )



def draw_menu(screen, font, screen_width, screen_height):

    title_surface = font.render(
        "SURVIVAL GAME",
        True,
        (255, 255, 255)
    )

    start_surface = font.render(
        "Press ENTER to Start",
        True,
        (255, 255, 255)
    )

    title_rect = title_surface.get_rect(
        center=(
            screen_width // 2,
            screen_height // 2 - 50
        )
    )

    start_rect = start_surface.get_rect(
        center=(
            screen_width // 2,
            screen_height // 2 + 30
        )
    )

    screen.blit(title_surface, title_rect)
    screen.blit(start_surface, start_rect)



def create_bullet(player, width, height):
    bullet = pygame.Rect(
        0,
        0,
        width,
        height
    )

    bullet.midbottom = player.rect.midtop

    return bullet 



def update_bullets(bullets, speed, dt):
    for bullet in bullets:
        bullet.y -= speed * dt

    bullets[:] = [
        bullet
        for bullet in bullets
        if bullet.bottom >= 0
    ]



def create_enemy(screen_width, enemy_width, enemy_height, enemy_speed, enemy_image):
    x = random.randint(
        0,
        screen_width - enemy_width
    )

    y = -enemy_height 

    return Enemy(
        x,
        y,
        enemy_width,
        enemy_height,
        enemy_speed,
        enemy_image
    )



def handle_collisions(bullets, enemies, particles, explosion_sound):
    enemies_destroyed = 0

    for bullet in bullets[:]:
        for enemy in enemies[:]:

            if bullet.colliderect(enemy.rect):

                create_explosion(
                    enemy.rect.centerx,
                    enemy.rect.centery,
                    particles
                )

                explosion_sound.play()

                bullets.remove(bullet)
                enemies.remove(enemy)

                enemies_destroyed += 1

                break

    return enemies_destroyed



def handle_player_collisions(player, enemies):
    hits = 0

    for enemy in enemies[:]:
        if player.rect.colliderect(enemy.rect):
            enemies.remove(enemy)
            hits += 1

    return hits 



def remove_escaped_enemies(enemies, screen_height):
    escaped = 0

    for enemy in enemies[:]:
        if enemy.rect.top > screen_height:
            enemies.remove(enemy)
            escaped += 1

    return escaped



def create_stars(count, screen_width, screen_height):
    stars = []

    for _ in range(count):
        star = {
            "x": random.randint(0, screen_width),
            "y": random.randint(0, screen_height),
            "speed": random.randint(50, 200),
            "size": random.randint(1, 3)
        }

        stars.append(star)

    return stars



def update_stars(stars, dt, screen_width, screen_height):
    for star in stars:

        star["y"] += star["speed"] * dt

        if star["y"] > screen_height:
            star["y"] = 0
            star["x"] = random.randint(0, screen_width)



def get_difficulty(score):
    enemy_speed = min(
        ENEMY_SPEED + score * SPEED_INCREASE_PER_POINT,
        MAX_ENEMY_SPEED
    )

    spawn_time = max(
        ENEMY_SPAWN_TIME - score * SPAWN_DECREASE_PER_POINT,
        MIN_ENEMY_SPAWN_TIME
    )

    return enemy_speed, spawn_time



def get_level(score):
    return score // 10 + 1


def draw_stars(screen, stars):
    for star in stars:
        pygame.draw.circle(
            screen,
            (200, 200, 220),
            (int(star["x"]), int(star["y"])),
            star["size"]
        )



def create_explosion(x, y, particles):
    for _ in range(20):

        velocity_x = random.randint(-200, 200)
        velocity_y = random.randint(-200, 200)

        lifetime = random.uniform(0.3, 0.7)

        size = random.randint(2, 5)

        particle = Particle(
            x,
            y,
            velocity_x,
            velocity_y,
            lifetime,
            size
        )

        particles.append(particle)




def draw_game_over(screen, font, score, screen_width, screen_height):
    game_over_surface = font.render(
        "GAME OVER!",
        True,
        (255, 255, 255)
    )

    score_surface = font.render(
        f"Final Score: {score}",
        True,
        (255, 255, 255)
    )

    restart_surface = font.render(
        "Press R to Restart",
        True,
        (255, 255, 255)
    )

    game_over_rect = game_over_surface.get_rect(
        center=(
            screen_width // 2,
            screen_height // 2 - 50
        )
    )

    score_rect = score_surface.get_rect(
        center=(
            screen_width // 2,
            screen_height // 2
        )
    )

    restart_rect = restart_surface.get_rect(
        center=(
            screen_width // 2,
            screen_height // 2 + 50
        )
    )

    screen.blit(game_over_surface, game_over_rect)
    screen.blit(score_surface, score_rect)
    screen.blit(restart_surface, restart_rect)



# INITIALIZATION

pygame.init()

# CONSTANTS
# Game Window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"

STAR_COUNT = 140

FPS = 60

# Player Dimensions
PLAYER_WIDTH = 80  
PLAYER_HEIGHT = 50  
PLAYER_SPEED = 400   # player travels 400 pixels per second 
PLAYER_STARTING_HEALTH = 3    

# Bullet Settings
BULLET_WIDTH = 6
BULLET_HEIGHT = 20
BULLET_SPEED = 700
FIRE_COOLDOWN = 0.20

# Enemies
ENEMY_WIDTH = 70
ENEMY_HEIGHT = 50
ENEMY_SPEED = 150
ENEMY_SPAWN_TIME = 1.0
MAX_ENEMY_SPEED = 350
MIN_ENEMY_SPAWN_TIME = 0.35
SPEED_INCREASE_PER_POINT = 5
SPAWN_DECREASE_PER_POINT = 0.02


 
# SCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Survival Game: Space Shooter!")

# FONT
score_font = pygame.font.Font(None, 36)


# PLAYER IMAGE - LOAD FIGHTER JET PNG FOR PLAYER
player_image = pygame.image.load(
    "assets/images/player_jet.png"
).convert_alpha()

player_image = pygame.transform.smoothscale(
    player_image,
    (PLAYER_WIDTH, PLAYER_HEIGHT)
)

# ENEMY IMAGE
enemy_image = pygame.image.load(
    "assets/images/enemy_ship.png"
).convert_alpha()

enemy_image = pygame.transform.smoothscale(
    enemy_image,
    (ENEMY_WIDTH, ENEMY_HEIGHT)
)

# SOUNDS
laser_sound = pygame.mixer.Sound(
    "assets/sounds/laser.wav"
)

explosion_sound = pygame.mixer.Sound(
    "assets/sounds/explosion.wav"
)

laser_sound.set_volume(0.25)
explosion_sound.set_volume(0.40)



# PLAYER STARTING COORDINATES
player_x = SCREEN_WIDTH // 2   
player_y = SCREEN_HEIGHT - 80 


# CREATE PLAYER
player = Player(
    player_x,
    player_y,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_SPEED,
    player_image
)


# CREATE STARS
stars = create_stars(
    STAR_COUNT,
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)


# CLOCK
# Create the Clock object for game
clock = pygame.time.Clock()


enemy_spawn_timer = 0.0
fire_timer = 0.0

bullets = [] 
enemies = []
particles = []

score = 0

player_health = PLAYER_STARTING_HEALTH 

# is application open
running = True

# what part of game we're currently in
game_state = MENU


while running:

    # TIME
    # calculate delta time: elapsed time btwn two frames
    dt = clock.tick(FPS) / 1000

    # EVENTS
    for event in pygame.event.get():

        # close the game window
        if event.type == pygame.QUIT:
            running = False

        # handle key presses
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN and game_state == MENU:
                game_state = PLAYING

            # restart after game over
            if event.key == pygame.K_r and game_state == GAME_OVER:

                score = 0
                player_health = PLAYER_STARTING_HEALTH

                bullets.clear()
                enemies.clear()
                particles.clear()

                enemy_spawn_timer = 0.0
                fire_timer = FIRE_COOLDOWN 

                # reset player to center
                player.position.x = (
                    SCREEN_WIDTH - player.rect.width
                ) / 2

                player.rect.x = round(player.position.x)

                game_state = PLAYING


    # UPDATE GAME
    # only update gameplay if we are not currently on game over screen
    if game_state == PLAYING:

        # enemy spawn timer
        enemy_spawn_timer += dt 

        fire_timer += dt 

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and fire_timer >= FIRE_COOLDOWN:
            bullets.append(
                create_bullet(
                    player,
                    BULLET_WIDTH,
                    BULLET_HEIGHT
                )
            )
            laser_sound.play()
            fire_timer = 0.0


        current_enemy_speed, current_spawn_time = get_difficulty(
            score
        )

        # SPAWN ENEMIES - spawn a new enemy when timer expires
        if enemy_spawn_timer >= current_spawn_time:
                enemies.append(
                    create_enemy(
                        SCREEN_WIDTH,
                        ENEMY_WIDTH,
                        ENEMY_HEIGHT,
                        current_enemy_speed,
                        enemy_image
                    )
                )
        
                enemy_spawn_timer = 0.0


        # UPDATE

        update_stars(
            stars,
            dt,
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        )

        player.update(
            dt,
            SCREEN_WIDTH
        )

        # update bullets
        update_bullets(
            bullets,
            BULLET_SPEED,
            dt
        )


        # update all enemies/move enemies
        for enemy in enemies:
            enemy.update(dt)

        # particles update and remove dead particles
        for particle in particles:
            particle.update(dt)

        particles[:] = [
            particle
            for particle in particles
            if not particle.is_dead()
        ]


        # check collisions
        score += handle_collisions(
            bullets,
            enemies,
            particles,
            explosion_sound 
        )

        # player health
        hits = handle_player_collisions(
            player,
            enemies
        )

        player_health = max(
            0,
            player_health - hits
        )


        # ESCAPED ENEMIES
        # remove enemies that have gone below the screen 
        escaped_enemies = remove_escaped_enemies(
            enemies,
            SCREEN_HEIGHT
        )

        player_health = max(
            0,
            player_health - escaped_enemies
        )


        # game over
        if player_health == 0:
            game_state = GAME_OVER


    # LEVEL
    level = get_level(score)

    
    # RENDER
    # draw normal game
    draw_game(
        screen, 
        player,
        bullets,
        enemies,
        particles,
        stars,
        score,
        player_health,
        level,
        score_font
    )


    # draw game over text on top pf game
    if game_state == MENU:

        screen.fill((10, 10, 25))

        draw_stars(
            screen,
            stars
        )

        draw_menu(
            screen,
            score_font,
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        )


    elif game_state == PLAYING:

        draw_game(
            screen, 
            player,
            bullets,
            enemies,
            particles,
            stars,
            score,
            player_health,
            level,
            score_font
            )


    elif game_state == GAME_OVER:
        
        draw_game(
            screen, 
            player,
            bullets,
            enemies,
            particles,
            stars,
            score,
            player_health,
            level,
            score_font
            )

        draw_game_over(
            screen,
            score_font,
            score,
            SCREEN_WIDTH,
            SCREEN_HEIGHT
        )

    # show the completed frame
    pygame.display.flip()

    
pygame.quit()






