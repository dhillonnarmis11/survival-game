import pygame

class Enemy:
    def __init__(self, x, y, width, height, speed, image):

        self.image = image
        self.speed = speed 
         
        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.position = pygame.Vector2(x, y)
        

    def update(self, dt):
        self.position.y += self.speed * dt
        self.rect.y = round(self.position.y)

    def draw(self, screen):
        screen.blit(
            self.image, 
            self.rect
        )
        