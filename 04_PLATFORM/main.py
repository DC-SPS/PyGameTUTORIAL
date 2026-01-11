import pygame
import sys

pygame.init()

# Nastavenia okna
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Farby
WHITE = (240, 240, 240)
BLUE = (50, 150, 255)
GREEN = (50, 200, 50)
DARK_GREY = (40, 40, 40)

# Písmo
font = pygame.font.SysFont("Consolas", 22, bold=True)

# Premenné pre hráča
player_rect = pygame.Rect(100, HEIGHT - 200, 50, 50)
player_vel_y = 0 
player_speed = 8 
is_jumping = False
GRAVITY = 0.98
JUMP_STRENGTH = -18 

# Plošiny
base = (150, HEIGHT - 50, WIDTH-200, 50)
platforms = [
    pygame.Rect(base),
    pygame.Rect(base[0]-50, base[1] - 100, 300, 40),
    pygame.Rect(base[0]+100, base[1] - 250, 250, 40),
    pygame.Rect(base[0]+150, base[1] - 450, 200, 40)
]

running = True
while running:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                player_vel_y = JUMP_STRENGTH
                is_jumping = True

    # 1. Os X
    keys = pygame.key.get_pressed()
    move_x = 0
    if keys[pygame.K_LEFT]:  move_x -= player_speed
    if keys[pygame.K_RIGHT]: move_x += player_speed

    player_rect.x += move_x
    for plat in platforms:
        if player_rect.colliderect(plat):
            if move_x > 0: player_rect.right = plat.left
            if move_x < 0: player_rect.left = plat.right

    # 2. Os Y
    player_vel_y += GRAVITY
    player_rect.y += player_vel_y
    on_ground = False

    for plat in platforms:
        if player_rect.colliderect(plat):
            if player_vel_y > 0:
                player_rect.bottom = plat.top
                player_vel_y = 0
                on_ground = True
            elif player_vel_y < 0:
                player_rect.top = plat.bottom
                player_vel_y = 0
    is_jumping = not on_ground

    # --- VYKRESLOVANIE ---
    for plat in platforms:
        pygame.draw.rect(screen, GREEN, plat)
    
    pygame.draw.rect(screen, BLUE, player_rect)

    # --- INFO PRE HRÁČA (UI) ---
    # Renderujeme texty priamo v loope, ak by sa náhodou menili, 
    # ale pre výkon je lepšie ich mať pred loopom, ak sú statické.
    img_esc = font.render("ESC: Ukončiť", True, DARK_GREY)
    img_move = font.render("ŠÍPKY: Pohyb", True, DARK_GREY)
    img_jump = font.render("MEDZERA: Skok", True, DARK_GREY)
    img_speed = font.render(f"Výška skoku v Y: {round(player_vel_y, 2)}", True, DARK_GREY)


    # Vykreslenie s malým odsadením od okraja
    screen.blit(img_esc, (30, 30))
    screen.blit(img_move, (30, 60))
    screen.blit(img_jump, (30, 90))
    screen.blit(img_speed, (30, 120))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()