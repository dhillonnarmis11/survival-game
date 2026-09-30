import pygame

class Enemy:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.position = pygame.Vector2(x, y)
        self.speed = speed 

    def update(self, dt):
        self.position.y += self.speed * dt
        self.rect.y = round(self.position.y)

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (220, 80, 100),
            self.rect
        )
        