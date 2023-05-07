#Либы
import pygame, sys
#from threading import Timer as tmr
import time
from random import randint

#Инициализация либ
pygame.init() #Инициализация пайгеим
pygame.mixer.init(channels=12) #Инициализация pygame.mixer и установка ограничения 12 канала

#Класс игры, в нём происходят основные действия
class Game:
	def __init__(self):
		#Гл. Настройки
		self.version = "0.3v" #Версия игры
		self.MASHTAB = 5 #Умножение размера текстур (Норма - 5. Нетбуки - 4)
		self.screensize = [135 * self.MASHTAB, 100 * self.MASHTAB] #Размер окна (810, 600)
		self.screen = pygame.display.set_mode(self.screensize) #Создание окна
		self.MAX_SCORE = 0 # Рекорд
		self.GAME_TYPE = "NONE" # 2 игрока - 2P, 1 игрок - 1P
		self.SOUND_OFF = 0 #Звук выключен? ?_?
		pygame.display.set_caption(f"Лютый Гонщик {self.version}") #Название окна
		pygame.display.set_icon(pygame.image.load("assets/Images/LOGO.png"))
		self.clock = pygame.time.Clock() #Pygame клок
		self.running = 0 #Да.
		self.FPS = 60 #ФиПиЭйС

		self.CONSOLE_ENABLED = 0 #Отвечает за разблокировку консоли игры. Обычно включается во время разработки или в дев. билдах (auto-py-to-exe)
		self.DEBUG_TEXT_ENABLE = 0 #Отвечает за разблокировку дебаг текста

		#Управление
		self.KEY_LEFT = pygame.K_a #Клавиша "ВЛЕВО"
		self.KEY_RIGHT = pygame.K_d #Клавиша "ВПРАВО"
		self.P2_KEY_LEFT = pygame.K_LEFT
		self.P2_KEY_RIGHT = pygame.K_RIGHT

		#Дорога
		self.BACKGROUND_PNG = pygame.image.load("assets/Images/BACKGROUND.png")

		#Тролебусы
		self.AQUA_TROLLEBUS_PNG = pygame.image.load("assets/Images/AQUA_TROLLEBUS.png").convert_alpha()
		self.GRAY_TROLLEBUS_PNG = pygame.image.load("assets/Images/GRAY_TROLLEBUS.png").convert_alpha()
		self.LIME_TROLLEBUS_PNG = pygame.image.load("assets/Images/LIME_TROLLEBUS.png").convert_alpha()
		
		#Машины
		self.AQUA_VAZ_PNG = pygame.image.load("assets/Images/AQUA_VAZ-2107.png").convert_alpha()
		self.LIME_VAZ_PNG = pygame.image.load("assets/Images/LIME_VAZ-2107.png").convert_alpha()
		self.WHITE_VAZ_PNG = pygame.image.load("assets/Images/WHITE_VAZ-2107.png").convert_alpha()
		self.POLICE_VAZ_PNG = pygame.image.load("assets/Images/POLICE_VAZ-2107.png").convert_alpha()
		self.SPORT_VAZ_PNG = pygame.image.load("assets/Images/SPORT_VAZ-2107.png").convert_alpha()
		self.GAZELL_PNG = pygame.image.load("assets/Images/GAZELL.png").convert_alpha()

		#GFX
		self.CAR_CRASH = pygame.mixer.Sound("assets/GFX/CAR_CRASH.ogg")
		self.CAR_POLICE = pygame.mixer.Sound("assets/GFX/POLICE.ogg")
		self.CAR_MOVE = pygame.mixer.Sound("assets/GFX/CAR_MOVE.ogg")
		#Game Font
		self.GAME_FONT = "assets/GAME_FONT.ttf"

		self.XSIZE() #Увеличение размера спрайтов в 4 раза
		self.MACHINES_TO_RAND = [self.AQUA_TROLLEBUS_PNG, self.GRAY_TROLLEBUS_PNG, self.LIME_TROLLEBUS_PNG, self.AQUA_VAZ_PNG, self.LIME_VAZ_PNG, self.WHITE_VAZ_PNG, self.GAZELL_PNG]
		self.SZ_MACHINES_TO_RAND = [self.AQUA_TROLLEBUS_PNG_SIZE, self.GRAY_TROLLEBUS_PNG_SIZE, self.LIME_TROLLEBUS_PNG_SIZE, self.AQUA_VAZ_PNG_SIZE, self.LIME_VAZ_PNG_SIZE, self.WHITE_VAZ_PNG_SIZE, self.GAZELL_PNG_SIZE]
		self.MACHINES = 7-1
		self.Values() #Инициализация игровых переменных
		self.MainMenu()
		#self.TestPolygon() #Запуск игровой сцены

	def Values(self):
		#Переменные 140

		self.PLAYER_UNLOCK_CONTROLS = 0 #Отвечает за разблокировку управления игроком
		self.PLAYER_COLLISION = 1 #Коллизия игрока
		self.PLAYER_SCORE = 0 #Очки игрока
		self.PLAYER_SPEED = 1.6 * self.MASHTAB #Скорость машины игрока
		self.PLAYER_SPEED_OTH = 0.8 * self.MASHTAB #Скорость машины игрока в направление Лево/Право
		if self.GAME_TYPE == "1P":
			self.PLAYER_CAR_X = 63.3 * self.MASHTAB #Координата тачки игрока по оси X
			self.PLAYER_CAR_Y = 78 * self.MASHTAB #Координата тачки игрока по оси Z
			self.PLAYER2_CAR_X = 0 #Координата полицейской тачки по оси X
			self.PLAYER2_CAR_Z = 0 #Координата полицейской тачки по оси Z
		else:
			self.PLAYER_CAR_X = 28 * self.MASHTAB #Координата тачки игрока по оси X
			self.PLAYER_CAR_Y = 78 * self.MASHTAB #Координата тачки игрока по оси Z
			self.PLAYER2_CAR_X = 98 * self.MASHTAB #Координата полицейской тачки по оси X
			self.PLAYER2_CAR_Z = 78 * self.MASHTAB #Координата полицейской тачки по оси Z

		self.CAN_GENERATEMACHINES = 0 #Могут ли генерироватся машины?
		self.F_GN = 150 * self.MASHTAB #Минимальная координата спавна машин
		self.S_GN = 550 * self.MASHTAB #Максимальная координата спавна машин

		self.CAR1_X = 7.26 * self.MASHTAB #X машины на 1 линии
		self.CAR1_Z = 0 #X машины на 1 линии
		self.IS_CAR1 = 0 
		self.SN_CAR1 = 0
		self.MA_CAR1 = ""
		self.MA_CAR1_SZ = [0, 0]

		self.CAR2_X = 21.25 * self.MASHTAB #X машины на 2 линии
		self.CAR2_Z = 0 #X машины на 2 линии
		self.IS_CAR2 = 0
		self.SN_CAR2 = 0
		self.MA_CAR2 = ""
		self.MA_CAR2_SZ = [0, 0]

		self.CAR3_X = 35.25 * self.MASHTAB #X машины на 3 линии
		self.CAR3_Z = 0 #X машины на 3 линии
		self.IS_CAR3 = 0
		self.SN_CAR3 = 0
		self.MA_CAR3 = ""
		self.MA_CAR3_SZ = [0, 0]

		self.CAR4_X = 49.3 * self.MASHTAB #X машины на 4 линии
		self.CAR4_Z = 0 #X машины на 4 линии
		self.IS_CAR4 = 0
		self.SN_CAR4 = 0
		self.MA_CAR4 = ""
		self.MA_CAR4_SZ = [0, 0]

		self.CAR5_X = 63.3 * self.MASHTAB #X машины на 5 линии
		self.CAR5_Z = 0 #X машины на 5 линии
		self.IS_CAR5 = 0
		self.SN_CAR5 = 0
		self.MA_CAR5 = ""
		self.MA_CAR5_SZ = [0, 0]

		self.CAR6_X = 77.3 * self.MASHTAB #X машины на 6 линии
		self.CAR6_Z = 0 #X машины на 6 линии
		self.IS_CAR6 = 0
		self.SN_CAR6 = 0
		self.MA_CAR6 = ""
		self.MA_CAR6_SZ = [0, 0]

		self.CAR7_X = 91.3 * self.MASHTAB #X машины на 7 линии
		self.CAR7_Z = 0 #X машины на 7 линии
		self.IS_CAR7 = 0
		self.SN_CAR7 = 0
		self.MA_CAR7 = ""
		self.MA_CAR7_SZ = [0, 0]

		self.CAR8_X = 105.3 * self.MASHTAB #X машины на 8 линии
		self.CAR8_Z = 0 #X машины на 8 линии
		self.IS_CAR8 = 0
		self.SN_CAR8 = 0
		self.MA_CAR8 = ""
		self.MA_CAR8_SZ = [0, 0]

		self.CAR9_X = 119 * self.MASHTAB #X машины на 9 линии
		self.CAR9_Z = 0 #X машины на 9 линии
		self.IS_CAR9 = 0
		self.SN_CAR9 = 0
		self.MA_CAR9 = ""
		self.MA_CAR9_SZ = [0, 0]

		self.BG1_X = 0 #Координата бг 1 по оси X
		self.BG1_Z = self.screensize[0] - self.screensize[0] * 2 + 35 * self.MASHTAB #Координата бг 1 по оси Z

		self.BG2_X = 0 #Координата бг 2 по оси X
		self.BG2_Z = 0 #Координата бг 2 по оси Z

		#Машина 1
		self.CAR1_SRFC = pygame.Surface(self.MA_CAR1_SZ, pygame.SRCALPHA, 32)
		self.CAR1_RECT = self.CAR1_SRFC.get_rect()
		self.CAR1_RECT.x = self.CAR1_X
		self.CAR1_RECT.y = self.CAR1_Z
		#Машина 2
		self.CAR2_SRFC = pygame.Surface(self.MA_CAR2_SZ, pygame.SRCALPHA, 32)
		self.CAR2_RECT = self.CAR2_SRFC.get_rect()
		self.CAR2_RECT.x = self.CAR2_X
		self.CAR2_RECT.y = self.CAR2_Z
		#Машина 3
		self.CAR3_SRFC = pygame.Surface(self.MA_CAR3_SZ, pygame.SRCALPHA, 32)
		self.CAR3_RECT = self.CAR3_SRFC.get_rect()
		self.CAR3_RECT.x = self.CAR3_X
		self.CAR3_RECT.y = self.CAR3_Z
		#Машина 4
		self.CAR4_SRFC = pygame.Surface(self.MA_CAR4_SZ, pygame.SRCALPHA, 32)
		self.CAR4_RECT = self.CAR4_SRFC.get_rect()
		self.CAR4_RECT.x = self.CAR4_X
		self.CAR4_RECT.y = self.CAR4_Z
		#Машина 5
		self.CAR5_SRFC = pygame.Surface(self.MA_CAR5_SZ, pygame.SRCALPHA, 32)
		self.CAR5_RECT = self.CAR5_SRFC.get_rect()
		self.CAR5_RECT.x = self.CAR5_X
		self.CAR5_RECT.y = self.CAR5_Z
		#Машина 6
		self.CAR6_SRFC = pygame.Surface(self.MA_CAR6_SZ, pygame.SRCALPHA, 32)
		self.CAR6_RECT = self.CAR6_SRFC.get_rect()
		self.CAR6_RECT.x = self.CAR6_X
		self.CAR6_RECT.y = self.CAR6_Z
		#Машина 7
		self.CAR7_SRFC = pygame.Surface(self.MA_CAR7_SZ, pygame.SRCALPHA, 32)
		self.CAR7_RECT = self.CAR7_SRFC.get_rect()
		self.CAR7_RECT.x = self.CAR7_X
		self.CAR7_RECT.y = self.CAR7_Z
		#Машина 8
		self.CAR8_SRFC = pygame.Surface(self.MA_CAR8_SZ, pygame.SRCALPHA, 32)
		self.CAR8_RECT = self.CAR8_SRFC.get_rect()
		self.CAR8_RECT.x = self.CAR8_X
		self.CAR8_RECT.y = self.CAR8_Z
		#Машина 9
		self.CAR9_SRFC = pygame.Surface(self.MA_CAR9_SZ, pygame.SRCALPHA, 32)
		self.CAR9_RECT = self.CAR9_SRFC.get_rect()
		self.CAR9_RECT.x = self.CAR9_X
		self.CAR9_RECT.y = self.CAR9_Z
		#Машина игрока
		self.PLAYER_CAR_SRFC = pygame.Surface(self.SPORT_VAZ_PNG_SIZE, pygame.SRCALPHA, 32)
		self.PLAYER_CAR_RECT = self.PLAYER_CAR_SRFC.get_rect()
		self.PLAYER_CAR_SRFC.blit(self.SPORT_VAZ_PNG, (0, 0))
		#Машина 2 игрока
		self.PLAYER2_CAR_SRFC = pygame.Surface(self.POLICE_VAZ_PNG_SIZE, pygame.SRCALPHA, 32)
		self.PLAYER2_CAR_RECT = self.PLAYER2_CAR_SRFC.get_rect()
		self.PLAYER2_CAR_SRFC.blit(self.POLICE_VAZ_PNG, (0, 0))

		#self.PLAYER_CAR_RECT.x = self.PLAYER_CAR_X
		#self.PLAYER_CAR_RECT.y = self.PLAYER_CAR_Y

	def XSIZE(self):
		#Дорога
		self.BACKGROUND_PNG = pygame.transform.scale(self.BACKGROUND_PNG, (int(self.BACKGROUND_PNG.get_width()) * self.MASHTAB, int(self.BACKGROUND_PNG.get_height()) * self.MASHTAB))
		self.BACKGROUND_PNG_SIZE = [self.BACKGROUND_PNG.get_width(), self.BACKGROUND_PNG.get_height()]
		#Тролебусы
		self.AQUA_TROLLEBUS_PNG = pygame.transform.scale(self.AQUA_TROLLEBUS_PNG, (int(self.AQUA_TROLLEBUS_PNG.get_width()) * self.MASHTAB, int(self.AQUA_TROLLEBUS_PNG.get_height()) * self.MASHTAB))
		self.AQUA_TROLLEBUS_PNG_SIZE = [self.AQUA_TROLLEBUS_PNG.get_width(), self.AQUA_TROLLEBUS_PNG.get_height()]
		self.GRAY_TROLLEBUS_PNG = pygame.transform.scale(self.GRAY_TROLLEBUS_PNG, (int(self.GRAY_TROLLEBUS_PNG.get_width()) * self.MASHTAB, int(self.GRAY_TROLLEBUS_PNG.get_height()) * self.MASHTAB))
		self.GRAY_TROLLEBUS_PNG_SIZE = [self.GRAY_TROLLEBUS_PNG.get_width(), self.GRAY_TROLLEBUS_PNG.get_height()]
		self.LIME_TROLLEBUS_PNG = pygame.transform.scale(self.LIME_TROLLEBUS_PNG, (int(self.LIME_TROLLEBUS_PNG.get_width()) * self.MASHTAB, int(self.LIME_TROLLEBUS_PNG.get_height()) * self.MASHTAB))
		self.LIME_TROLLEBUS_PNG_SIZE = [self.LIME_TROLLEBUS_PNG.get_width(), self.LIME_TROLLEBUS_PNG.get_height()]

		#Машины
		self.AQUA_VAZ_PNG = pygame.transform.scale(self.AQUA_VAZ_PNG, (int(self.AQUA_VAZ_PNG.get_width()) * self.MASHTAB, int(self.AQUA_VAZ_PNG.get_height()) * self.MASHTAB))
		self.AQUA_VAZ_PNG_SIZE = [self.AQUA_VAZ_PNG.get_width(), self.AQUA_VAZ_PNG.get_height()]
		self.LIME_VAZ_PNG = pygame.transform.scale(self.LIME_VAZ_PNG, (int(self.LIME_VAZ_PNG.get_width()) * self.MASHTAB, int(self.LIME_VAZ_PNG.get_height()) * self.MASHTAB))
		self.LIME_VAZ_PNG_SIZE = [self.LIME_VAZ_PNG.get_width(), self.LIME_VAZ_PNG.get_height()]
		self.WHITE_VAZ_PNG = pygame.transform.scale(self.WHITE_VAZ_PNG, (int(self.WHITE_VAZ_PNG.get_width()) * self.MASHTAB, int(self.WHITE_VAZ_PNG.get_height()) * self.MASHTAB))
		self.WHITE_VAZ_PNG_SIZE = [self.WHITE_VAZ_PNG.get_width(), self.WHITE_VAZ_PNG.get_height()]
		self.POLICE_VAZ_PNG = pygame.transform.scale(self.POLICE_VAZ_PNG, (int(self.POLICE_VAZ_PNG.get_width()) * self.MASHTAB, int(self.POLICE_VAZ_PNG.get_height()) * self.MASHTAB))
		self.POLICE_VAZ_PNG_SIZE = [self.POLICE_VAZ_PNG.get_width(), self.POLICE_VAZ_PNG.get_height()]
		self.SPORT_VAZ_PNG = pygame.transform.scale(self.SPORT_VAZ_PNG, (int(self.SPORT_VAZ_PNG.get_width()) * self.MASHTAB, int(self.SPORT_VAZ_PNG.get_height()) * self.MASHTAB))
		self.SPORT_VAZ_PNG_SIZE = [self.SPORT_VAZ_PNG.get_width(), self.SPORT_VAZ_PNG.get_height()]
		self.GAZELL_PNG = pygame.transform.scale(self.GAZELL_PNG, (int(self.GAZELL_PNG.get_width()) * self.MASHTAB, int(self.GAZELL_PNG.get_height()) * self.MASHTAB))
		self.GAZELL_PNG_SIZE = [self.GAZELL_PNG.get_width(), self.GAZELL_PNG.get_height()]

	def TextDraw(self, text, size, color, cord, surface):
		font = pygame.font.Font(self.GAME_FONT, size) #Создание фонт обьекта
		text = font.render(text, True, color) #создание текст обьекта для отрисовки
		surface.blit(text, cord) #отрисовка на указанном surface

	def PlayerMoveTo(self, to):
		if to == "LEFT": #Едем в лево
			self.PLAYER_CAR_X -= self.PLAYER_SPEED_OTH
			#self.PLAYER_CAR_SRFC = pygame.transform.rotate(self.PLAYER_CAR_SRFC, 0.1)
		if to == "RIGHT": #Едем в право
			self.PLAYER_CAR_X += self.PLAYER_SPEED_OTH
			#self.PLAYER_CAR_SRFC = pygame.transform.rotate(self.PLAYER_CAR_SRFC, -0.1)
		if to == "P2LEFT":
			self.PLAYER2_CAR_X -= self.PLAYER_SPEED_OTH
		if to == "P2RIGHT":
			self.PLAYER2_CAR_X += self.PLAYER_SPEED_OTH

	def AnimatedBackground(self):
		#Start
		self.PLAYER_UNLOCK_CONTROLS = 1
		self.CAN_GENERATEMACHINES = 1

		if self.PLAYER_UNLOCK_CONTROLS:
			self.PLAYER_SCORE += 1

		self.BG1_Z += self.PLAYER_SPEED
		self.BG2_Z += self.PLAYER_SPEED

		if (self.BG1_Z + self.screensize[0] >= self.screensize[0]):
			self.BG1_Z = self.screensize[0] - self.screensize[0] * 2 + 35 * self.MASHTAB
			self.BG2_Z = 0

		#End
		self.screen.blit(self.BACKGROUND_PNG, (self.BG1_X, self.BG1_Z))
		self.screen.blit(self.BACKGROUND_PNG, (self.BG2_X, self.BG2_Z))

	def MachinePosGenerate(self):
		generatedpos = 0
		self.CAR1_SRFC = pygame.Surface(self.MA_CAR1_SZ, pygame.SRCALPHA, 32)
		self.CAR1_RECT = self.CAR1_SRFC.get_rect()
		self.CAR2_SRFC = pygame.Surface(self.MA_CAR2_SZ, pygame.SRCALPHA, 32)
		self.CAR2_RECT = self.CAR2_SRFC.get_rect()
		self.CAR3_SRFC = pygame.Surface(self.MA_CAR3_SZ, pygame.SRCALPHA, 32)
		self.CAR3_RECT = self.CAR3_SRFC.get_rect()
		self.CAR4_SRFC = pygame.Surface(self.MA_CAR4_SZ, pygame.SRCALPHA, 32)
		self.CAR4_RECT = self.CAR4_SRFC.get_rect()
		self.CAR5_SRFC = pygame.Surface(self.MA_CAR5_SZ, pygame.SRCALPHA, 32)
		self.CAR5_RECT = self.CAR5_SRFC.get_rect()
		self.CAR6_SRFC = pygame.Surface(self.MA_CAR6_SZ, pygame.SRCALPHA, 32)
		self.CAR6_RECT = self.CAR6_SRFC.get_rect()
		self.CAR7_SRFC = pygame.Surface(self.MA_CAR7_SZ, pygame.SRCALPHA, 32)
		self.CAR7_RECT = self.CAR7_SRFC.get_rect()
		self.CAR8_SRFC = pygame.Surface(self.MA_CAR8_SZ, pygame.SRCALPHA, 32)
		self.CAR8_RECT = self.CAR8_SRFC.get_rect()
		self.CAR9_SRFC = pygame.Surface(self.MA_CAR9_SZ, pygame.SRCALPHA, 32)
		self.CAR9_RECT = self.CAR9_SRFC.get_rect()
		if self.CAN_GENERATEMACHINES:
			#Машина 1
			if self.IS_CAR1 != 1:
				self.IS_CAR1 = 1
				result = randint(0, self.MACHINES)
				self.MA_CAR1 = self.MACHINES_TO_RAND[result]
				self.MA_CAR1_SZ = self.SZ_MACHINES_TO_RAND[result]
				self.SN_CAR1 = result
				generatedpos = randint(self.F_GN, self.S_GN)
				self.CAR1_Z = generatedpos - generatedpos * 2
			if self.IS_CAR1:
				self.CAR1_Z += self.PLAYER_SPEED
				if self.CAR1_Z >= self.screensize[0]:
					self.IS_CAR1 = 0
			#Машина 2
			if self.IS_CAR2 != 1:
				self.IS_CAR2 = 1
				result = randint(0, self.MACHINES)
				self.MA_CAR2 = self.MACHINES_TO_RAND[result]
				self.MA_CAR2_SZ = self.SZ_MACHINES_TO_RAND[result]
				self.SN_CAR2 = result
				generatedpos = randint(self.F_GN, self.S_GN)
				self.CAR2_Z = generatedpos - generatedpos * 2
			if self.IS_CAR2:
				self.CAR2_Z += self.PLAYER_SPEED
				if self.CAR2_Z >= self.screensize[0]:
					self.IS_CAR2 = 0
			#Машина 3
			if self.IS_CAR3 != 1:
				self.IS_CAR3 = 1
				result = randint(0, self.MACHINES)
				self.MA_CAR3 = self.MACHINES_TO_RAND[result]
				self.MA_CAR3_SZ = self.SZ_MACHINES_TO_RAND[result]
				self.SN_CAR3 = result
				generatedpos = randint(self.F_GN, self.S_GN)
				self.CAR3_Z = generatedpos - generatedpos * 2
			if self.IS_CAR3:
				self.CAR3_Z += self.PLAYER_SPEED
				if self.CAR3_Z >= self.screensize[0]:
					self.IS_CAR3 = 0
			#Машина 4
			if self.IS_CAR4 != 1:
				self.IS_CAR4 = 1
				result = randint(0, self.MACHINES)
				self.MA_CAR4 = self.MACHINES_TO_RAND[result]
				self.MA_CAR4_SZ = self.SZ_MACHINES_TO_RAND[result]
				self.SN_CAR4 = result
				generatedpos = randint(self.F_GN, self.S_GN)
				self.CAR4_Z = generatedpos - generatedpos * 2
			if self.IS_CAR4:
				self.CAR4_Z += self.PLAYER_SPEED
				if self.CAR4_Z >= self.screensize[0]:
					self.IS_CAR4 = 0
			#Машина 5
			if self.IS_CAR5 != 1:
				self.IS_CAR5 = 1
				result = randint(0, self.MACHINES)
				self.MA_CAR5 = self.MACHINES_TO_RAND[result]
				self.MA_CAR5_SZ = self.SZ_MACHINES_TO_RAND[result]
				self.SN_CAR5 = result
				generatedpos = randint(self.F_GN, self.S_GN)
				self.CAR5_Z = generatedpos - generatedpos * 2
			if self.IS_CAR5:
				self.CAR5_Z += self.PLAYER_SPEED
				if self.CAR5_Z >= self.screensize[0]:
					self.IS_CAR5 = 0
			#Машина 6
			if self.IS_CAR6 != 1:
				self.IS_CAR6 = 1
				result = randint(0, self.MACHINES)
				self.MA_CAR6 = self.MACHINES_TO_RAND[result]
				self.MA_CAR6_SZ = self.SZ_MACHINES_TO_RAND[result]
				self.SN_CAR6 = result
				generatedpos = randint(self.F_GN, self.S_GN)
				self.CAR6_Z = generatedpos - generatedpos * 2
			if self.IS_CAR6:
				self.CAR6_Z += self.PLAYER_SPEED
				if self.CAR6_Z >= self.screensize[0]:
					self.IS_CAR6 = 0
			#Машина 7
			if self.IS_CAR7 != 1:
				self.IS_CAR7 = 1
				result = randint(0, self.MACHINES)
				self.MA_CAR7 = self.MACHINES_TO_RAND[result]
				self.MA_CAR7_SZ = self.SZ_MACHINES_TO_RAND[result]
				self.SN_CAR7 = result
				generatedpos = randint(self.F_GN, self.S_GN)
				self.CAR7_Z = generatedpos - generatedpos * 2
			if self.IS_CAR7:
				self.CAR7_Z += self.PLAYER_SPEED
				if self.CAR7_Z >= self.screensize[0]:
					self.IS_CAR7 = 0
			#Машина 8
			if self.IS_CAR8 != 1:
				self.IS_CAR8 = 1
				result = randint(0, self.MACHINES)
				self.MA_CAR8 = self.MACHINES_TO_RAND[result]
				self.MA_CAR8_SZ = self.SZ_MACHINES_TO_RAND[result]
				self.SN_CAR8 = result
				generatedpos = randint(self.F_GN, self.S_GN)
				self.CAR8_Z = generatedpos - generatedpos * 2
			if self.IS_CAR8:
				self.CAR8_Z += self.PLAYER_SPEED
				if self.CAR8_Z >= self.screensize[0]:
					self.IS_CAR8 = 0
			#Машина 9
			if self.IS_CAR9 != 1:
				self.IS_CAR9 = 1
				result = randint(0, self.MACHINES)
				self.MA_CAR9 = self.MACHINES_TO_RAND[result]
				self.MA_CAR9_SZ = self.SZ_MACHINES_TO_RAND[result]
				self.SN_CAR9 = result
				generatedpos = randint(self.F_GN, self.S_GN)
				self.CAR9_Z = generatedpos - generatedpos * 2
			if self.IS_CAR9:
				self.CAR9_Z += self.PLAYER_SPEED
				if self.CAR9_Z >= self.screensize[0]:
					self.IS_CAR9 = 0

			#Отрисовка
			self.CAR1_SRFC.blit(self.MA_CAR1, (0, 0))
			self.screen.blit(self.CAR1_SRFC, (self.CAR1_X, self.CAR1_Z))
			self.CAR2_SRFC.blit(self.MA_CAR2, (0, 0))
			self.screen.blit(self.CAR2_SRFC, (self.CAR2_X, self.CAR2_Z))
			self.CAR3_SRFC.blit(self.MA_CAR3, (0, 0))
			self.screen.blit(self.CAR3_SRFC, (self.CAR3_X, self.CAR3_Z))
			self.CAR4_SRFC.blit(self.MA_CAR4, (0, 0))
			self.screen.blit(self.CAR4_SRFC, (self.CAR4_X, self.CAR4_Z))
			self.CAR5_SRFC.blit(self.MA_CAR5, (0, 0))
			self.screen.blit(self.CAR5_SRFC, (self.CAR5_X, self.CAR5_Z))
			self.CAR6_SRFC.blit(self.MA_CAR6, (0, 0))
			self.screen.blit(self.CAR6_SRFC, (self.CAR6_X, self.CAR6_Z))
			self.CAR7_SRFC.blit(self.MA_CAR7, (0, 0))
			self.screen.blit(self.CAR7_SRFC, (self.CAR7_X, self.CAR7_Z))
			self.CAR8_SRFC.blit(self.MA_CAR8, (0, 0))
			self.screen.blit(self.CAR8_SRFC, (self.CAR8_X, self.CAR8_Z))
			self.CAR9_SRFC.blit(self.MA_CAR9, (0, 0))
			self.screen.blit(self.CAR9_SRFC, (self.CAR9_X, self.CAR9_Z))
