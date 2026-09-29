# Space Shooter - Survival Game

import pygame

# FUNCTIONS

# UPDATE PLAYER FUNCTION 
def update_player(player, position, speed, dt, screen_width):

    # Checking which keyboard keys are being held down/pressed
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        position.x -= speed * dt

    if keys[pygame.K_RIGHT]:
        position.x += speed * dt


    position.x = max(
        0, 
        min(position.x, screen_width - player.width)
    )

    player.x = round(position.x)



# RENDERING FUNCTION FOR GRAPHICS ON SCREEN
def draw_game(screen, player, player_image, bullets):
    screen.fill((10, 10, 25))

    screen.blit(player_image, player)

    for bullet in bullets:
        pygame.draw.rect(
            screen,
            (100, 220, 255),
            bullet
        )

    pygame.display.flip()



def create_bullet(player, width, height):
    bullet = pygame.Rect(
        0,
        0,
        width,
        height
    )

    bullet.midbottom = player.midtop

    return bullet 



def update_bullets(bullets, speed, dt):
    for bullet in bullets:
        bullet.y -= speed * dt

    bullets[:] = [
        bullet
        for bullet in bullets
        if bullet.bottom >= 0
    ]




# INITIALIZATION

pygame.init()

# CONSTANTS
# Game Window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

# Player Dimensions
PLAYER_WIDTH = 70  
PLAYER_HEIGHT = 40  

# Bullet Settings
BULLET_WIDTH = 6
BULLET_HEIGHT = 20
BULLET_SPEED = 700

 
# SCREEN
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Survival Game: Space Shooter!")


# Player starting coordinates 
player_x = SCREEN_WIDTH // 2   
player_y = SCREEN_HEIGHT - 80 

# CREATING PLAYER
player = pygame.Rect(
    player_x, 
    player_y, 
    PLAYER_WIDTH, 
    PLAYER_HEIGHT
)


# PLAYER IMAGE - LOAD FIGHTER JET PNG FOR PLAYER
player_image = pygame.image.load(
    "assets/images/player_jet.png"
).convert_alpha()

player_image = pygame.transform.smoothscale(
    player_image,
    (PLAYER_WIDTH, PLAYER_HEIGHT)
)


player_position = pygame.Vector2(player.x, player.y)


# CLOCK
# Create the Clock object for game
clock = pygame.time.Clock()

FPS = 60
PLAYER_SPEED = 400   # player travels 400 pixels per second 

bullets = [] 

running = True

while running:

    # calculate delta time: elapsed time btwn two frames
    dt = clock.tick(FPS) / 1000

    # EVENTS
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(
                    create_bullet(
                        player,
                        BULLET_WIDTH,
                        BULLET_HEIGHT
                    )
                )


    # UPDATE
    # calling update_player function to update player 
    update_player(
        player, 
        player_position,
        PLAYER_SPEED, 
        dt, 
        SCREEN_WIDTH
    )

    update_bullets(
        bullets,
        BULLET_SPEED,
        dt
    )

    # RENDER
    draw_game(
        screen, 
        player, 
        player_image,
        bullets
    )


    
pygame.quit()






