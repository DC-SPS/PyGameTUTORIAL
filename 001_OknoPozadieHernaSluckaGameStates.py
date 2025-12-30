import pygame
import sys

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60

# Nastavenie farieb
bg = (0, 0, 0)  # Čierna farba pozadia
player_color = (255, 0, 0)  # Červená farba hráča

   
class GaemeObject(pygame.sprite.Sprite):
    def __init__(self, x, y, color=player_color):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Player(GaemeObject):
    def __init__(self, x, y):
        super().__init__(x, y)
        # Ďalšie inicializácie hráča
        self.speed = 5  # Rýchlosť pohybu hráča

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

    def draw(self, screen):
            screen.blit(self.image, self.rect)

def handleImput():
    if pygame.key.get_pressed() == pygame.K_UP:
        pass  # Spracovanie stlačenia klávesu
    if pygame.key.get_pressed() == pygame.K_DOWN:
        pass  # Spracovanie stlačenia klávesu
    player.update()

def updateGameObjects(screen):
    screen.fill(bg)  # Vyplnenie obrazovky červenou farbou
    # Aktualizácia a vykreslenie herných objektov
    screen.blit(pygame.font.SysFont('Arial', 30).render('Základná herná slučka', True, (255, 255, 255)), (50, 50))
    player.draw(screen)
#    pygame.draw.rect(screen, player_color, (200, 150, 50, 50))  # Nakreslenie červeného štvorca

class Game:
    def __init__(self):
        # Vytvorenie okna
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('ákladná herná slučka - GAMESTATE')

        pygame.init()
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)  # Nastavenie snímkovej frekvencie

            for event in pygame.event.get(): # Spracovanie udalostí
                if event.type == pygame.QUIT: # Ukončenie hry pri zatvorení okna X
                    running = False

            handleImput()  # Funkcia na spracovanie vstupu
            updateGameObjects(self.screen)  # Funkcia na aktualizáciu herných objektov

            pygame.display.flip()    # Aktualizácia obrazovky

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  
    game = Game()
    game.run()