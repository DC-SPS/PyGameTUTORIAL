import pygame
import sys

pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4-Way Parallax Scrolling")

clock = pygame.time.Clock()

# Načítaj obrázky
def load_and_scale(path):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (WIDTH, HEIGHT))

bg_far = load_and_scale("03_BG_PARALLAX/img/bg_far.png")
bg_mid = load_and_scale("03_BG_PARALLAX/img/bg_mid.png")
bg_close = load_and_scale("03_BG_PARALLAX/img/bg_close.png")

# Pozície X a Y pre každú vrstvu
pos = {
    "far":   {"x": 0, "y": 0, "speed": 1},
    "mid":   {"x": 0, "y": 0, "speed": 5},
    "close": {"x": 0, "y": 0, "speed": 10}
}

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    keys = pygame.key.get_pressed()
    
    # Reset smerov pre tento snímok
    dx, dy = 0, 0
    
    if keys[pygame.K_LEFT]:  dx = 1
    if keys[pygame.K_RIGHT]: dx = -1
    if keys[pygame.K_UP]:    dy = 1
    if keys[pygame.K_DOWN]:  dy = -1

    # Aktualizácia pozícií pre všetky vrstvy
    for layer in pos.values():
        layer["x"] += dx * layer["speed"]
        layer["y"] += dy * layer["speed"]

        # Nekonečné opakovanie X
        if layer["x"] <= -WIDTH: layer["x"] = 0
        if layer["x"] >= WIDTH:  layer["x"] = 0
        
        # Nekonečné opakovanie Y
        if layer["y"] <= -HEIGHT: layer["y"] = 0
        if layer["y"] >= HEIGHT:  layer["y"] = 0

    screen.fill((0, 0, 0))

    # Vykreslenie vrstiev (každá sa kreslí 4x, aby pokryla rohy pri diagonálnom pohybe)
    for img, p in [(bg_far, pos["far"]), (bg_mid, pos["mid"]), (bg_close, pos["close"])]:
        x, y = p["x"], p["y"]
        
        # Hlavný obrázok
        screen.blit(img, (x, y))
        
        # Horizontálne a vertikálne kópie pre plynulý prechod
        # (Vykresľujeme mriežku 2x2 pre každú vrstvu)
        offsetX = WIDTH if x < 0 else -WIDTH
        offsetY = HEIGHT if y < 0 else -HEIGHT
        
        screen.blit(img, (x + offsetX, y))          # Vedľa
        screen.blit(img, (x, y + offsetY))          # Nad alebo pod
        screen.blit(img, (x + offsetX, y + offsetY)) # Diagonálne

    pygame.display.flip()

pygame.quit()
sys.exit()