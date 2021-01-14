import pygame
from pygame.sprite import Sprite

class Bullet(Sprite): #Klasa dla pocisków

	def __init__(self, ai_game):
		#Utworzenie obiektu pocisku w aktualnym położeniu statku
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.color = self.settings.bullet_color

		#Utworzenie prostokąta pocisku w punkcie(0,0) i nadanie mu odpowiedniego położenia
		self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
		self.rect.midtop = ai_game.ship.rect.midtop

		self.y = float(self.rect.y) #polozenie pocisku jest zmienna typu float

	def update(self): #poruszanie pociskiem po ekranie
		#uaktualnienie położenia pocisku
		self.y -=self.settings.bullet_speed

		#uaktualnienie rect pocisku
		self.rect.y = self.y

	def draw_bullet(self): #wyświetlenie pocisku na ekranie
		pygame.draw.rect(self.screen, self.color, self.rect)