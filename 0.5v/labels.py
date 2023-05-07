#Важно! Текстуры игры не умножены в 5(по умолчанию.) РАЗ! Они умножаются для pygame на этапе инициализации. Прошу учесть этот факт! Размеры окна без умножения: 135x100
#Ещё. TX, TY это координаты текста кнопки, они рисуются на самом surface кнопки. BX, BX это координаты кнопки на экране.

FONT = "assets/GAME_FONT.ttf"

BUTTON_COLORS = [(255, 255, 255), (205, 205, 205), (105, 105, 105)]
SCREEN_SIZE = [135, 100]

#LABEL_ИМЯ = ["TYPE", "ТЕКСТ", (R, G, B), РАЗМЕР, X, Y]

LABEL_HELLOWORLD = ["Hello World!", (255, 255, 255), 3, 0, 0]
LABEL_FPS = ["FPS:", (255, 255, 255), 3, 0, 4]

LABLE_TITLE = ["Лютый Гонщик", (255, 30, 0), 8, 20, 23]
LABLE_MAINMENULB1 = ["1 - 1 Игрок         2 - 2 Игрока", (255, 255, 30), 3, 19, 58]
LABLE_TELEGRAM = ["By AltTeam. TG:t.me/lytigonchic", (255, 255, 255), 2, 0, SCREEN_SIZE[1] - 2]
LABLE_SOUNDOFF = ["Звук Выключен", (255, 0, 0), 3, 0, SCREEN_SIZE[1] - 3*2]
LABLE_YOUSCOREINGAME1 = ["Очки:", (0, 180, 0), 3, 0, SCREEN_SIZE[1] - 3]
LABLE_PAUSE = ["Пауза", (255, 255, 255), 3, 60, 8.4]
LABLE_HOWTOEXITFROMPAUSE = ["Выйти из паузы - ENTER", (255, 255, 255), 3, 34.6, 90]
LABLE_GAMEOVER = ["Game Over!", (0, 0, 0), 3*4, 10.5, 30]
LABLE_YOUSCOREINGAME = ["Ваши очки:", (0, 0, 0), 3, 48, 47]
LABLE_RECORD = ["Рекорд:", (0, 0, 0), 3, 48, 43.5]
LABLE_HOWTOSTARTNEWGAME = ['Нажмите "Enter" для начала новой игры.', (0, 0, 0), 3, 11.5, 64]
LABLE_SHOW_FPS = ["FPS:", (0, 0, 0), 0.5, 0, 0]
LABLE_MAINMENULB2 = ["3 - Настройки", (255, 255, 30), 3, 46, 65]
LABLE_OPTMENULB1 = ["Настройки", (255, 255, 255), 5, 46, 10]
LABLE_OPTMENULB2 = ["Маштаб:", (255, 255, 255), 3, 10, 30]
LABLE_OPTMENULB5 = ["Сенсор. Упр:", (255, 255, 255), 3, 10, 37.9]
LABLE_OPTMENULB3 = ["*Нужно выйти из игры для применения некоторых настроек.", (200, 200, 200), 2, 13, 80]
LABLE_OPTMENULB4 = ["Режим фуллскрина:", (255, 255, 255), 3, 10, 34]
LABLE_OPTMENULB6 = ["Звук:", (255, 255, 255), 3, 10, 41.9]
LABLE_OPTMENUPATH = ["Game path:", (255, 255, 255), 1, 0, 0]

#BUTTON_ИМЯ = ["ТЕКСТ" TYPE, BUTTSZX, BUTTSZY, BX, BY]
# TYPE - ONECL, MULTI

BUTTON_OPTMENUPLUS = ["+", "ONECL", 5, 5, 35, 28.9]
BUTTON_OPTMENUMIN = ["-", "ONECL", 5, 5, 41, 28.9]
BUTTON_OPTMENUCHFULL = ["Сменить", "ONECL", 24, 5, 73, 32.9]
BUTTON_OPTMENUCHONSP = ["Сменить", "ONECL", 24, 5, 50, 36.5]
BUTTON_OPTMENUCHSOUN = ["Сменить", "ONECL", 24, 5, 29, 40.3]
BUTTON_OPTMENUEXIT = ["Выйти в меню", "ONECL", 40, 5, SCREEN_SIZE[0]/2-40/2, 86]

BUTTON_GAMEOVER_NEWGAME = ["Заного", "ONECL", 24, 5, 20, 64]
BUTTON_GAMEOVER_EXIT = ["Выйти", "ONECL", 24, 5, SCREEN_SIZE[1]-9, 64]

BUTTON_MAINMENU_ONEPL = ["1 Игрок", "ONECL", 25, 5, 55, 56]
BUTTON_MAINMENU_TWOPL = ["2 Игрока", "ONECL", 25, 5, 55, 62]
BUTTON_MAINMENU_NOTWOPL = ["--------", "ONECL", 25, 5, 55, 62]
BUTTON_MAINMENU_OPTIONS = ["Настро.", "ONECL", 25, 5, 55, 68]

BUTTON_PLAYING_MUTE = ["MUTE", "ONECL", 16, 5, 1, 6.3]
BUTTON_PLAYING_PAUSE = ["PAUSE", "ONECL", 16, 5, 1, 1]

BUTTON_PAUSE_RETURN = ["Назад в игру", "ONECL", 38, 5, SCREEN_SIZE[0]/2-38/2, 80]
BUTTON_MAINMENU_MENU = ["Меню", "ONECL", 38, 5, SCREEN_SIZE[0]/2-38/2, 86]
BUTTON_PAUSE_EXITFROMGAME = ["Выйти из игры", "ONECL", 40, 5, SCREEN_SIZE[0]/2-40/2, 92]

BUTTON_PLAYING_ONEPLMODE_LEFT = ["<", "MULTI", 10, 10, 10, 80]
BUTTON_PLAYING_ONEPLMODE_RIGHT = [">", "MULTI", 10, 10, 115, 80]

BUTTON_PLAYING_TWOPLMODE_P1LEFT = ["<", "MULTI", 10, 10, 10, 80]
BUTTON_PLAYING_TWOPLMODE_P1RIGHT = [">", "MULTI", 10, 10, 25, 80]
BUTTON_PLAYING_TWOPLMODE_P2LEFT = ["<", "MULTI", 10, 10, 100, 80]
BUTTON_PLAYING_TWOPLMODE_P2RIGHT = [">", "MULTI", 10, 10, 115, 80]