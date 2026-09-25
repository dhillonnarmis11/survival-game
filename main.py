# Space Shooter - Survival Game

import pygame

pygame.init()

# Game Window

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Player Dimensions and starting coordinates
PLAYER_WIDTH = 70  
PLAYER_HEIGHT = 40  
player_x = SCREEN_WIDTH // 2   
player_y = SCREEN_HEIGHT - 80  

player = pygame.Rect(
    player_x,
    player_y,
    PLAYER_WIDTH,
    PLAYER_HEIGHT
)



screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Survival Game: Space Shooter!")

# Create the Clock object for game
clock = pygame.time.Clock()

FPS = 60
PLAYER_SPEED = 400   # player travels 400 pixels per second 


running = True

while running:

    # calculate delta time: elapsed time btwn two frames
    dt = clock.tick(FPS) / 1000


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((10, 10, 25))

    pygame.draw.rect(screen, (80, 180, 255), player)


    # Checking which keyboard keys are being held down/pressed
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= PLAYER_SPEED * dt

    if keys[pygame.K_RIGHT]:
        player.x += PLAYER_SPEED * dt


    # make sure player stays within the screen
    if player.left < 0:  # make sure left edge (player.left) of player isn't out of screen
        player.left = 0

    if player.right > SCREEN_WIDTH:   # make sure right edge (player.right) of player isn't out of screen
        player.right = SCREEN_WIDTH


    pygame.display.flip() 


pygame.quit()






