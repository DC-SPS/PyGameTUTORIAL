import pygame

class Game:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.WINDOW_WIDTH = info.current_w
        self.WINDOW_HEIGHT = info.current_h
        pygame.font.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption('Základná herná slučka - GAME')
        self.FPS = 60

    def input_handler(self):
        # Spracovanie vstupu - HANDLE INPUT
        keys = pygame.key.get_pressed()
        
    def update_game_objects(self):
        # Aktualizácia herných objektov - UPDATE
        self.screen.fill((0, 0, 0))  # Vyplnenie obrazovky čiernou farbou

    def render_game_objects(self):
        # Vykreslenie herných objektov na obrazovku - RENDER
        pygame.display.flip()    # Aktualizácia obrazovky

    def run(self):
        running = True
        while running:
            self.clock.tick(self.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.input_handler()
            self.update_game_objects()
            self.render_game_objects()


        pygame.quit()