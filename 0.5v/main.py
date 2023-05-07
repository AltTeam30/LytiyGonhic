#Либы
import pygame
import sys, time, os
from random import randint
from pypresence import Presence
#Всякое нужное
from labels import *
#Инициализация либ
pygame.init() #Инициализация пайгеим
pygame.mixer.init(channels=12) #Инициализация pygame.mixer и установка ограничения 12 канала

#Класс кнопки, в обьяснение он не нуждается.
class Button:
	def __init__(self, ADDXY, surf, BUTTON, MASHTAB, ACT):
		self.PATH = os.path.abspath(".")+'/'
		#MASHTAB_FILE = open(f"{self.PATH}options/mashtab.txt", "r")
		self.MASHTAB = MASHTAB
		#MASHTAB_FILE.close()
		self.BUTT = BUTTON
		self.ADDX, self.ADDY = ADDXY
		self.colors = BUTTON_COLORS
		self.surface = surf
		self.comm = ACT
		
		self.onePress = 0
		self.alreadyPressed = 0

		self.ButtonSurface = pygame.Surface((self.BUTT[2] * self.MASHTAB, self.BUTT[3] * self.MASHTAB))
		self.ButtonRect = self.ButtonSurface.get_rect()
		self.ButtonRect.x = self.BUTT[4]*self.MASHTAB+self.ADDX
		self.ButtonRect.y = self.BUTT[5]*self.MASHTAB+self.ADDY
		self.MouseSurface = pygame.Surface((1, 1))
		self.MouseRect = self.MouseSurface.get_rect()

		font = pygame.font.Font(f"{self.PATH}{FONT}", 3 * self.MASHTAB)
		self.ButtonText = font.render(self.BUTT[0], 1, (0, 0, 0))
	
	def tick(self):
		#print(stpos)
		MX, MY = pygame.mouse.get_pos()
		self.MouseRect.x = MX
		self.MouseRect.y = MY
		MCOLLIDE = pygame.Rect.colliderect(self.MouseRect, self.ButtonRect)
		MPRESS = pygame.mouse.get_pressed()[0]
		self.ButtonSurface.fill(self.colors[0])

		if MCOLLIDE:
			self.ButtonSurface.fill(self.colors[1])
			if self.BUTT[1] == "ONECL":
				if MPRESS:
					self.ButtonSurface.fill(self.colors[2])
					if self.onePress:
						self.comm()
					elif not self.alreadyPressed:
						self.comm()
						self.alreadyPressed = 1
				else:
					self.alreadyPressed = 0
			if self.BUTT[1] == "MULTI":
				if MPRESS:
					self.ButtonSurface.fill(self.colors[2])
					self.comm()

		self.ButtonSurface.blit(self.ButtonText, (self.ButtonRect.width/2 - self.ButtonText.get_rect().width/2, self.ButtonRect.height/2 - self.ButtonText.get_rect().height/2))
		self.surface.blit(self.ButtonSurface, (self.ButtonRect.x, self.ButtonRect.y))

