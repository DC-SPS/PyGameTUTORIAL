import pygame

pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Pygame Window")

FPS = 60
BG = (0, 0, 0)

sheet = pygame.image.load('PyGameTUTORIAL/02_ANIMACIE/img/Lightning.png').convert_alpha()
shipX, shipY = 400, 300

SHIP_W, SHIP_H = 64, 64
DIRECTION = 'UP'

FRAME_W, FRAME_H = 32, 32
NUM_FRAMES = 4

images = []
for i in range(NUM_FRAMES):
    frame = pygame.Surface((FRAME_W, FRAME_H), pygame.SRCALPHA)
    frame.blit(sheet, (0, 0), pygame.Rect(i * FRAME_W, 0, FRAME_W, FRAME_H))
    frame = pygame.transform.scale(frame, (SHIP_W, SHIP_H))
    images.append(frame)

index = 0
clock = pygame.time.Clock()
isRunning = True

ANIM_FPS = 6
frame_time_ms = 1000.0 / ANIM_FPS
anim_accumulator = 0.0

# ---------------- SHOOTING ----------------
bullets = []
BULLET_SPEED = 10
BULLET_SIZE = 6
shoot_cooldown = 200  # ms
last_shot = 0
# ------------------------------------------

while isRunning:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            isRunning = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        DIRECTION = 'UP'
        shipY = max(0, shipY - 5)

    if keys[pygame.K_DOWN]:
        DIRECTION = 'DOWN'
        shipY = min(HEIGHT - SHIP_H, shipY + 5)

    if keys[pygame.K_LEFT]:
        DIRECTION = 'LEFT'
        shipX = max(0, shipX - 5)

    if keys[pygame.K_RIGHT]:
        DIRECTION = 'RIGHT'
        shipX = min(WIDTH - SHIP_W, shipX + 5)

    # ---------- SHOOTING INPUT ----------
    now = pygame.time.get_ticks()
    if keys[pygame.K_SPACE] and now - last_shot > shoot_cooldown:
        last_shot = now

        bx = shipX + SHIP_W // 2
        by = shipY + SHIP_H // 2

        bullets.append({
            "rect": pygame.Rect(bx, by, BULLET_SIZE, BULLET_SIZE),
            "dir": DIRECTION
        })
    # -----------------------------------

    anim_accumulator += dt
    while anim_accumulator >= frame_time_ms:
        index = (index + 1) % len(images)
        anim_accumulator -= frame_time_ms

    # ---------- MOVE BULLETS ----------
    for bullet in bullets[:]:
        if bullet["dir"] == 'UP':
            bullet["rect"].y -= BULLET_SPEED
        elif bullet["dir"] == 'DOWN':
            bullet["rect"].y += BULLET_SPEED
        elif bullet["dir"] == 'LEFT':
            bullet["rect"].x -= BULLET_SPEED
        elif bullet["dir"] == 'RIGHT':
            bullet["rect"].x += BULLET_SPEED

        if not screen.get_rect().colliderect(bullet["rect"]):
            bullets.remove(bullet)
    # ---------------------------------

    screen.fill(BG)

    if DIRECTION == 'UP':
        screen.blit(images[index], (shipX, shipY))
    elif DIRECTION == 'DOWN':
        screen.blit(pygame.transform.flip(images[index], False, True), (shipX, shipY))
    elif DIRECTION == 'LEFT':
        screen.blit(pygame.transform.rotate(images[index], 90), (shipX, shipY))
    elif DIRECTION == 'RIGHT':
        screen.blit(pygame.transform.rotate(images[index], -90), (shipX, shipY))

    # ---------- DRAW BULLETS ----------
    for bullet in bullets:
        pygame.draw.rect(screen, (255, 255, 0), bullet["rect"])
    # ---------------------------------

    pygame.display.flip()

pygame.quit()
