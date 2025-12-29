import pygame

pygame.init()

# Vytvorenie okna
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Základné Pygame Okno - TITLE')

# Herná slučka
running = True
while running:
    for event in pygame.event.get(): # Spracovanie udalostí
        if event.type == pygame.QUIT: # Ukončenie hry pri zatvorení okna X
            running = False

    screen.fill((0, 0, 0))  # Vyplnenie obrazovky čiernou farbou

    pygame.draw.circle(screen, (255, 0, 0), (200, 150), 50)  # Nakreslenie červeného kruhu

    pygame.display.flip()    # Aktualizácia obrazovky

pygame.quit()
