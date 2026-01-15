import pygame
import pytmx  # Knižnica na načítanie Tiled máp / pip install pytmx
import sys

"""

Potrebuješ aj stiahnuť a nainštalovať Tiled. Editor máp: https://thorbjorn.itch.io/tiled?download
Ďalej potrebuješ knižnicu pytmx, ktorú nainštaluješ cez pip: pip install pytmx
A nakoniec potrebuješ nejakú .tmx mapu. Môžeš si ju vytvoriť v Tiled, alebo stiahnuť z internetu.

"""

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def load_map(file_path):
    # load_pygame načíta mapu a rovno skonvertuje obrázky pre Pygame
    return pytmx.load_pygame(file_path)

def draw_map(surface, tmx_data):
    # Prechádzame všetky vrstvy mapy
    for layer in tmx_data.visible_layers:
        # Zaujímajú nás len vrstvy, ktoré obsahujú dlaždice (TiledTileLayer)
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    # Vykreslíme dlaždicu na správnu pozíciu
                    # Súradnice x, y v Tiled sú v indexoch mriežky, 
                    # preto ich násobíme šírkou/výškou dlaždice
                    surface.blit(tile, (x * tmx_data.tilewidth, 
                                        y * tmx_data.tileheight))

# Načítanie dát (predpokladajme súbor 'mapa.tmx')
# Skús si vytvoriť jednoduchú mapu v programe Tiled
try:
    tmx_data = load_map("PyGameTUTORIAL/05_TILED_MAPS/tmxs/Map_v1.tmx")
except Exception as e:
    print(f"Chyba pri načítaní mapy: {e}")
    tmx_data = None

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    if tmx_data:
        draw_map(screen, tmx_data)
    else:
        # Ak nemáš .tmx súbor, vypíše aspoň upozornenie
        font = pygame.font.SysFont("Arial", 20)
        img = font.render("Chýba mapa.tmx! Vytvor si ju v programe Tiled.", True, (255, 255, 255))
        screen.blit(img, (50, 50))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()