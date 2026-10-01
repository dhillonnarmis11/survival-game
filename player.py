import pygame

class Player:

    def __init__(
            self,
            x,
            y,
            width,
            height,
            speed,
            image
    ):
        self.image = image
        self.speed = speed

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        self.position = pygame.Vector2(
            x,
            y
        )


    def update(self, dt, screen_width):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.position.x -= self.speed * dt

        if keys[pygame.K_RIGHT]:
            self.position.x += self.speed * dt

        self.position.x = max(
            0,
            min(
                self.position.x,
                screen_width - self.rect.width
            )
        )

        self.rect.x = round(self.position.x)   


    def draw(self, screen):
        screen.blit(
            self.image,
            self.rect
        )

        

        

            
        