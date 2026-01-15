import pygame
import sys

# Inicializácia
pygame.init()
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level 1: Parallax + Tiled 2D World")
clock = pygame.time.Clock()

# Pomocná funkcia na načítanie a škálovanie
def load_img(path, size=(WIDTH, HEIGHT)):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size)

# --- NAČÍTANIE GRAFIKY (Assety) ---
sky = load_img("PyGameTUTORIAL/05_TILED_MAPS/imgs/sky_solid_color.png")
clouds = load_img("PyGameTUTORIAL/05_TILED_MAPS/imgs/clouds.png")
mtn_far = load_img("PyGameTUTORIAL/05_TILED_MAPS/imgs/mountain_depth_z_1.png")
mtn_near = load_img("PyGameTUTORIAL/05_TILED_MAPS/imgs/mountain_depth_z_2.png")
# Tileset pre hráča alebo platformy (použijeme kúsok z neho)
tileset = pygame.image.load("PyGameTUTORIAL/05_TILED_MAPS/imgs/pixel_platform_03_tileset_final.png").convert_alpha()

# --- HRÁČ A FYZIKA ---
player_rect = pygame.Rect(100, 400, 40, 40)
player_vel_y = 0
player_speed = 6
GRAVITY = 0.9
JUMP_STRENGTH = -16
is_jumping = False

# --- MAPA (Tiled simulácia) ---
# Chýba: tmx_data = pytmx.load_pygame("mapa.tmx")
platforms = [
    pygame.Rect(0, 550, 2000, 50),    # Hlavná zem 
    pygame.Rect(400, 400, 200, 30),   # Plošina 1
    pygame.Rect(700, 300, 200, 30),   # Plošina 2
    pygame.Rect(1000, 450, 300, 30),  # Plošina 3
]

# Kamera (posun sveta)
camera_x = 0 # Nuž veď som vravel, že sa treba učiť teóriu - MATEMATKA, FYZIKA sú ako dve sestry :D

running = True
while running:
    screen.fill((0, 0, 0))
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
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

    # Aplikácia pohybu X
    player_rect.x += move_x
    # Kamera nasleduje hráča (udržuje ho v strede)
    camera_x = player_rect.centerx - WIDTH // 2

    # Aplikácia gravitácie a Y
    player_vel_y += GRAVITY
    player_rect.y += player_vel_y

    # Kolízie s mapou
    on_ground = False
    for plat in platforms:
        if player_rect.colliderect(plat):
            if player_vel_y > 0:
                player_rect.bottom = plat.top
                player_vel_y = 0
                on_ground = True
    is_jumping = not on_ground

    # --- VYKRESLOVANIE (PORADIE VRSTIEV) ---
    
    # 1. Statická obloha
    screen.blit(sky, (0, 0))

    # 2. Parallax - Oblaky (najpomalšie)
    screen.blit(clouds, (-(camera_x * 0.1) % WIDTH, 50))
    screen.blit(clouds, (-(camera_x * 0.1) % WIDTH - WIDTH, 50))

    # 3. Parallax - Vzdialené hory
    screen.blit(mtn_far, (-(camera_x * 0.3) % WIDTH, 100))
    screen.blit(mtn_far, (-(camera_x * 0.3) % WIDTH - WIDTH, 100))

    # 4. Parallax - Bližšie hory
    screen.blit(mtn_near, (-(camera_x * 0.6) % WIDTH, 200))
    screen.blit(mtn_near, (-(camera_x * 0.6) % WIDTH - WIDTH, 200))

    # 5. Svet (Mapa a Platformy) - hýbu sa 1:1 s kamerou
    for plat in platforms:
        # Vykresľujeme relatívne ku kamere
        draw_rect = pygame.Rect(plat.x - camera_x, plat.y, plat.width, plat.height)
        pygame.draw.rect(screen, (100, 60, 30), draw_rect) # Hnedá farba zeme

    # 6. Hráč
    pygame.draw.rect(screen, (50, 150, 255), (player_rect.x - camera_x, player_rect.y, player_rect.width, player_rect.height))

    # --- HUD Info ---
    font = pygame.font.SysFont("Arial", 20, bold=True)
    info = font.render("Šípky: Pohyb | Medzera: Skok | Parallax Level 1", True, (255, 255, 255))
    screen.blit(info, (20, 20))

    pygame.display.flip()

pygame.quit()