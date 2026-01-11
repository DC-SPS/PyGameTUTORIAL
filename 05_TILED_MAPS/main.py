import pygame
import sys
import pytmx

# --- INICIALIZÁCIA ---
pygame.init()
WIDTH, HEIGHT = 960, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- NAČÍTANIE MAPY ---
try:
    # Cesta k tvojmu súboru
    tmx_data = pytmx.load_pygame("05_TILED_MAPS/tmxs/Map_v1.tmx")
    tile_w = tmx_data.tilewidth # 32 
    tile_h = tmx_data.tileheight # 32 
    map_w_px = tmx_data.width * tile_w
except Exception as e:
    print(f"Chyba: {e}")
    sys.exit()

# --- EXTRAKCIA KOLÍZIÍ ---
platforms = []
for layer in tmx_data.visible_layers:
    # Dôležité: Názov vrstvy v TMX je "Tile Layer 1" [cite: 1, 2]
    if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "Tile Layer 1":
        for x, y, gid in layer:
            if gid != 0:
                platforms.append(pygame.Rect(x * tile_w, y * tile_h, tile_w, tile_h))

# --- HRÁČ ---
# Zmenšil som Rect hráča na 30x30, aby sa "nezasekával" v 32px dierach
player_rect = pygame.Rect(100, 500, 30, 30) 
player_vel_y = 1
player_speed = 6
GRAVITY = 0.8
JUMP_STRENGTH = -16
is_jumping = True
camera_x = 0

running = True
while running:
    screen.fill((0, 0, 0))
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                player_vel_y = JUMP_STRENGTH
                is_jumping = True

    # --- POHYB ---
    keys = pygame.key.get_pressed()
    move_x = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * player_speed

    # 1. Horizontálny pohyb
    player_rect.x += move_x
    for plat in platforms:
        if player_rect.colliderect(plat):
            if move_x > 0: player_rect.right = plat.left
            elif move_x < 0: player_rect.left = plat.right

    # 2. Vertikálny pohyb (Gravitácia)
    player_vel_y += GRAVITY
    player_rect.y += player_vel_y
    
    on_ground = False
    for plat in platforms:
        if player_rect.colliderect(plat):
            # Padáme dole
            if player_vel_y > 0:
                player_rect.bottom = plat.top
                player_vel_y = 0
                on_ground = True
            # Skáčeme hore
            elif player_vel_y < 0:
                player_rect.top = plat.bottom
                player_vel_y = 0
    
    is_jumping = not on_ground

    # --- KAMERA ---
    camera_x = player_rect.centerx - WIDTH // 2
    if camera_x < 0: camera_x = 0
    if camera_x > map_w_px - WIDTH: camera_x = map_w_px - WIDTH

    # --- VYKRESLOVANIE ---
    # (Vykresli pozadia ako predtým...)
    
    # Mapa
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    screen.blit(tile, (x * tile_w - camera_x, y * tile_h))

    # Hráč
    pygame.draw.rect(screen, (0, 0, 255), (player_rect.x - camera_x, player_rect.y, player_rect.width, player_rect.height))

    pygame.display.flip()

pygame.quit()