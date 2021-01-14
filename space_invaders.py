import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button

class AlienInvasion: #Ogólna klasa przeznaczona do zarządzania zasobami i sposobem działania gry
    
    def __init__(self): #Inicjalizacja gry i utworzenie jej zasobów

        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        # Utworzenie egzemplarza przechowującego dane statystyczne oraz klasy Scoreboard
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        self.play_button = Button(self, "Graj") # Utworzenie przycisku Gra

    def run_game(self): #Rozpoczęcie głównej pętli gry
        while True: #Oczekiwanie na kliknięcie myszką lub wciśnięcie klawisza
            self._check_events() #Odświeżenie ekranu w trakcie każdej iteracji pętli

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen() #uaktualnienie obrazów na ekranie i przejście do nowego ekranu

    def _update_bullets(self):
        self.bullets.update() # Uaktualnienie położenia pocisków

        # Usuwanie pocisków poza ekranem
        for bullet in self.bullets.copy():
             if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        print(len(self.bullets))

        self._check_bullet_alien_coliisions()

    def _check_bullet_alien_coliisions(self): # Reakcja na zderzenie pocisku z obcym
         # Sprawdzenie, czy pocisk trafił obcego, jeśli tak to usuwamy i pocisk i obcego
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Pozbywamy się reszty pocisków i tworzymy nową flotę
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Inkrementacja poziomu
            self.stats.level +=1
            self.sb.prep_level()

    def _ship_hit(self): # Reakcja na zniszczenie statku
        if self.stats.ships_left > 0:
            # Zmniejszenie wartości w ships_left i uaktualnienie ilości posiadanych statków
            self.stats.ships_left -=1
            self.sb.prep_ships()

            # Usunięcie zawartości list aliens i bullets
            self.aliens.empty()
            self.bullets.empty()

            # Utworzenie nowej floty oraz wyśrodkowanie statku
            self._create_fleet()
            self.ship.center_ship()

            # Stop
            sleep(0.6)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self): 
        self._check_fleet_edges() # Sprawdzenie czy flota znajduje się przy krawędzi
        self.aliens.update() # Uaktualnienie położenia obcych

        # Wykrywanie kolizji między flotą a naszym statkiem
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        
        # Wykrywanie obcych docierających do dolnej krawędzi ekranu
        self._check_aliens_bottom()

    def _check_aliens_bottom(self): # Sprawdzenie czy obcy dotarł do dolnej krawędzi ekranu
        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit() # Jak w przypadku zderzenia ze statkiem
                break

    def _create_fleet(self): # Utworzenie floty
        # Utworzenie obcego
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        
        # Ilosc rzędów która zmieści się na ekranie
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        
        # Stworzenie floty
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)
    
    def _create_alien(self, alien_number, row_number): # Stworzenie obcego i umieszczenie go w rzędzie
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self): # Reakcja, gdy obcy dotknie krawędzi
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self): # Przesunięcie floty w dół i zmiana kierunku jej poruszania
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):	
        self.screen.fill(self.settings.bg_color) #Odświeżanie ekranu w trakcie każdej iteracji pętli
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Wyświetlenie punktacji
        self.sb.show_score()

        # Wyświetlenie przycisku tylko, gdy gra jest niekatywna
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip() #Nakazanie pythonowi wyświetlenia ostatnio odświeżonego ekranu

    def _check_events(self): #reakcja na klawiature i mysz
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos): # Rozpoczęcie nowej gry po kliknięciu przycisku "Graj"
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.settings.initialize_dynamic_settings() # Wyzerowanie ustawień gry
            
            # Wyzerowanie danych gry
            self.stats.reset_stats() 
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Ukrycie kursora
            pygame.mouse.set_visible(False)

            # Usunięcie zawartości list aliens i bullets
            self.aliens.empty()
            self.bullets.empty()

            # Utworzenie nowej armii i wyśrodkowanie statku
            self._create_fleet()
            self.ship.center_ship()
	
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT: 
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT: 
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key ==pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key ==pygame.K_LEFT:
            self.ship.moving_left = False
    
    def _fire_bullet(self): # Utworzenie nowego pocisku i dodanie go do grupy pocisków
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

if __name__ == '__main__': # Utworzenie egzemplarza gry i jej uruchomienie
    ai = AlienInvasion()
    ai.run_game()