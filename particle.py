import pygame

class Particle:

    def __init__(self, x, y, velocity_x, velocity_y, lifetime, size):
        self.position = pygame.Vector2(x, y)

        self.velocity = pygame.Vector2(velocity_x, velocity_y)

        self.lifetime = lifetime
        self.size = size

    def update(self, dt):
        self.position += self.velocity * dt

        self.lifetime -= dt

    def draw(self, screen):
        pygame.draw.circle(
            screen, 
            (255, 180, 60),
            (
                round(self.position.x),
                round(self.position.y)
            ),
            self.size
        )

    def is_dead(self):
        return self.lifetime <= 0