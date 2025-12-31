import pygame

pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Pygame Window")

FPS = 60

# background color (used to clear the screen)
BG = (0, 0, 0)

# Load sprite sheet once
sheet = pygame.image.load('02_ANIMACIE\img\Lightning.png').convert_alpha()
shipX, shipY = 400, 300
isShooting = False
SHIP_W, SHIP_H = 64, 64
DIRECTION = 'UP'  # 'UP', 'DOWN', 'LEFT', 'RIGHT'

# frame size in the sheet and number of frames
FRAME_W, FRAME_H = 32, 32
NUM_FRAMES = 4

# extract frames properly using area or subsurface
images = []
for i in range(NUM_FRAMES):
    frame = pygame.Surface((FRAME_W, FRAME_H), pygame.SRCALPHA)
    frame.blit(sheet, (0, 0), pygame.Rect(i * FRAME_W, 0, FRAME_W, FRAME_H))
    frame = pygame.transform.scale(frame, (SHIP_W, SHIP_H))
    images.append(frame)

index = 0
clock = pygame.time.Clock()
isRunning = True

# animation settings
ANIM_FPS = 6  # animation frames per second (slower)
frame_time_ms = 1000.0 / ANIM_FPS
anim_accumulator = 0.0

while isRunning:
    # dt is milliseconds since last tick
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            isRunning = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        DIRECTION = 'UP'
        shipY -= 5
        if shipY < 0:
            shipY = 0
    if keys[pygame.K_DOWN]: 
        DIRECTION = 'DOWN'
        shipY += 5
        if shipY > HEIGHT - SHIP_H:
            shipY = HEIGHT - SHIP_H
    if keys[pygame.K_LEFT]:
        DIRECTION = 'LEFT'
        shipX -= 5
        if shipX < 0:
            shipX = 0
    if keys[pygame.K_RIGHT]:
        DIRECTION = 'RIGHT'
        shipX += 5
        if shipX > WIDTH - SHIP_W:
            shipX = WIDTH - SHIP_W
    if keys[pygame.K_SPACE]:
        isShooting = True
    else:
        isShooting = False

    # advance animation on its own timing
    anim_accumulator += dt
    while anim_accumulator >= frame_time_ms:
        index = (index + 1) % len(images)
        anim_accumulator -= frame_time_ms

    screen.fill(BG)

    if DIRECTION == 'UP':
        screen.blit(images[index], (shipX, shipY))  # Draw the current frame    
    elif DIRECTION == 'DOWN':
        flipped_image = pygame.transform.flip(images[index], False, True)
        screen.blit(flipped_image, (shipX, shipY))  # Draw the current frame
    elif DIRECTION == 'LEFT':
        flipped_image = pygame.transform.rotate(images[index], 90)
        screen.blit(flipped_image, (shipX, shipY))  # Draw the current frame
    elif DIRECTION == 'RIGHT':
        flipped_image = pygame.transform.rotate(images[index], -90)
        screen.blit(flipped_image, (shipX, shipY))  # Draw the current frame

    #screen.blit(images[index], (shipX, shipY))  # Draw the current frame

    pygame.display.flip()

pygame.quit()