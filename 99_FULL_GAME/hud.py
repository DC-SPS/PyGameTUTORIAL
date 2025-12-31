import pygame

class HUD:
    def __init__(self, velkost=25):
        self.font = pygame.font.SysFont("arial", velkost)

    def draw(self, screen, state, score):
        state_text = self.font.render(f"State: {state}", True, (255, 255, 255))
        screen.blit(state_text, (10, 10))
        score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (pygame.display.get_window_size()[0] - score_text.get_width() - 10, 10))