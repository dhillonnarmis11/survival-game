# Space Shooter - Survival Game

import pygame
import random

from enemy import Enemy
from player import Player

# FUNCTIONS



# RENDERING FUNCTION FOR GRAPHICS ON SCREEN
def draw_game(screen, player, bullets, enemies, score, player_health, score_font):
    screen.fill((10, 10, 25))

    player.draw(screen)

    for bullet in bullets:
        pygame.draw.rect(
            screen,
            (100, 220, 255),
            bullet
        )

    for enemy in enemies:
        enemy.draw(screen) 

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

    screen.blit(
        score_surface,
        (20, 20)
    )

    screen.blit(
        health_surface,
        (20, 60) 
    )



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



def create_enemy(screen_width, enemy_width, enemy_height, enemy_speed):
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
        enemy_speed
    )



def handle_collisions(bullets, enemies):
    enemies_destroyed = 0

    for bullet in bullets[:]:
        for enemy in enemies[:]:

            if bullet.colliderect(enemy.rect):
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

FPS = 60

# Player Dimensions
PLAYER_WIDTH = 70  
PLAYER_HEIGHT = 40  
PLAYER_SPEED = 400   # player travels 400 pixels per second 
PLAYER_STARTING_HEALTH = 3    

# Bullet Settings
BULLET_WIDTH = 6
BULLET_HEIGHT = 20
BULLET_SPEED = 700

# Enemies
ENEMY_WIDTH = 60
ENEMY_HEIGHT = 40
ENEMY_SPEED = 150
ENEMY_SPAWN_TIME = 1.0


 
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


# CLOCK
# Create the Clock object for game
clock = pygame.time.Clock()


enemy_spawn_timer = 0.0

bullets = [] 

enemies = []

score = 0

player_health = PLAYER_STARTING_HEALTH 


running = True
game_over = False


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

            # shoot only while game is active
            if event.key == pygame.K_SPACE and not game_over:
                bullets.append(
                    create_bullet(
                        player,
                        BULLET_WIDTH,
                        BULLET_HEIGHT
                    )
                )

            # restart after game over
            if event.key == pygame.K_r and game_over:

                score = 0
                player_health = PLAYER_STARTING_HEALTH

                bullets.clear()
                enemies.clear()

                enemy_spawn_timer = 0.0

                # reset player to center
                player.position.x = (
                    SCREEN_WIDTH - player.rect.width
                ) / 2

                player.rect.x = round(player.position.x)

                game_over = False


    # UPDATE GAME
    # only update gameplay if we are not currently on game over screen
    if not game_over:

        # enemy spawn timer
        enemy_spawn_timer += dt 


        # SPAWN ENEMIES - spawn a new enemy when timer expires
        if enemy_spawn_timer >= ENEMY_SPAWN_TIME:
                enemies.append(
                    create_enemy(
                        SCREEN_WIDTH,
                        ENEMY_WIDTH,
                        ENEMY_HEIGHT,
                        ENEMY_SPEED
                    )
                )
        
                enemy_spawn_timer = 0.0


        # UPDATE

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

        # update all enemies
        for enemy in enemies:
            enemy.update(dt)

        # check collisions
        score += handle_collisions(
            bullets,
            enemies 
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

        # game over
        if player_health == 0:
            game_over = True

        # remove enemies that have gone below the screen 
        enemies[:] = [
            enemy 
            for enemy in enemies 
            if enemy.rect.top <= SCREEN_HEIGHT
        ]

    
    # RENDER
    # draw normal game
    draw_game(
        screen, 
        player,
        bullets,
        enemies,
        score,
        player_health,
        score_font
    )

    # draw game over text on top pf game
    if game_over:
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






