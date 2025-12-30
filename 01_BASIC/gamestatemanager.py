class GameStateManager:
    def __init__(self):
        self.state = "MENU"  # MENU, PLAY, PAUSE, GAME_OVER

    def set_state(self, new_state):
        self.state = new_state
