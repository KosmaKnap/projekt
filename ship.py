import pygame
from pygame.sprite import Sprite

class Ship(Sprite): # Klasa przeznaczona do zarządzania statkiem kosmicznym

	def __init__(self, ai_game):
		#inicjalizacja statku oraz jego położenie początkowe
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect = ai_game.screen.get_rect()

		#Wczytanie grafiki statku kosmicznego i pobranie jego prostokąta
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()

		#Każdy nowy statek pojawia się na dole ekranu
		self.rect.midbottom = self.screen_rect.midbottom
		
		self.x = float(self.rect.x) #Położenie poziome statku przechowywane jest w zmiennej typu float

		#opcje wskazujące na poruszanie się statku
		self.moving_right = False 
		self.moving_left = False

	def update(self): # Uaktualnienie położenia statku
		#uaktualnienie wartości poziomej statku, a nie prostokąta (rect)
		if self.moving_right and self.rect.right <self.screen_rect.right:
			self.x +=self.settings.ship_speed
		if self.moving_left and self.rect.left > 0:
			self.x -=self.settings.ship_speed

		self.rect.x = self.x #uaktualnienie obiektu rect(prostokat) na podstawie wartosci self.x

	def blitme(self): # Wyswietlenie statku kosmicznego w jego aktualnym położeniu
		self.screen.blit(self.image, self.rect)

	def center_ship(self): # Umieszczenie statku w pozycji wyjściowej (środek dół)
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)