#Класс игры, в нём происходят основные действия.
class Game:
	def __init__(self):
		#Гл. Настройки

		self.PATH = os.path.abspath(".")+'/'

		print(f"Game path:{self.PATH}")

		mashtab_fromfile = open(f"{self.PATH}options/mashtab.txt", "r")
		defsoundmode_fromfile = open(f"{self.PATH}options/defaultsoundmode.txt", "r")
		fullscreen = open(f"{self.PATH}options/fullscreen.txt", "r")
		sensormode_fromfile = open(f"{self.PATH}options/onscreenplay.txt", "r")

		self.version = "0.5v" #Версия игры
		self.MASHTAB = int(mashtab_fromfile.read()) #Умножение размера текстур (Норма - 5. Нетбуки - 4)
		mashtab_fromfile.close()
		self.screensize = [135 * self.MASHTAB, 100 * self.MASHTAB] #Размер окна (810, 600)
		if int(fullscreen.read()):
			self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF) #Создание окна
			fullscreen.close()
		else:
			fullscreen.close()
			self.screen = pygame.display.set_mode(self.screensize, pygame.DOUBLEBUF) #Создание окна
		self.MAX_SCORE = 0 # Рекорд
		self.GAME_TYPE = "NONE" # 2 игрока - 2P, 1 игрок - 1P
		self.SOUND_OFF = int(defsoundmode_fromfile.read()) #Звук выключен? ?_?
		defsoundmode_fromfile.close()
		self.ALLOW_MOVE_BACKGROUNG = 1
		self.PLAYER_UNLOCK_CONTROLS = 1
		self.CAN_GENERATEMACHINES = 1
		self.CAN_MACHINES_MOVE = 1
		pygame.display.set_caption(f"Лютый Гонщик {self.version}") #Название окна
		pygame.display.set_icon(pygame.image.load(f"{self.PATH}assets/Images/LOGO.png"))
		self.clock = pygame.time.Clock() #Pygame клок
		self.running = 0 #Да.
		self.FPS = 60 #ФиПиЭйС

		self.CONSOLE_ENABLED = 0 #Отвечает за разблокировку консоли игры. Обычно включается во время разработки или в дев. билдах (auto-py-to-exe)
		self.DEBUG_TEXT_ENABLE = 0 #Отвечает за разблокировку дебаг текста
		self.RUN_RPC_ATSTART = 1
		self.SENSORMODE = int(sensormode_fromfile.read())
		sensormode_fromfile.close()

		self.senstemp = self.SENSORMODE

		#Управление
		self.KEY_LEFT = pygame.K_a #Клавиша "ВЛЕВО"
		self.KEY_RIGHT = pygame.K_d #Клавиша "ВПРАВО"
		self.ALT_KEY_LEFT = pygame.K_LEFT #Клавиша "ВЛЕВО"
		self.ALT_KEY_RIGHT = pygame.K_RIGHT #Клавиша "ВПРАВО"

		self.P2_KEY_LEFT = pygame.K_LEFT
		self.P2_KEY_RIGHT = pygame.K_RIGHT

		fullscreen = open(f"{self.PATH}options/fullscreen.txt", "r")

		if int(fullscreen.read()):
			X, Y = pygame.display.get_surface().get_size()
			self.ADDX = X / 2 - self.screensize[0] / 2
			self.ADDY = Y / 2 - self.screensize[1] / 2
			fullscreen.close()
			self.temp1 = 1
		else:
			self.ADDX = 0
			self.ADDY = 0
			fullscreen.close()
			self.temp1 = 0

		self.temp = self.MASHTAB

		#Дорога
		self.BACKGROUND_PNG = pygame.image.load(f"{self.PATH}assets/Images/BACKGROUND.png").convert_alpha()
		self.FREEZE_PNG = pygame.image.load(f"{self.PATH}assets/Images/FREEZE.png").convert_alpha()

		#Текстурка окна GameOver
		self.GAME_OVER_SCREEN = pygame.image.load(f"{self.PATH}assets/Images/GAME_OVER_SCREEN.png").convert_alpha()

		#Тролебусы
		self.AQUA_TROLLEBUS_PNG = pygame.image.load(f"{self.PATH}assets/Images/AQUA_TROLLEBUS.png").convert_alpha()
		self.GRAY_TROLLEBUS_PNG = pygame.image.load(f"{self.PATH}assets/Images/GRAY_TROLLEBUS.png").convert_alpha()
		self.LIME_TROLLEBUS_PNG = pygame.image.load(f"{self.PATH}assets/Images/LIME_TROLLEBUS.png").convert_alpha()
		
		#Машины
		self.AQUA_VAZ_PNG = pygame.image.load(f"{self.PATH}assets/Images/AQUA_VAZ-2107.png").convert_alpha()
		self.LIME_VAZ_PNG = pygame.image.load(f"{self.PATH}assets/Images/LIME_VAZ-2107.png").convert_alpha()
		self.WHITE_VAZ_PNG = pygame.image.load(f"{self.PATH}assets/Images/WHITE_VAZ-2107.png").convert_alpha()
		self.POLICE_VAZ_PNG = pygame.image.load(f"{self.PATH}assets/Images/POLICE_VAZ-2107.png").convert_alpha()
		self.SPORT_VAZ_PNG = pygame.image.load(f"{self.PATH}assets/Images/SPORT_VAZ-2107.png").convert_alpha()
		self.GAZELL_PNG = pygame.image.load(f"{self.PATH}assets/Images/GAZELL.png").convert_alpha()

		#GFX
		self.CAR_CRASH = pygame.mixer.Sound(f"{self.PATH}assets/GFX/CAR_CRASH.ogg")
		self.CAR_POLICE = pygame.mixer.Sound(f"{self.PATH}assets/GFX/POLICE.ogg")
		self.CAR_MOVE = pygame.mixer.Sound(f"{self.PATH}assets/GFX/CAR_MOVE.ogg")
		self.GAME_PAUSE = pygame.mixer.Sound(f"{self.PATH}assets/GFX/GAME_PAUSE.ogg")
		#Game Font
		self.GAME_FONT = f"{self.PATH}assets/GAME_FONT.ttf"

		if self.RUN_RPC_ATSTART:
			try:
				client_id = "1100155001579524246"
				self.RPC = Presence(client_id)
				self.RPC.connect()

				self.RPC.update(state=f"Лютый Гонщик {self.version} by AltTeam.", large_image="icon", buttons=[{"label": "ТГ Игры", "url": "https://t.me/lytigonchic"}])
			except Exception as e:
				print(f"Error while starting a Discord RPC. Exception: {e}")

		self.BUTTON_PRESS = None
		self.BUTTON_EVENT_POS = [0, 0]

		self.XSIZE() #Увеличение размера спрайтов в 4 раза
		self.MACHINES_TO_RAND = [self.AQUA_TROLLEBUS_PNG, self.GRAY_TROLLEBUS_PNG, self.LIME_TROLLEBUS_PNG, self.AQUA_VAZ_PNG, self.LIME_VAZ_PNG, self.WHITE_VAZ_PNG, self.GAZELL_PNG]
		self.SZ_MACHINES_TO_RAND = [self.AQUA_TROLLEBUS_PNG_SIZE, self.GRAY_TROLLEBUS_PNG_SIZE, self.LIME_TROLLEBUS_PNG_SIZE, self.AQUA_VAZ_PNG_SIZE, self.LIME_VAZ_PNG_SIZE, self.WHITE_VAZ_PNG_SIZE, self.GAZELL_PNG_SIZE]
		self.MACHINES = 7-1
		self.Values() #Инициализация игровых переменных
		self.MainMenu()
		#self.TestPolygon() #Запуск игровой сцены

	def Values(self):
		#Переменные 140

		self.needtoexitmainmenu = None

		self.PLAYER_UNLOCK_CONTROLS = 1 #Отвечает за разблокировку управления игроком
		self.PLAYER_COLLISION = 1 #Коллизия игрока
		self.PLAYER_SCORE = 0 #Очки игрока
		self.PLAYER_SPEED = 1.6 * self.MASHTAB #Скорость машины игрока
		self.PLAYER_SPEED_OTH = 0.8 * self.MASHTAB #Скорость машины игрока в направление Лево/Право
		if self.GAME_TYPE == "1P":
			self.PLAYER_CAR_X = 63.3 * self.MASHTAB + self.ADDX #Координата тачки игрока по оси X
			self.PLAYER_CAR_Y = 78 * self.MASHTAB + self.ADDY #Координата тачки игрока по оси Z
			self.PLAYER2_CAR_X = 0 #Координата полицейской тачки по оси X
			self.PLAYER2_CAR_Z = 0 #Координата полицейской тачки по оси Z
		else:
			self.PLAYER_CAR_X = 28 * self.MASHTAB + self.ADDX #Координата тачки игрока по оси X
			self.PLAYER_CAR_Y = 78 * self.MASHTAB + self.ADDY #Координата тачки игрока по оси Z
			self.PLAYER2_CAR_X = 98 * self.MASHTAB + self.ADDX #Координата полицейской тачки по оси X
			self.PLAYER2_CAR_Z = 78 * self.MASHTAB + self.ADDY #Координата полицейской тачки по оси Z

		self.CAN_GENERATEMACHINES = 1 #Могут ли генерироватся машины?
		self.F_GN = 150 * self.MASHTAB + self.ADDY #Минимальная координата спавна машин
		self.S_GN = 550 * self.MASHTAB + self.ADDY #Максимальная координата спавна машин

		self.CAR1_X = 7.26 * self.MASHTAB + self.ADDX #X машины на 1 линии
		self.CAR1_Z = 0 #X машины на 1 линии
		self.IS_CAR1 = 0 
		self.SN_CAR1 = 0
		self.MA_CAR1 = ""
		self.MA_CAR1_SZ = [0, 0]

		self.CAR2_X = 21.25 * self.MASHTAB + self.ADDX #X машины на 2 линии
		self.CAR2_Z = 0 #X машины на 2 линии
		self.IS_CAR2 = 0
		self.SN_CAR2 = 0
		self.MA_CAR2 = ""
		self.MA_CAR2_SZ = [0, 0]

		self.CAR3_X = 35.25 * self.MASHTAB + self.ADDX #X машины на 3 линии
		self.CAR3_Z = 0 #X машины на 3 линии
		self.IS_CAR3 = 0
		self.SN_CAR3 = 0
		self.MA_CAR3 = ""
		self.MA_CAR3_SZ = [0, 0]

		self.CAR4_X = 49.3 * self.MASHTAB + self.ADDX #X машины на 4 линии
		self.CAR4_Z = 0 #X машины на 4 линии
		self.IS_CAR4 = 0
		self.SN_CAR4 = 0
		self.MA_CAR4 = ""
		self.MA_CAR4_SZ = [0, 0]

		self.CAR5_X = 63.3 * self.MASHTAB + self.ADDX #X машины на 5 линии
		self.CAR5_Z = 0 #X машины на 5 линии
		self.IS_CAR5 = 0
		self.SN_CAR5 = 0
		self.MA_CAR5 = ""
		self.MA_CAR5_SZ = [0, 0]

		self.CAR6_X = 77.3 * self.MASHTAB + self.ADDX #X машины на 6 линии
		self.CAR6_Z = 0 #X машины на 6 линии
		self.IS_CAR6 = 0
		self.SN_CAR6 = 0
		self.MA_CAR6 = ""
		self.MA_CAR6_SZ = [0, 0]

		self.CAR7_X = 91.3 * self.MASHTAB + self.ADDX #X машины на 7 линии
		self.CAR7_Z = 0 #X машины на 7 линии
		self.IS_CAR7 = 0
		self.SN_CAR7 = 0
		self.MA_CAR7 = ""
		self.MA_CAR7_SZ = [0, 0]

		self.CAR8_X = 105.3 * self.MASHTAB + self.ADDX #X машины на 8 линии
		self.CAR8_Z = 0 #X машины на 8 линии
		self.IS_CAR8 = 0
		self.SN_CAR8 = 0
		self.MA_CAR8 = ""
		self.MA_CAR8_SZ = [0, 0]

		self.CAR9_X = 119 * self.MASHTAB + self.ADDX #X машины на 9 линии
		self.CAR9_Z = 0 #X машины на 9 линии
		self.IS_CAR9 = 0
		self.SN_CAR9 = 0
		self.MA_CAR9 = ""
		self.MA_CAR9_SZ = [0, 0]

		self.BG1_X = 0 + self.ADDX #Координата бг 1 по оси X
		self.BG1_Z = self.screensize[0] - self.screensize[0] * 2 + 35 * self.MASHTAB + self.ADDY #Координата бг 1 по оси Z

		self.BG2_X = 0 + self.ADDX#Координата бг 2 по оси X
		self.BG2_Z = 0 + self.ADDY#Координата бг 2 по оси Z

		self.fade = pygame.Surface(self.screensize)
		self.fadestate = 0
		self.needfade = 0

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
		self.FREEZE_PNG = pygame.transform.scale(self.FREEZE_PNG, (int(self.FREEZE_PNG.get_width()) * self.MASHTAB, int(self.FREEZE_PNG.get_height()) * self.MASHTAB))
		self.FREEZE_PNG_SIZE = [self.FREEZE_PNG.get_width(), self.FREEZE_PNG.get_height()]


		#В обьяснении не нуждается
		self.GAME_OVER_SCREEN = pygame.transform.scale(self.GAME_OVER_SCREEN, (int(self.GAME_OVER_SCREEN.get_width()) * self.MASHTAB, int(self.GAME_OVER_SCREEN.get_height()) * self.MASHTAB))
		self.GAME_OVER_SCREEN_SIZE = [self.GAME_OVER_SCREEN.get_width(), self.GAME_OVER_SCREEN.get_height()]

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

	def TextDraw(self, lablefromlables, add):
		surface = self.screen
		font = pygame.font.Font(f"{self.PATH}{FONT}", lablefromlables[2] * self.MASHTAB) #Создание фонт обьекта
		text = font.render(f"{lablefromlables[0]}{add}", True, lablefromlables[1]) #создание текст обьекта для отрисовки
		surface.blit(text, (lablefromlables[3] * self.MASHTAB + self.ADDX, lablefromlables[4] * self.MASHTAB + self.ADDY)) #отрисовка на указанном surface

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
		#print(self.PLAYER_UNLOCK_CONTROLS)
		if self.ALLOW_MOVE_BACKGROUNG:
			self.BG1_Z += self.PLAYER_SPEED
			self.BG2_Z += self.PLAYER_SPEED
			self.PLAYER_SCORE += 1

			if (self.BG1_Z + self.screensize[0] >= self.screensize[0]):
				self.BG1_Z = self.screensize[0] - self.screensize[0] * 2 + 35 * self.MASHTAB
				self.BG2_Z = 0

		#End
		self.screen.blit(self.BACKGROUND_PNG, (self.BG1_X, self.BG1_Z + self.ADDY))
		self.screen.blit(self.BACKGROUND_PNG, (self.BG2_X, self.BG2_Z + self.ADDY))

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
				generatedpos = randint(self.F_GN, self.S_GN) + self.ADDY
				self.CAR1_Z = generatedpos - generatedpos * 2 
			if self.IS_CAR1:
				self.CAR1_Z += self.PLAYER_SPEED
				if self.CAR1_Z >= self.screensize[0] + self.ADDY:
					self.IS_CAR1 = 0
			#Машина 2
			if self.IS_CAR2 != 1:
				self.IS_CAR2 = 1
				result = randint(0, self.MACHINES)
				self.MA_CAR2 = self.MACHINES_TO_RAND[result]
				self.MA_CAR2_SZ = self.SZ_MACHINES_TO_RAND[result]
				self.SN_CAR2 = result
				generatedpos = randint(self.F_GN, self.S_GN)
				self.CAR2_Z = generatedpos - generatedpos * 2 + self.ADDY
			if self.IS_CAR2:
				self.CAR2_Z += self.PLAYER_SPEED
				if self.CAR2_Z >= self.screensize[0] + self.ADDY:
					self.IS_CAR2 = 0
			#Машина 3
			if self.IS_CAR3 != 1:
				self.IS_CAR3 = 1
				result = randint(0, self.MACHINES)
				self.MA_CAR3 = self.MACHINES_TO_RAND[result]
				self.MA_CAR3_SZ = self.SZ_MACHINES_TO_RAND[result]
				self.SN_CAR3 = result
				generatedpos = randint(self.F_GN, self.S_GN)
				self.CAR3_Z = generatedpos - generatedpos * 2 + self.ADDY
			if self.IS_CAR3:
				self.CAR3_Z += self.PLAYER_SPEED
				if self.CAR3_Z >= self.screensize[0] + self.ADDY:
					self.IS_CAR3 = 0
			#Машина 4
			if self.IS_CAR4 != 1:
				self.IS_CAR4 = 1
				result = randint(0, self.MACHINES)
				self.MA_CAR4 = self.MACHINES_TO_RAND[result]
				self.MA_CAR4_SZ = self.SZ_MACHINES_TO_RAND[result]
				self.SN_CAR4 = result
				generatedpos = randint(self.F_GN, self.S_GN)
				self.CAR4_Z = generatedpos - generatedpos * 2 + self.ADDY
			if self.IS_CAR4:
				self.CAR4_Z += self.PLAYER_SPEED
				if self.CAR4_Z >= self.screensize[0] + self.ADDY:
					self.IS_CAR4 = 0
			#Машина 5
			if self.IS_CAR5 != 1:
				self.IS_CAR5 = 1
				result = randint(0, self.MACHINES)
				self.MA_CAR5 = self.MACHINES_TO_RAND[result]
				self.MA_CAR5_SZ = self.SZ_MACHINES_TO_RAND[result]
				self.SN_CAR5 = result
				generatedpos = randint(self.F_GN, self.S_GN)
				self.CAR5_Z = generatedpos - generatedpos * 2 + self.ADDY
			if self.IS_CAR5:
				self.CAR5_Z += self.PLAYER_SPEED
				if self.CAR5_Z >= self.screensize[0] + self.ADDY:
					self.IS_CAR5 = 0
			#Машина 6
			if self.IS_CAR6 != 1:
				self.IS_CAR6 = 1
				result = randint(0, self.MACHINES)
				self.MA_CAR6 = self.MACHINES_TO_RAND[result]
				self.MA_CAR6_SZ = self.SZ_MACHINES_TO_RAND[result]
				self.SN_CAR6 = result
				generatedpos = randint(self.F_GN, self.S_GN)
				self.CAR6_Z = generatedpos - generatedpos * 2 + self.ADDY
			if self.IS_CAR6:
				self.CAR6_Z += self.PLAYER_SPEED
				if self.CAR6_Z >= self.screensize[0] + self.ADDY:
					self.IS_CAR6 = 0
			#Машина 7
			if self.IS_CAR7 != 1:
				self.IS_CAR7 = 1
				result = randint(0, self.MACHINES)
				self.MA_CAR7 = self.MACHINES_TO_RAND[result]
				self.MA_CAR7_SZ = self.SZ_MACHINES_TO_RAND[result]
				self.SN_CAR7 = result
				generatedpos = randint(self.F_GN, self.S_GN)
				self.CAR7_Z = generatedpos - generatedpos * 2 + self.ADDY
			if self.IS_CAR7:
				self.CAR7_Z += self.PLAYER_SPEED
				if self.CAR7_Z >= self.screensize[0] + self.ADDY:
					self.IS_CAR7 = 0
			#Машина 8
			if self.IS_CAR8 != 1:
				self.IS_CAR8 = 1
				result = randint(0, self.MACHINES)
				self.MA_CAR8 = self.MACHINES_TO_RAND[result]
				self.MA_CAR8_SZ = self.SZ_MACHINES_TO_RAND[result]
				self.SN_CAR8 = result
				generatedpos = randint(self.F_GN, self.S_GN)
				self.CAR8_Z = generatedpos - generatedpos * 2 + self.ADDY
			if self.IS_CAR8:
				self.CAR8_Z += self.PLAYER_SPEED
				if self.CAR8_Z >= self.screensize[0] + self.ADDY:
					self.IS_CAR8 = 0
			#Машина 9
			if self.IS_CAR9 != 1:
				self.IS_CAR9 = 1
				result = randint(0, self.MACHINES)
				self.MA_CAR9 = self.MACHINES_TO_RAND[result]
				self.MA_CAR9_SZ = self.SZ_MACHINES_TO_RAND[result]
				self.SN_CAR9 = result
				generatedpos = randint(self.F_GN, self.S_GN)
				self.CAR9_Z = generatedpos - generatedpos * 2 + self.ADDY
			if self.IS_CAR9:
				self.CAR9_Z += self.PLAYER_SPEED
				if self.CAR9_Z >= self.screensize[0] + self.ADDY:
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

	def FadeScreen(self, color, how, val):
		self.fade.fill(color)
		if how == "in":
			if self.fadestate == 300:
				print("No")
				self.fadestate = 0
				self.fade.set_alpha(self.fadestate)
			else:
				self.fadestate += val
				self.fade.set_alpha(self.fadestate)
				self.screen.blit(self.fade, (0 + self.ADDX, 0 + self.ADDY))
		if how == "out":
			if self.fadestate == 0:
				print("No")
				self.fadestate = 300
				self.fade.set_alpha(self.fadestate)
			else:
				self.fadestate -= val
				self.fade.set_alpha(self.fadestate)
				self.screen.blit(self.fade, (0 + self.ADDX, 0 + self.ADDY))

	def PlusToMashtab(self):
		if self.temp >= 3 and self.temp <= 9:
			self.temp += 1
			if self.temp <= 2:
				self.temp = 3
			if self.temp >= 10:
				self.temp = 9
			mashtab_fromfile = open(f"{self.PATH}options/mashtab.txt", "w")
			mashtab_fromfile.write(str(self.temp))
			mashtab_fromfile.close()

	def MinusToMashtab(self):
		if self.temp >= 3 and self.temp <= 9:
			self.temp -= 1
			if self.temp <= 2:
				self.temp = 3
			if self.temp >= 10:
				self.temp = 9
			mashtab_fromfile = open(f"{self.PATH}options/mashtab.txt", "w")
			mashtab_fromfile.write(str(self.temp))
			mashtab_fromfile.close()

	def ChangeFullscreen(self):
		if self.temp1:
			self.temp1 = 0
		else:
			self.temp1 = 1
		temp_file = open(f"{self.PATH}options/fullscreen.txt", "w")
		temp_file.write(str(self.temp1))
		temp_file.close()

	def Exit(self):
		pygame.quit()
		sys.exit()

	def console(self):
		if self.CONSOLE_ENABLED:
			#self.screen.fill((255, 255, 255))
			#self.TextDraw("Console opened. Check you executable window", 12, (255, 255, 255), (0, 0), self.screen)
			pygame.display.flip()
			print("Welcome to game console! To exit from console write exit")
			while True:
				consoleinput = str(input(">"))
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

	def StartOnePlayer(self):
		self.running = 0
		self.GAME_TYPE = "1P"
		self.MainScene()

	def StartTwoPlayer(self):
		self.running = 0
		self.GAME_TYPE = "2P"
		self.MainScene()

	def OnePlLeft(self):
		if self.PLAYER_UNLOCK_CONTROLS:
			if self.PLAYER_CAR_X > 0 + self.ADDX:
				self.PlayerMoveTo("LEFT")

	def OnePlRight(self):
		if self.PLAYER_UNLOCK_CONTROLS:
			if self.PLAYER_CAR_X < self.screensize[0] - self.SPORT_VAZ_PNG_SIZE[0] - 1 + self.ADDX:
				self.PlayerMoveTo("RIGHT")

	def TwoPlLeft(self):
		if self.PLAYER_UNLOCK_CONTROLS:
			if self.PLAYER2_CAR_X > 0 + self.ADDX:
				self.PlayerMoveTo("P2LEFT")

	def TwoPlRight(self):
		if self.PLAYER_UNLOCK_CONTROLS:
			if self.PLAYER2_CAR_X < self.screensize[0] - self.SPORT_VAZ_PNG_SIZE[0] - 1 + self.ADDX:
				self.PlayerMoveTo("P2RIGHT")

	def UpdateButtStates(self, press, pos):
		self.BUTTON_EVENT_POS = pos
		self.BUTTON_PRESS = press

	def EditSensorMode(self):
		if self.senstemp:
			self.senstemp = 0
			self.SENSORMODE = 0
			temp = open(f"{self.PATH}options/onscreenplay.txt", "w")
			temp.write(str(self.senstemp))
			temp.close()
		else:
			self.senstemp = 1
			self.SENSORMODE = 1
			temp = open(f"{self.PATH}options/onscreenplay.txt", "w")
			temp.write(str(self.senstemp))
			temp.close()

	def EditSoundMode(self):
		if self.SOUND_OFF:
			self.SOUND_OFF = 0
			temp = open(f"{self.PATH}options/defaultsoundmode.txt", "w")
			temp.write(str(self.SOUND_OFF))
			temp.close()
		else:
			self.SOUND_OFF = 1
			temp = open(f"{self.PATH}options/defaultsoundmode.txt", "w")
			temp.write(str(self.SOUND_OFF))
			temp.close()

	def ExitFromPause(self):
		self.running = 0
		if self.SOUND_OFF != 1:
			self.CAR_POLICE.play(loops=-1)
			self.CAR_MOVE.play(loops=-1)
			self.GAME_PAUSE.stop()
		self.ALLOW_MOVE_BACKGROUNG = 1
		self.CAN_GENERATEMACHINES = 1

	def GoToPause(self):
		self.Pause()
		self.running = 1

	def GoToMainMenu(self):
		self.running = 0
		self.needtoexitmainmenu = 1
		if self.SOUND_OFF != 1:
			self.CAR_POLICE.play(loops=-1)
			self.CAR_MOVE.play(loops=-1)
			self.GAME_PAUSE.stop()
		self.ALLOW_MOVE_BACKGROUNG = 1
		self.CAN_GENERATEMACHINES = 1

	def MainMenu(self):
		self.Values()
		self.running = 1
		self.needfade = 1
		self.fadestate = 300
		self.CAR_MOVE.stop()
		self.CAR_POLICE.stop()
		self.CAR_CRASH.stop()
		dark = pygame.Surface(self.screensize)
		dark.fill((0, 0, 0))
		OnePlayerButton = Button((self.ADDX, self.ADDY), self.screen, BUTTON_MAINMENU_ONEPL, self.MASHTAB, self.StartOnePlayer)
		TwoPlayerButton = Button((self.ADDX, self.ADDY), self.screen, BUTTON_MAINMENU_TWOPL, self.MASHTAB, self.StartTwoPlayer)
		NoTwoPlayerButton = Button((self.ADDX, self.ADDY), self.screen, BUTTON_MAINMENU_NOTWOPL, self.MASHTAB, print)
		OptionsButton = Button((self.ADDX, self.ADDY), self.screen, BUTTON_MAINMENU_OPTIONS, self.MASHTAB, self.Options)
		while True:
			self.screen.fill((0, 0, 0))
			self.AnimatedBackground()
			self.TextDraw(LABLE_TITLE, "")
			self.TextDraw(LABLE_TELEGRAM, "")

			OnePlayerButton.tick()
			if self.SENSORMODE:
				NoTwoPlayerButton.tick()
			else:
				TwoPlayerButton.tick()
			OptionsButton.tick()

			self.screen.blit(dark, (0 + self.ADDX, self.screensize[1] + self.ADDY))
			self.screen.blit(dark, (0 + self.ADDX, self.screensize[1] - self.screensize[1] * 2 + self.ADDY))
			self.screen.blit(dark, (0 + self.ADDX + self.screensize[0], self.ADDY))
			self.screen.blit(dark, (self.screensize[0] - self.screensize[0] * 2 + self.ADDX, self.ADDY))

			if self.needfade:
				if self.fadestate == 0:
					self.needfade = 0
				self.FadeScreen((0, 0, 0), "out", 35)
			
			KEYS=pygame.key.get_pressed()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			pygame.display.flip()
			self.clock.tick(self.FPS)

	def Options(self):
		self.Values()
		self.running = 1
		dark = pygame.Surface(self.screensize)
		dark.fill((0, 0, 0))
		dark2 = pygame.Surface((self.screensize[0], self.screensize[1]))
		dark2.set_alpha(100)
		MashtabPlusButt = Button((self.ADDX, self.ADDY), self.screen, BUTTON_OPTMENUPLUS, self.MASHTAB, self.PlusToMashtab)
		MashtabMinButt = Button((self.ADDX, self.ADDY), self.screen, BUTTON_OPTMENUMIN, self.MASHTAB, self.MinusToMashtab)
		ChangeFullButt = Button((self.ADDX, self.ADDY), self.screen, BUTTON_OPTMENUCHFULL, self.MASHTAB, self.ChangeFullscreen)
		ChangeSoundMode = Button((self.ADDX, self.ADDY), self.screen, BUTTON_OPTMENUCHSOUN, self.MASHTAB, self.EditSoundMode)
		ChangeSENMButt = Button((self.ADDX, self.ADDY), self.screen, BUTTON_OPTMENUCHONSP, self.MASHTAB, self.EditSensorMode)
		ExitButt = Button((self.ADDX, self.ADDY), self.screen, BUTTON_OPTMENUEXIT, self.MASHTAB, self.GoToMainMenu)
		while self.running:
			self.screen.fill((0, 0, 0))
			self.AnimatedBackground()
			self.screen.blit(dark2, (self.ADDX, self.ADDY))
			count = 0
			for char in LABLE_OPTMENULB2[0]:
				count += 1
			self.TextDraw(LABLE_OPTMENULB1, "")
			self.TextDraw(LABLE_OPTMENULB2, self.temp)
			self.TextDraw(LABLE_OPTMENULB3, "")
			self.TextDraw(LABLE_OPTMENULB5, self.senstemp)
			self.TextDraw(LABLE_OPTMENULB6, self.SOUND_OFF)
			self.TextDraw(LABLE_OPTMENUPATH, self.PATH)
			if int(self.temp1):
				self.TextDraw(LABLE_OPTMENULB4, "Да.")
			else:
				self.TextDraw(LABLE_OPTMENULB4, "Нет.")
			tempone = LABLE_OPTMENULB2[3]
			MashtabPlusButt.tick()
			MashtabMinButt.tick()
			ChangeFullButt.tick()
			ChangeSoundMode.tick()
			ExitButt.tick()
			ChangeSENMButt.tick()
			self.screen.blit(dark, (0 + self.ADDX, self.screensize[1] + self.ADDY))
			self.screen.blit(dark, (0 + self.ADDX, self.screensize[1] - self.screensize[1] * 2 + self.ADDY))
			self.screen.blit(dark, (0 + self.ADDX + self.screensize[0], self.ADDY))
			self.screen.blit(dark, (self.screensize[0] - self.screensize[0] * 2 + self.ADDX, self.ADDY))
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			pygame.display.flip()
			self.clock.tick(self.FPS)
		self.MainMenu()

	def MainScene(self):
		self.Values()
		self.running = 1
		dark = pygame.Surface((self.screensize[0], self.screensize[1]))
		dark.fill((0, 0, 0))
		ONEPLMODE_LEFT = Button((self.ADDX, self.ADDY), self.screen, BUTTON_PLAYING_ONEPLMODE_LEFT, self.MASHTAB, self.OnePlLeft)
		ONEPLMODE_RIGHT = Button((self.ADDX, self.ADDY), self.screen, BUTTON_PLAYING_ONEPLMODE_RIGHT, self.MASHTAB, self.OnePlRight)
		TWOPLMODE_P1LEFT = Button((self.ADDX, self.ADDY), self.screen, BUTTON_PLAYING_TWOPLMODE_P1LEFT, self.MASHTAB, self.OnePlLeft)
		TWOPLMODE_P1RIGHT = Button((self.ADDX, self.ADDY), self.screen, BUTTON_PLAYING_TWOPLMODE_P1RIGHT, self.MASHTAB, self.OnePlRight)
		TWOPLMODE_P2LEFT = Button((self.ADDX, self.ADDY), self.screen, BUTTON_PLAYING_TWOPLMODE_P2LEFT, self.MASHTAB, self.TwoPlLeft)
		TWOPLMODE_P2RIGHT = Button((self.ADDX, self.ADDY), self.screen, BUTTON_PLAYING_TWOPLMODE_P2RIGHT, self.MASHTAB, self.TwoPlRight)

		PauseButt = Button((self.ADDX, self.ADDY), self.screen, BUTTON_PLAYING_PAUSE, self.MASHTAB, self.GoToPause)
		if self.SOUND_OFF != 1:
			self.CAR_POLICE.play(loops=-1)
			self.CAR_MOVE.play(loops=-1)
		while self.running:
			KEYS=pygame.key.get_pressed()
			if KEYS[pygame.K_ESCAPE]:
				self.Pause()

			self.screen.fill((0, 0, 0))
			self.AnimatedBackground()
			self.MachinePosGenerate()
			if self.PLAYER_COLLISION:
				self.ColliderOfMachines()

			self.screen.blit(self.PLAYER_CAR_SRFC, (self.PLAYER_CAR_X, self.PLAYER_CAR_Y))
			if self.GAME_TYPE == "2P":
				self.screen.blit(self.PLAYER2_CAR_SRFC, (self.PLAYER2_CAR_X, self.PLAYER2_CAR_Z))

			if self.SOUND_OFF:
				self.TextDraw(LABLE_SOUNDOFF, "")
			self.TextDraw(LABLE_YOUSCOREINGAME1, self.PLAYER_SCORE)

			if self.PLAYER_UNLOCK_CONTROLS:
				if KEYS[self.KEY_LEFT]:
					self.OnePlLeft()
				if KEYS[self.KEY_RIGHT]:
					self.OnePlRight()
				if self.GAME_TYPE == "2P":
					if KEYS[self.P2_KEY_LEFT]:
						self.TwoPlLeft()
					if KEYS[self.P2_KEY_RIGHT]:
						self.TwoPlRight()

				if KEYS[pygame.K_BACKQUOTE]:
					self.console()

			if self.SENSORMODE:
				if self.GAME_TYPE == "1P":
					ONEPLMODE_LEFT.tick()
					ONEPLMODE_RIGHT.tick()
				if self.GAME_TYPE == "2P":
					TWOPLMODE_P1LEFT.tick()
					TWOPLMODE_P1RIGHT.tick()
					TWOPLMODE_P2LEFT.tick()
					TWOPLMODE_P2RIGHT.tick()
			PauseButt.tick()

			self.screen.blit(dark, (0 + self.ADDX, self.screensize[1] + self.ADDY))
			self.screen.blit(dark, (0 + self.ADDX, self.screensize[1] - self.screensize[1] * 2 + self.ADDY))
			self.screen.blit(dark, (0 + self.ADDX + self.screensize[0], self.ADDY))
			self.screen.blit(dark, (self.screensize[0] - self.screensize[0] * 2 + self.ADDX, self.ADDY))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			if self.needtoexitmainmenu:
				self.running = 0

			pygame.display.flip()
			self.clock.tick(self.FPS)
		self.MainMenu()

	def Pause(self):
		self.running = 1
		dark = pygame.Surface((self.screensize[0], self.screensize[1]))
		dark.fill((0, 0, 0))
		dark2 = pygame.Surface((self.screensize[0], self.screensize[1]))
		dark2.set_alpha(100)
		self.ALLOW_MOVE_BACKGROUNG = 0
		self.CAN_GENERATEMACHINES = 0
		ReturnButton = Button((self.ADDX, self.ADDY), self.screen, BUTTON_PAUSE_RETURN, self.MASHTAB, self.ExitFromPause)
		ExitFromGame = Button((self.ADDX, self.ADDY), self.screen, BUTTON_PAUSE_EXITFROMGAME, self.MASHTAB, self.Exit)
		ExitToMenu = Button((self.ADDX, self.ADDY), self.screen, BUTTON_MAINMENU_MENU, self.MASHTAB, self.GoToMainMenu)
		if self.SOUND_OFF != 1:
			self.CAR_POLICE.stop()
			self.CAR_MOVE.stop()
			self.GAME_PAUSE.play()
		
		while self.running:
			self.AnimatedBackground()
			self.MachinePosGenerate()
			self.screen.blit(self.PLAYER_CAR_SRFC, (self.PLAYER_CAR_X, self.PLAYER_CAR_Y))
			if self.GAME_TYPE == "2P":
				self.screen.blit(self.PLAYER2_CAR_SRFC, (self.PLAYER2_CAR_X, self.PLAYER2_CAR_Z))
			self.screen.blit(dark2, (self.ADDX, self.ADDY))
			self.TextDraw(LABLE_PAUSE, "")
			ReturnButton.tick()
			ExitFromGame.tick()
			ExitToMenu.tick()

			self.screen.blit(dark, (0 + self.ADDX, self.screensize[1] + self.ADDY))
			self.screen.blit(dark, (0 + self.ADDX, self.screensize[1] - self.screensize[1] * 2 + self.ADDY))
			self.screen.blit(dark, (0 + self.ADDX + self.screensize[0], self.ADDY))
			self.screen.blit(dark, (self.screensize[0] - self.screensize[0] * 2 + self.ADDX, self.ADDY))

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			pygame.display.flip()
			self.clock.tick(self.FPS)

	def NewGame(self):
		self.running = 0
		self.ALLOW_MOVE_BACKGROUNG = 1
		self.CAN_GENERATEMACHINES = 1
		self.CAR_CRASH.stop()
		self.MainScene()

	def GameOverScreen(self):
		self.running = 1
		dark = pygame.Surface((self.screensize[0], self.screensize[1]))
		dark.fill((0, 0, 0))
		self.ALLOW_MOVE_BACKGROUNG = 0
		self.CAN_GENERATEMACHINES = 0
		self.needfade = 1
		self.fadestate = 300
		NewGameButton = Button((self.ADDX, self.ADDY), self.screen, BUTTON_GAMEOVER_NEWGAME, self.MASHTAB, self.NewGame)
		ExitButton = Button((self.ADDX, self.ADDY), self.screen, BUTTON_GAMEOVER_EXIT, self.MASHTAB, self.GoToMainMenu)
		if self.SOUND_OFF != 1:
			self.CAR_MOVE.stop()
			self.CAR_POLICE.stop()
			self.CAR_CRASH.play()
		if self.PLAYER_SCORE > self.MAX_SCORE:
			self.MAX_SCORE = self.PLAYER_SCORE
		while self.running:
			self.screen.fill((0, 0, 0))
			self.AnimatedBackground()
			self.MachinePosGenerate()
			self.screen.blit(self.PLAYER_CAR_SRFC, (self.PLAYER_CAR_X, self.PLAYER_CAR_Y))
			if self.GAME_TYPE == "2P":
				self.screen.blit(self.PLAYER2_CAR_SRFC, (self.PLAYER2_CAR_X, self.PLAYER2_CAR_Z))
			self.screen.blit(self.GAME_OVER_SCREEN, (0 + self.ADDX, 26 * self.MASHTAB + self.ADDY))
			self.TextDraw(LABLE_GAMEOVER, "")
			self.TextDraw(LABLE_YOUSCOREINGAME, self.PLAYER_SCORE)
			self.TextDraw(LABLE_RECORD, self.MAX_SCORE)
			NewGameButton.tick()
			ExitButton.tick()

			self.screen.blit(dark, (0 + self.ADDX, self.screensize[1] + self.ADDY))
			self.screen.blit(dark, (0 + self.ADDX, self.screensize[1] - self.screensize[1] * 2 + self.ADDY))
			self.screen.blit(dark, (0 + self.ADDX + self.screensize[0], self.ADDY))
			self.screen.blit(dark, (self.screensize[0] - self.screensize[0] * 2 + self.ADDX, self.ADDY))

			if self.needfade:
				if self.fadestate == 0:
					self.needfade = 0
				self.FadeScreen((255, 255, 255), "out",  9)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			pygame.display.flip()
			self.clock.tick(self.FPS)

if __name__ == "__main__":
	game = Game()
