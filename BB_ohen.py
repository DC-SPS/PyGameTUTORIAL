import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

# Vytvorenie okna
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Ako animovať oheň')

# Nastavenie farieb
bg = (0, 0, 0)

# Nastavenie fontov a textov
font = pygame.font.SysFont('arial', 50)

fire_group = pygame.sprite.Group() # Skupina pre animácie ohňa


#create Explosion class
class Ohen(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 7):
			# Load and scale
			raw = pygame.image.load(f"img/exp{num:02d}.png")
			raw = pygame.transform.scale(raw, (100, 100))
			# Create surface with per-pixel alpha and copy pixels,
			# turning nearly-white pixels into fully transparent ones.
			w, h = raw.get_size()
			img = pygame.Surface((w, h), pygame.SRCALPHA)
			# Use a tolerance for 'white' to handle compression artifacts
			threshold = 250
			src = raw.convert()  # readable pixels
			for ix in range(w):
				for iy in range(h):
					col = src.get_at((ix, iy))
					# col may be (r,g,b) or (r,g,b,a)
					r, g, b = col[0], col[1], col[2]
					if len(col) > 3:
						a = col[3]
					else:
						a = 255
					if r >= threshold and g >= threshold and b >= threshold:
						img.set_at((ix, iy), (r, g, b, 0))
					else:
						img.set_at((ix, iy), (r, g, b, 255))
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
		explosion_speed = 4
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		#if the animation is complete, reset animation index
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()


# Herná slučka
running = True
while running:
	
    clock.tick(fps)  # Nastavenie snímkovej frekvencie

    for event in pygame.event.get(): # Spracovanie udalostí
        if event.type == pygame.QUIT: # Ukončenie hry pri zatvorení okna X
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
			# Use the event position and only respond to left-click (button 1)
            if hasattr(event, 'pos') and event.button == 1:
                x, y = event.pos
                ohen = Ohen(x, y)
                fire_group.add(ohen)

    screen.fill(bg)  # Vyplnenie obrazovky čiernou farbou

    font.render('Klikni myš a uvidíš Oheň', True, (255, 0, 0))
    screen.blit(font.render('Klikni myš a uvidíš Oheň  ', True, (255, 0, 0)), (50, 50))

    fire_group.update()
    fire_group.draw(screen)

    #pygame.draw.circle(screen, (255, 0, 0), (200, 150), 50)  # Nakreslenie červeného kruhu

    pygame.display.flip()    # Aktualizácia obrazovky

pygame.quit()
