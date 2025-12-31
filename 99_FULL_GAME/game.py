import pygame
from gamestatemanager import GameStateManager
from hud import HUD
from gameobjects import Player

class Game(pygame.sprite.Sprite):
    def __init__(self):
        pygame.init()
        pygame.font.init()
        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame - základ")

        self.clock = pygame.time.Clock()
        self.running = True

        self.state_manager = GameStateManager()
        self.player = Player(self.width // 2, self.height // 2, 40, 40)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.hud = HUD()

        # MENU
        self.selected = 0
        self.menu_items = ["PLAY", "EXIT"]
        self.font = pygame.font.SysFont("arial", 48)

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # FPS

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.state_manager.set_state("PAUSE")
                self.menu_items = ["PLAY", "RESUME", "EXIT"]

        
            # -------- MENU -------- MENU, PLAY, PAUSE, GAME_OVER
            if self.state_manager.state == "MENU" or self.state_manager.state == "PAUSE":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.menu_items)
                    if event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.menu_items)
                    if event.key == pygame.K_RETURN:
                        if self.menu_items[self.selected] == "PLAY":
                            self.state_manager.set_state("PLAY")
                            # Inicializácia alebo resetovanie hry
                            self.all_sprites.empty()
                            self.player = Player(self.width // 2, self.height // 2, 40, 40)
                            self.all_sprites.add(self.player)
                        elif self.menu_items[self.selected] == "RESUME":
                            # Pokračovanie hry
                            self.state_manager.set_state("PLAY")
                        elif self.menu_items[self.selected] == "EXIT":
                            # Ukončenie hry
                            self.running = False

    def update(self):
        # MENU, PLAY, PAUSE, GAME_OVER
        if self.state_manager.state == "PLAY":
            self.all_sprites.update()
            #self.player.update()

    def render(self):
        # MENU, PLAY, PAUSE, GAME_OVER
        if self.state_manager.state == "MENU":
            self.screen.fill((255, 0, 0))
            self.draw_menu()

        if self.state_manager.state == "PAUSE":
            self.screen.fill((0, 255, 0))
            self.all_sprites.draw(self.screen)
            #self.player.draw(self.screen)
            self.draw_menu()
            
        if self.state_manager.state == "GAME_OVER":
            self.screen.fill((0, 0, 255))
           
        if self.state_manager.state == "PLAY":
            self.screen.fill((30, 30, 30))
            self.all_sprites.draw(self.screen)
            #self.player.draw(self.screen)

        self.hud.draw(self.screen, self.state_manager.state, self.player.score)
        pygame.display.flip()

    def draw_menu(self):
        for i, text in enumerate(self.menu_items):
            color = (255, 255, 0) if i == self.selected else (200, 200, 200)
            label = self.font.render(text, True, color)
            rect = label.get_rect(center=(self.width // 2, self.height // 3 + i * 60))
            self.screen.blit(label, rect)
