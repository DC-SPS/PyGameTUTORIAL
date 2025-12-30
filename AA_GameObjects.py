
import pygame
import random

player_color = (255, 0, 0)  # Červená farba hráča

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, color=player_color):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        # Ďalšie inicializácie hráča
        self.speed = 5  # Rýchlosť pohybu hráča

    def handle_input(self, keys):
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

    def update(self, enemy):
        if self.rect.colliderect(enemy.rect):  # Príklad kolízie s nepriateľom
            print("Kolízia s nepriateľom!")

    def draw(self, screen):
            screen.blit(self.image, self.rect)

class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, color=(0, 0, 255))  # Modrá farba nepriateľa
        # Ďalšie inicializácie nepriateľa
        self.speed = random.randint(1, 3)  # Náhodná rýchlosť nepriateľa

    def update(self):
        self.rect.y += self.speed  # Pohyb nepriateľa nadol
        if self.rect.top > 800:  # Ak nepriateľ vyjde z obrazovky
            self.rect.bottom = 0  # Presuň ho späť na vrch obrazovky
            self.rect.x = random.randint(0, 600 - self.rect.width)  # Náhodná pozícia na osi X

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class HUD:
    def __init__(self):
        # Inicializácia HUD
        # screen.blit(pygame.font.SysFont('Arial', 25).render('Základná herná slučka', True, (255, 255, 255)), (50, 50))
        self.font = pygame.font.SysFont('Arial', 25)
        self.score = 0
        self.lives = 3
        self.level = 1
        import pygame
        import random

        player_color = (255, 0, 0)  # Červená farba hráča

        class GameObject(pygame.sprite.Sprite):
            def __init__(self, x, y, color=player_color):
                super().__init__()
                self.image = pygame.Surface((50, 50))
                self.image.fill(color)
                self.rect = self.image.get_rect()
                self.rect.center = (x, y)

        class Player(GameObject):
            def __init__(self, x, y):
                super().__init__(x, y)
                self.speed = 5

            def handle_input(self, keys):
                if keys[pygame.K_UP]:
                    self.rect.y -= self.speed
                if keys[pygame.K_DOWN]:
                    self.rect.y += self.speed
                if keys[pygame.K_LEFT]:
                    self.rect.x -= self.speed
                if keys[pygame.K_RIGHT]:
                    self.rect.x += self.speed

            def update(self, enemy):
                if hasattr(enemy, 'rect') and self.rect.colliderect(enemy.rect):
                    print("Kolízia s nepriateľom!")

            def draw(self, screen):
                screen.blit(self.image, self.rect)

        class Enemy(GameObject):
            def __init__(self, x, y):
                super().__init__(x, y, color=(0, 0, 255))
                self.speed = random.randint(1, 3)

            def update(self):
                self.rect.y += self.speed
                if self.rect.top > 800:
                    self.rect.bottom = 0
                    self.rect.x = random.randint(0, 600 - self.rect.width)

            def draw(self, screen):
                screen.blit(self.image, self.rect)

        class HUD:
            def __init__(self):
                pygame.font.init()
                self.font = pygame.font.SysFont('Arial', 25)
                self.score = 0
                self.lives = 3
                self.level = 1
                self.draw_position = (10, 10)
                self.color = (255, 255, 255)
                self.text = f'Score: {self.score} Lives: {self.lives} Level: {self.level}'
                self.image = self.font.render(self.text, True, self.color)

            def update(self, screen):
                self.text = f'Score: {self.score} Lives: {self.lives} Level: {self.level}'
                self.image = self.font.render(self.text, True, self.color)
                screen.blit(self.image, self.draw_position)

            def draw(self, screen):
                screen.blit(self.image, self.draw_position)
