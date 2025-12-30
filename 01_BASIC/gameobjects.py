import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sizeX, sizeY):
        super().__init__()
        self.speed = 5
        self.sizeX, self.sizeY = sizeX, sizeY
        self.score = 0
        self.lives = 3
        self.image = pygame.Surface((self.sizeX, self.sizeY))
        self.image.fill((0, 200, 255))
        self.rect = self.image.get_rect()
        # set initial position
        self.rect.topleft = (x, y)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        # Sprite images
        # player_image = pygame.image.load('player.png')
        # screen.blit(player_image, self.rect)