import pygame
import sys
import pytmx

# Inicializácia
pygame.init()
WIDTH, HEIGHT = 1024, 1024
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level 1: Parallax + Skutočná Tiled Mapa")
clock = pygame.time.Clock()

# Pomocná funkcia na načítanie a škálovanie
def load_img(path, size=(WIDTH, HEIGHT)):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size)

# --- NAČÍTANIE GRAFIKY (Assety) ---
sky = load_img("05_TILED_MAPS/imgs/sky_solid_color.png")
clouds = load_img("05_TILED_MAPS/imgs/clouds.png")
mtn_far = load_img("05_TILED_MAPS/imgs/mountain_depth_z_1.png")
mtn_near = load_img("05_TILED_MAPS/imgs/mountain_depth_z_2.png")

# --- NAČÍTANIE MAPY ---
try:
    # Načítame vašu mapu Map_v1.tmx 
    tmx_data = pytmx.load_pygame("05_TILED_MAPS/tmxs/Map_v1.tmx")
    tile_width = tmx_data.tilewidth
    tile_height = tmx_data.tileheight
except Exception as e:
    print(f"Chyba pri načítaní mapy: {e}")
    sys.exit()

# Extrakcia kolízií z vrstvy "Tile Layer 1" 
platforms = []
for layer in tmx_data.visible_layers:
    if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "Tile Layer 1":
        for x, y, gid in layer:
            if gid != 0:  # Ak dlaždica nie je prázdna, vytvoríme Rect pre kolíziu
                platforms.append(pygame.Rect(x * tile_width, y * tile_height, tile_width, tile_height))

# --- HRÁČ A FYZIKA ---
player_rect = pygame.Rect(100, 100, 32, 32) # Upravená veľkosť podľa tilewidth 
player_vel_y = 0
player_speed = 6
GRAVITY = 0.8
JUMP_STRENGTH = -16
is_jumping = False

# Kamera
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
    move_x = 0
    if keys[pygame.K_LEFT]: move_x = -player_speed
    if keys[pygame.K_RIGHT]: move_x = player_speed

    # Os X a kolízie
    player_rect.x += move_x
    for plat in platforms:
        if player_rect.colliderect(plat):
            if move_x > 0: player_rect.right = plat.left
            if move_x < 0: player_rect.left = plat.right

    # Os Y a gravitácia
    player_vel_y += GRAVITY
    player_rect.y += player_vel_y
    
    on_ground = False
    for plat in platforms:
        if player_rect.colliderect(plat):
            if player_vel_y > 0: # Pristátie
                player_rect.bottom = plat.top
                player_vel_y = 0
                on_ground = True
            elif player_vel_y < 0: # Náraz hlavou
                player_rect.top = plat.bottom
                player_vel_y = 0
    is_jumping = not on_ground

    # Kamera sleduje hráča
    camera_x = player_rect.centerx - WIDTH // 2

    # --- VYKRESLOVANIE ---
    
    # 1. Parallax pozadie
    screen.blit(sky, (0, 0))
    screen.blit(clouds, (-(camera_x * 0.1) % WIDTH, 50))
    screen.blit(clouds, (-(camera_x * 0.1) % WIDTH - WIDTH, 50))
    screen.blit(mtn_far, (-(camera_x * 0.3) % WIDTH, 100))
    screen.blit(mtn_far, (-(camera_x * 0.3) % WIDTH - WIDTH, 100))
    screen.blit(mtn_near, (-(camera_x * 0.6) % WIDTH, 200))
    screen.blit(mtn_near, (-(camera_x * 0.6) % WIDTH - WIDTH, 200))

    # 2. Vykreslenie Tiled Mapy
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    # Kreslíme dlaždice posunuté o kameru
                    screen.blit(tile, (x * tile_width - camera_x, y * tile_height))

    # 3. Hráč (Modrá kocka)
    pygame.draw.rect(screen, (50, 150, 255), (player_rect.x - camera_x, player_rect.y, player_rect.width, player_rect.height))

    pygame.display.flip()

pygame.quit()
sys.exit()