# and self.PLAYER_CAR_Y == self.CAR1_Z
	def ColliderOfMachines(self):
		#Машина 1
		self.CAR1_RECT.x = self.CAR1_X
		self.CAR1_RECT.y = self.CAR1_Z
		#Машина 2
		self.CAR2_RECT.x = self.CAR2_X
		self.CAR2_RECT.y = self.CAR2_Z
		#Машина 3
		self.CAR3_RECT.x = self.CAR3_X
		self.CAR3_RECT.y = self.CAR3_Z
		#Машина 4
		self.CAR4_RECT.x = self.CAR4_X
		self.CAR4_RECT.y = self.CAR4_Z
		#Машина 5
		self.CAR5_RECT.x = self.CAR5_X
		self.CAR5_RECT.y = self.CAR5_Z
		#Машина 6
		self.CAR6_RECT.x = self.CAR6_X
		self.CAR6_RECT.y = self.CAR6_Z
		#Машина 7
		self.CAR7_RECT.x = self.CAR7_X
		self.CAR7_RECT.y = self.CAR7_Z
		#Машина 8
		self.CAR8_RECT.x = self.CAR8_X
		self.CAR8_RECT.y = self.CAR8_Z
		#Машина 9
		self.CAR9_RECT.x = self.CAR9_X
		self.CAR9_RECT.y = self.CAR9_Z
		#Машина игрока
		self.PLAYER_CAR_RECT.x = self.PLAYER_CAR_X
		self.PLAYER_CAR_RECT.y = self.PLAYER_CAR_Y
		#Машина 2 игрока
		self.PLAYER2_CAR_RECT.x = self.PLAYER2_CAR_X
		self.PLAYER2_CAR_RECT.y = self.PLAYER2_CAR_Z

		#self.POLICE_CAR_X = self.PLAYER2_CAR_X
		#self.POLICE_CAR_Z = self.PLAYER_CAR_Y + self.POLICE_VAZ_PNG_SIZE[1] + 30

		#Обработка столкновенний
		collide1 = pygame.Rect.colliderect(self.PLAYER_CAR_RECT, self.CAR1_RECT)
		collide2 = pygame.Rect.colliderect(self.PLAYER_CAR_RECT, self.CAR2_RECT)
		collide3 = pygame.Rect.colliderect(self.PLAYER_CAR_RECT, self.CAR3_RECT)
		collide4 = pygame.Rect.colliderect(self.PLAYER_CAR_RECT, self.CAR4_RECT)
		collide5 = pygame.Rect.colliderect(self.PLAYER_CAR_RECT, self.CAR5_RECT)
		collide6 = pygame.Rect.colliderect(self.PLAYER_CAR_RECT, self.CAR6_RECT)
		collide7 = pygame.Rect.colliderect(self.PLAYER_CAR_RECT, self.CAR7_RECT)
		collide8 = pygame.Rect.colliderect(self.PLAYER_CAR_RECT, self.CAR8_RECT)
		collide9 = pygame.Rect.colliderect(self.PLAYER_CAR_RECT, self.CAR9_RECT)
		if self.GAME_TYPE == "2P":
			p2collide1 = pygame.Rect.colliderect(self.PLAYER2_CAR_RECT, self.CAR1_RECT)
			p2collide2 = pygame.Rect.colliderect(self.PLAYER2_CAR_RECT, self.CAR2_RECT)
			p2collide3 = pygame.Rect.colliderect(self.PLAYER2_CAR_RECT, self.CAR3_RECT)
			p2collide4 = pygame.Rect.colliderect(self.PLAYER2_CAR_RECT, self.CAR4_RECT)
			p2collide5 = pygame.Rect.colliderect(self.PLAYER2_CAR_RECT, self.CAR5_RECT)
			p2collide6 = pygame.Rect.colliderect(self.PLAYER2_CAR_RECT, self.CAR6_RECT)
			p2collide7 = pygame.Rect.colliderect(self.PLAYER2_CAR_RECT, self.CAR7_RECT)
			p2collide8 = pygame.Rect.colliderect(self.PLAYER2_CAR_RECT, self.CAR8_RECT)
			p2collide9 = pygame.Rect.colliderect(self.PLAYER2_CAR_RECT, self.CAR9_RECT)

			collideplayers = pygame.Rect.colliderect(self.PLAYER_CAR_RECT, self.PLAYER2_CAR_RECT)
		if collide1:
			self.running = 0
			self.GameOverScreen()
		if collide2:
			self.running = 0
			self.GameOverScreen()
		if collide3:
			self.running = 0
			self.GameOverScreen()
		if collide4:
			self.running = 0
			self.GameOverScreen()
		if collide5:
			self.running = 0
			self.GameOverScreen()
		if collide6:
			self.running = 0
			self.GameOverScreen()
		if collide7:
			self.running = 0
			self.GameOverScreen()
		if collide8:
			self.running = 0
			self.GameOverScreen()
		if collide9:
			self.running = 0
			self.GameOverScreen()

		if self.GAME_TYPE == "2P":
			if p2collide1:
				self.running = 0
				self.GameOverScreen()
			if p2collide2:
				self.running = 0
				self.GameOverScreen()
			if p2collide3:
				self.running = 0
				self.GameOverScreen()
			if p2collide4:
				self.running = 0
				self.GameOverScreen()
			if p2collide5:
				self.running = 0
				self.GameOverScreen()
			if p2collide6:
				self.running = 0
				self.GameOverScreen()
			if p2collide7:
				self.running = 0
				self.GameOverScreen()
			if p2collide8:
				self.running = 0
				self.GameOverScreen()
			if p2collide9:
				self.running = 0
				self.GameOverScreen()

			if collideplayers:
				self.running = 0
				self.GameOverScreen()

	def console(self):
		if self.CONSOLE_ENABLED:
			#self.screen.fill((255, 255, 255))
			self.TextDraw("Console opened. Check you executable window", 12, (255, 255, 255), (0, 0), self.screen)
			pygame.display.flip()
			print("Welcome to game console! To exit from console write exit")
			while True:
				consoleinput = str(input(">"))
				if consoleinput == "CTXP!":
					print("Hmm... Hmm? Hmm Hmm!")
				if consoleinput == "cookie":
					print("ХРАЗ, будешь печеньку?")
				if consoleinput == "enablecollision":
					self.PLAYER_COLLISION = 1
					print("Collision Enabled!")
				if consoleinput == "disablecollision":
					self.PLAYER_COLLISION = 0
					print("Collision Disabled!")
				if consoleinput == "enabledebug":
					self.DEBUG_TEXT_ENABLE = 1
					print("DEBUG TEXT ENABLED")
				if consoleinput == "disabledebug":
					self.DEBUG_TEXT_ENABLE = 0
					print("DEBUG TEXT DISABLED")
				if consoleinput == "setspeed":
					print("Write to console you speed value")
					while True:
						try:
							valinput = int(input("Val>"))
							self.PLAYER_SPEED = valinput
							print(f"Player speed set:{valinput}")
							break
						except ValueError:
							print("it must be a value!")
				if consoleinput == "gameexit":
					pygame.quit()
					sys.exit()
				if consoleinput == "exit":
					print("Exit to game...")
					break

	def MainMenu(self):
		self.Values()
		self.running = 1
		while True:
			self.AnimatedBackground()
			#self.TextDraw(f"FPS:{str(int(self.clock.get_fps()))}", 8, (0, 0, 0), (0, 0), self.screen)
			#self.TextDraw(f"MOUSE_POSITION:{str(pygame.mouse.get_pos())}", 8, (0, 0, 0), (0, 8), self.screen)
			self.TextDraw(f"Лютый Гонщик", 8 * self.MASHTAB, (255, 30, 0), (20 * self.MASHTAB, 23 * self.MASHTAB), self.screen)
			self.TextDraw(f"1 - 1 Игрок         2 - 2 Игрока", 3 * self.MASHTAB, (255, 255, 30), (19 * self.MASHTAB, 68 * self.MASHTAB), self.screen)
			self.TextDraw(f"By AltTeam", 3 * self.MASHTAB, (255, 255, 255), (0, self.screensize[1] - 3 * self.MASHTAB), self.screen)
			
			KEYS=pygame.key.get_pressed()
			if KEYS[pygame.K_1]:
				self.running = 0
				self.GAME_TYPE = "1P"
				self.MainScene()
			if KEYS[pygame.K_2]:
				self.running = 0
				self.GAME_TYPE = "2P"
				self.MainScene()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			pygame.display.flip()
			self.clock.tick(self.FPS)

	def MainScene(self):
		self.Values()
		self.running = 1
		if self.SOUND_OFF != 1:
			self.CAR_POLICE.play(loops=-1)
			self.CAR_MOVE.play(loops=-1)
		while self.running:
			KEYS=pygame.key.get_pressed()
			if KEYS[pygame.K_ESCAPE]:
				self.Pause()

			self.screen.fill((255, 255, 255))
			self.AnimatedBackground()
			self.MachinePosGenerate()
			if self.PLAYER_COLLISION:
				self.ColliderOfMachines()

			self.screen.blit(self.PLAYER_CAR_SRFC, (self.PLAYER_CAR_X, self.PLAYER_CAR_Y))
			if self.GAME_TYPE == "2P":
				self.screen.blit(self.PLAYER2_CAR_SRFC, (self.PLAYER2_CAR_X, self.PLAYER2_CAR_Z))

			if self.DEBUG_TEXT_ENABLE:
				self.TextDraw(f"FPS:{str(int(self.clock.get_fps()))}", 8, (0, 0, 0), (0, 0), self.screen)
				self.TextDraw(f"MOUSE_POSITION:{str(pygame.mouse.get_pos())}", 8, (0, 0, 0), (0, 8), self.screen)
			if self.SOUND_OFF:
				self.TextDraw(f"Звук Выключен", 3 * self.MASHTAB, (255, 0, 0), (0, self.screensize[1] - 3 * self.MASHTAB - 3 * self.MASHTAB), self.screen)
			self.TextDraw(f"Очки:{self.PLAYER_SCORE}", 3 * self.MASHTAB, (0, 180, 0), (0, self.screensize[1] - 3 * self.MASHTAB), self.screen)

			#KEYS=pygame.key.get_pressed()
			if self.PLAYER_UNLOCK_CONTROLS == 1:
				if KEYS[self.KEY_LEFT] and self.PLAYER_CAR_X > 0:
					self.PlayerMoveTo("LEFT")
				if KEYS[self.KEY_RIGHT] and self.PLAYER_CAR_X < self.screensize[0] - self.SPORT_VAZ_PNG_SIZE[0] - 1:
					self.PlayerMoveTo("RIGHT")
				if self.SOUND_OFF:
					if KEYS[pygame.K_F2]:
						self.SOUND_OFF = 0
						self.CAR_POLICE.play(loops=-1)
						self.CAR_MOVE.play(loops=-1)	
				if self.SOUND_OFF != 1:
					if KEYS[pygame.K_F1]:
						self.SOUND_OFF = 1
						self.CAR_POLICE.stop()
						self.CAR_MOVE.stop()
				#if KEYS[pygame.BACKSPACE]:
					#break
				if self.GAME_TYPE == "2P":
					if KEYS[self.P2_KEY_LEFT] and self.PLAYER2_CAR_X > 0:
						self.PlayerMoveTo("P2LEFT")
					if KEYS[self.P2_KEY_RIGHT] and self.PLAYER2_CAR_X < self.screensize[0] - self.SPORT_VAZ_PNG_SIZE[0] - 1:
						self.PlayerMoveTo("P2RIGHT")

				if KEYS[pygame.K_BACKQUOTE]:
					self.console()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			pygame.display.flip()
			self.clock.tick(self.FPS)
		#self.MainMenu()

	def Pause(self):
		if self.SOUND_OFF != 1:
			self.CAR_POLICE.stop()
			self.CAR_MOVE.stop()
		while True:
			self.TextDraw(f"Game Paused(ENTER - Return)", 3 * self.MASHTAB, (255, 255, 255), (0, 0), self.screen)
			KEYS=pygame.key.get_pressed()
			if KEYS[pygame.K_RETURN]:
				if self.SOUND_OFF != 1:
					self.CAR_POLICE.play(loops=-1)
					self.CAR_MOVE.play(loops=-1)
				break

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			pygame.display.flip()
			self.clock.tick(self.FPS)

	def GameOverScreen(self):
		self.running = 1
		if self.SOUND_OFF != 1:
			self.CAR_MOVE.stop()
			self.CAR_POLICE.stop()
			self.CAR_CRASH.play()
		if self.PLAYER_SCORE > self.MAX_SCORE:
			self.MAX_SCORE = self.PLAYER_SCORE
		while self.running:
			self.screen.fill((255, 255, 255))
			self.TextDraw(f"Game Over!", 3*4 * self.MASHTAB, (0, 0, 0), (10.5 * self.MASHTAB, 23 * self.MASHTAB), self.screen)
			self.TextDraw(f"Ваши очки:{self.PLAYER_SCORE}", 3 * self.MASHTAB, (0, 0, 0), (46 * self.MASHTAB, 37 * self.MASHTAB), self.screen)
			self.TextDraw(f"Рекорд:{self.MAX_SCORE}", 3 * self.MASHTAB, (0, 0, 0), (46 * self.MASHTAB, 41.5 * self.MASHTAB), self.screen)
			self.TextDraw(f'Нажмите "Enter" для начала новой игры.', 3 * self.MASHTAB, (0, 0, 0), (11.5 * self.MASHTAB, 75 * self.MASHTAB), self.screen)

			KEYS=pygame.key.get_pressed()
			if KEYS[pygame.K_RETURN]:
				self.running = 0
				self.CAR_CRASH.stop()
				self.MainScene()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			pygame.display.flip()
			self.clock.tick(self.FPS)

if __name__ == "__main__":
	game = Game()