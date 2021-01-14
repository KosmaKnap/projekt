class GameStats: # Monitoring danych statystycznych

    def __init__(self, ai_game): # Inicjalizacja danych
        self.settings = ai_game.settings
        self.reset_stats()

        # Uruchomienie gry w stanie nieaktywnym
        self.game_active = False

        # Najlepszy wynik nigdy nie będzie wyzerowany
        self.high_score = 0
    
    def reset_stats(self): # Inicjalizacja danych, które mogą się zmieniać w trakcie gry
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1