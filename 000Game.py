import pygame
import sys

from AA_GameObjects import Player, Enemy, HUD

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60

# Nastavenie farieb
bg = (0, 0, 0)  # Čierna farba pozadia


def handle_input():
    keys = pygame.key.get_pressed()
    player.handle_input(keys)
    #enemy.handle_input(keys)  # Ak nepriateľ potrebuje spracovať vstup

def update_game_objects(screen):
    screen.fill(bg)  # Vyplnenie obrazovky červenou farbou
    # Aktualizácia a vykreslenie herných objektov
    screen.blit(pygame.font.SysFont('Arial', 25).render('Základná herná slučka', True, (255, 255, 255)), (50, 50))
    hud.update(screen)
    player.update(enemy)
    enemy.update()


def render_game_objects(screen):
    # Vykreslenie herných objektov na obrazovku
    hud.draw(screen)
    player.draw(screen)
    enemy.draw(screen)

class Game:
    def __init__(self):
        # Vytvorenie okna
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('ákladná herná slučka - GAMESTATE')

        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)  # Nastavenie snímkovej frekvencie

            for event in pygame.event.get(): # Spracovanie udalostí
                if event.type == pygame.QUIT: # Ukončenie hry pri zatvorení okna X
                    running = False

            handle_input()  # Funkcia na spracovanie vstupu
            update_game_objects(self.screen)  # Funkcia na aktualizáciu herných objektov
            render_game_objects(self.screen)  # Funkcia na vykreslenie herných objektov

            pygame.display.flip()    # Aktualizácia obrazovky

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  
    enemy = Enemy(100, 0)
    hud = HUD()
    game = Game()
    game.run()