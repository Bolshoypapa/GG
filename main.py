#!/usr/bin/env python


from pygame.locals import *
from sys import exit
from time import sleep
from comp import *
from plitka import *
from os import path
from peremennye import *
from Generate import *
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic
import sys
import pygame

class App(QWidget):
    def __init__(self):
        super(App, self).__init__()
        self.ui = uic.loadUi("mydesign.ui")
        self.uii = uic.loadUi("rules.ui")
        self.start()
        self.btn_start()
        self.btn_exit()
        self.rules()
        self.back()

    def start(self):
        self.ui.show()

    def info(self):
        self.uii.show()

    def info(self):
        self.uii.show()

    def ppp(self):
        print('ldd')

    def rules(self):
        self.ui.btn_rules.clicked.connect(lambda: self.info())
        self.ui.btn_rules.clicked.connect(lambda: self.ui.close())

    def btn_exit(self):
        self.ui.btn_exit.clicked.connect(lambda: self.ui.close())

    def back(self):
        self.uii.btn_back.clicked.connect(lambda: self.start())
        self.uii.btn_back.clicked.connect(lambda: self.uii.close())

    def btn_start(self):
        #self.ui.btn_start.clicked.connect(lambda: self.ui.close())
        self.ui.btn_start.clicked.connect(lambda: main())


def seticon(iconname):

         #указывает имя значка и растровое изображение размером 32x32 пикселя
         #значок окна будет установлен в изображение, но черные пиксели будут заполнены

    icon=pygame.Surface((32,32))
    icon.set_colorkey((0,0,0))
    rawicon=pygame.image.load(iconname)
    for i in range(0,32):
        for j in range(0,32):
            icon.set_at((i,j), rawicon.get_at((i,j)))
    pygame.display.set_icon(icon)


def draw_bg(screen):

#отрисовка фона доски и всех необходимых кнопок


    #загружает изображения
    pass_button = pygame.image.load("images/pered_propuskom.png")
    replay_button = pygame.image.load("images/zanovo.png")
    exit_button = pygame.image.load("images/vyhod.png")
    computer_tiles_background = pygame.image.load("images/fishki_bota.png")
    human_tiles_background = pygame.image.load("images/moi_fishki.png")
    center_image = pygame.image.load("images/okno.png")

    #рисует центральный прямоугольник
    center_rectangle_start = (0, main_window_resolution[1]/4)
    center_rectangle_size = (main_window_resolution[0], main_window_resolution[1]/2)
    center_rectangle = Rect(center_rectangle_start, center_rectangle_size)
    pygame.draw.rect(screen, INNER_COLOR, center_rectangle)

    #рисует центральное изображение
    center_image_X = (main_window_resolution[0] - 780) / 2
    center_image_Y = (main_window_resolution[1] - 280) / 2
    screen.blit(center_image, (center_image_X, center_image_Y))

    #Рисует верхний и нижний прямоугольники


    #Рисует фон за плитками
    X_start = (main_window_resolution[0]- 565) / 2

    computer_tiles_background_Y = (main_window_resolution[1] / 8) - 60
    human_tiles_background_Y = main_window_resolution[1] - (main_window_resolution[1]/8) - 60

    screen.blit(computer_tiles_background, (X_start, computer_tiles_background_Y))
    screen.blit(human_tiles_background, (X_start, human_tiles_background_Y))

    #Рисует кнопки
    REPLAY_BUTTON_PLACE[0] = ((main_window_resolution[0] - 565) / 2 - 81) /2
    EXIT_BUTTON_PLACE[0] = ((main_window_resolution[0] - 565) / 2 - 81) /2

    REPLAY_BUTTON_PLACE[1] = human_tiles_background_Y + 25
    EXIT_BUTTON_PLACE[1] = REPLAY_BUTTON_PLACE[1] + 40

    PASS_BUTTON_PLACE[0] = ((main_window_resolution[0]- 565)/2 + 565) + ((main_window_resolution[0]- 565)/2 - 99)/2
    PASS_BUTTON_PLACE[1] = human_tiles_background_Y + 37

    screen.blit(replay_button, (REPLAY_BUTTON_PLACE[0], REPLAY_BUTTON_PLACE[1]))
    screen.blit(exit_button, (EXIT_BUTTON_PLACE[0], EXIT_BUTTON_PLACE[1]))
    screen.blit(pass_button, (PASS_BUTTON_PLACE[0], PASS_BUTTON_PLACE[1]))

    #обновляет отображение
    pygame.display.update()


def draw_tiles(screen):


        #эта функция рисует плитки как у пользователя так и у бота

    #Выводи пользовательские плитки на экран
    for i in range(len(HUMAN_TILES)):
        current_tile = HUMAN_TILES[i][0]
        current_position = HUMAN_TILES[i][1]
        temp_tile = Tile(current_tile[0], current_tile[1], screen, current_position[0], current_position[1])
        temp_tile.show_vertical()




def initialize(screen):


       #Эта функция берет изображение и создает наборы тайлов для игрока, а затем отображает их на экране

    #Создаёт два случайных списка плиток
    complete_tiles_set = generate_tiles()
    both_players_tiles = distribute_tiles(complete_tiles_set, NUMBER_OF_PLAYERS)

    #Строит список пользовательских плиток
    identifier = 0

    x_start = (main_window_resolution[0]- 565) // 2 + 25
    x_end = x_start + 514
    y_start = main_window_resolution[1] - (main_window_resolution[1]/8) - 34

    for i in range(x_start, x_end, 80):
        HUMAN_TILES.append([both_players_tiles[0][identifier], (i, y_start)])
        identifier += 1


    #Строит список плиток бота
    identifier = 0
    y_start = (main_window_resolution[1] // 8) -34

    for i in range(x_start, x_end, 80):
        COMPUTER_TILES.append([both_players_tiles[1][identifier], (i, y_start)])
        identifier += 1


    #Рисует фон и плитки домино на экране
    draw_bg(screen)
    draw_tiles(screen)


def clicked_on_tile(mouse_position, tile_position):

        #принимает две позиции как «кортежи» и возвращает True, если
         #мышь находится на плитке, возвращает False в противном случае

    if mouse_position[0] > tile_position[0]\
    and mouse_position[0] < (tile_position[0] + 34)\
    and mouse_position[1] > tile_position[1]\
    and mouse_position[1] < (tile_position[1] + 68) :
        return True
    else :
        return False


def tile_check(tile):

       # эта функция принимает плитку в качестве кортежа и возвращает списокплитки в ее подходящем состоянии (в виде кортежа), а положениегде он должен воспроизводиться (в виде строки).Если плитка может воспроизводиться с обеих сторон, возвращаемый список будетиметь 4 элемента, которые являются обоими состояниями, которые может иметь плитка.


    right = 0
    left = 0
    right_flip = 0
    left_flip = 0

    #Если это первая играемая плитка
    if len(PLAYED_TILES) == 0 :
        return tile, None

    #Проверяет, можно ли выложить плитку справа
    if tile[0] == PLAYED_TILES[-1][0][1] :
        right = 1

    elif tile[1] == PLAYED_TILES[-1][0][1] :
        right = 1
        right_flip = 1

    #Проверяет, можно ли выложить плитку слева
    if tile[1] == PLAYED_TILES[0][0][0] :
        left = 1

    elif tile[0] == PLAYED_TILES[0][0][0] :
        left = 1
        left_flip = 1


    #Если плитка может быть выложена с обеих сторон
    if (right == 1) and (left == 1) :

        #пустой список результатов
        result = []

        #Управление правой стороной
        if right_flip == 1 :
            result.extend([(tile[1], tile[0]), "right"])

        else :
            result.extend([tile, "right"])

        #Управление левой стороной
        if left_flip == 1 :
            result.extend([(tile[1], tile[0]), "left"])

        else :
            result.extend([tile, "left"])

        #Возвращает результат
        return result


    #Если плитка может быть выставлена только с правой стороны
    elif right == 1 :
        if right_flip == 1 :
            return (tile[1], tile[0]), "right"
        else :
            return tile, "right"

    #Если плитка может быть воспроизведена только с левой стороны
    elif left == 1 :
        if left_flip == 1 :
            return (tile[1], tile[0]), "left"
        else :
            return tile, "left"

    #Если плитка не подходит
    else :
        return None


def play(tile, screen, place = None):

        #эта функция принимает плитку в качестве "кортежа", отображает и место слева или справа, затем рисует плитку на экране.


    #определяет ориентацию плитки
    orientation = "horizontal"
    # будет ли плитка окрашена в другом порядке
    reverse_tile = 0

    #Инициализация место расположения плитки
    tile_x = 0
    tile_y = 0

    # Заставляет python распознавать эти переменные как глобальные
    global this_is_first_DOWN_tile
    global this_is_first_LEFT_tile
    global this_is_first_UP_tile
    global this_is_first_RIGHT_tile

    #набор переменных определяет, является ли плитка дублем или нет
    tile_is_DUO = 0

    if tile[0] == tile[1] :
        tile_is_DUO = 1

    #Проверяет, является ли эта плитка первой плиткой, которая будет воспроизведена
    if len(PLAYED_TILES) == 0 :

        #Проверяет, правильно ли уложена плитка, затем помещает ее в нужное место
        if tile_is_DUO:
            tile_x = main_window_resolution[0]//2 - 17
            tile_y = main_window_resolution[1]//2 - 34
            orientation = "vertical"

        else :
            tile_x = main_window_resolution[0]//2 - 34
            tile_y = main_window_resolution[1]//2 - 17

        #добавьте плитку в список "Фишки пользователя"
        PLAYED_TILES.append([tile,(tile_x, tile_y)])

    #если плитка будет воспроизводиться в левом направлении
    elif place == "left" :

        #Создаёт несколько переменных, чтобы облегчить понимание кода
        previous_tile = PLAYED_TILES[0][0]
        previous_position = PLAYED_TILES[0][1]

        previous_tile_is_DUO = 0

        if previous_tile[0] == previous_tile[1] :
            previous_tile_is_DUO = 1

        #Ход только в левом направлении
        if TOTAL_X["left"] < main_window_resolution[0]//2 - 150 :

            if tile_is_DUO :
                TOTAL_X["left"] += 36
                orientation = "vertical"
                tile_x = previous_position[0] - 36
                tile_y = previous_position[1] - 17

            else :
                if previous_tile_is_DUO :
                    TOTAL_X["left"] += 70
                    tile_x = previous_position[0] - 70
                    tile_y = previous_position[1] + 17

                else :
                    TOTAL_X["left"] += 70
                    tile_x = previous_position[0] - 70
                    tile_y = previous_position[1]

        #дошел до левого края окна
        else :

            #Движение плитки вверх
            if TOTAL_Y["up"] < main_window_resolution[1]//4 -110 :

                #это первая плитка, которая будет разыграна
                if this_is_first_UP_tile :
                    this_is_first_UP_tile = 0

                    #предыдущая плитка - дубль
                    if previous_tile_is_DUO :
                        TOTAL_Y["up"] += 104  #34 + 70
                        orientation = "vertical"
                        tile_x = previous_position[0]
                        tile_y = previous_position[1] - 70

                    #предыдущая плитка НЕ дубль
                    else :
                        if tile_is_DUO :
                            orientation = "vertical"
                            tile_x = previous_position[0] - 36
                            tile_y = previous_position[1] - 17


                            #эта плитка была горизонтальной, что приводит к ошибке вычисления
                            this_is_first_UP_tile = 1

                        else :
                            TOTAL_Y["up"] += 87  #17 + 70
                            orientation = "vertical"
                            tile_x = previous_position[0]
                            tile_y = previous_position[1] - 70

                #это НЕ первая плитка, которая будет разыграна
                else :

                    #предыдущая плитка - дубль
                    if previous_tile_is_DUO :
                        TOTAL_Y["up"] += 70
                        orientation = "vertical"
                        tile_x = previous_position[0] + 17
                        tile_y = previous_position[1] - 70

                    #предыдущая плитка НЕ дубль
                    else :
                        if tile_is_DUO :
                            TOTAL_Y["up"] += 36
                            tile_x = previous_position[0] - 17
                            tile_y = previous_position[1] - 36

                        else :
                            TOTAL_Y["up"] += 70
                            orientation = "vertical"
                            tile_x = previous_position[0]
                            tile_y = previous_position[1] - 70

            #играйте в правильном направлении
            else :

                #это первая плитка, которая будет воспроизведена ПРАВИЛЬНО
                if this_is_first_RIGHT_tile :
                    this_is_first_RIGHT_tile = 0

                    #предыдущая плитка была - дубль
                    if previous_tile_is_DUO :
                        tile_x = previous_position[0] + 70
                        tile_y = previous_position[1]
                        reverse_tile = 1

                    #предыдущая плитка НЕ дубль
                    else :
                        if tile_is_DUO :
                            TOTAL_Y["up"] += 36
                            tile_x = previous_position[0] - 17
                            tile_y = previous_position[1] - 36


                            this_is_first_RIGHT_tile = 1

                        else :

                            TOTAL_Y["up"] += 36
                            tile_x = previous_position[0] + 36
                            tile_y = previous_position[1]
                            reverse_tile = 1

                #это НЕ первая плитка, которую нужно разыграть ПРАВИЛЬНО
                else :

                    #предыдущая плитка была - дубль
                    if previous_tile_is_DUO :
                        tile_x = previous_position[0] + 36
                        tile_y = previous_position[1] + 17
                        reverse_tile = 1

                    #предыдущая плитка НЕ дубль
                    else :

                        if tile_is_DUO :
                            orientation = "vertical"
                            tile_x = previous_position[0] + 70
                            tile_y = previous_position[1] - 17

                        else :
                            tile_x = previous_position[0] + 70
                            tile_y = previous_position[1]
                            reverse_tile = 1

        #ДОБАВЬТЕ ВОСПРОИЗВЕДЕННУЮ ПЛИТКУ В СПИСОК Пользователя
        PLAYED_TILES.insert(0, [tile, (tile_x, tile_y)])


    #если плитка будет разыгрываться в правильном направлении
    elif place == "right" :

        #Создание нескольких переменных, чтобы облегчить понимание кода
        previous_tile = PLAYED_TILES[-1][0]
        previous_position = PLAYED_TILES[-1][1]

        previous_tile_is_DUO = 0

        if previous_tile[0] == previous_tile[1] :
            previous_tile_is_DUO = 1

        #Играйте в правильном направлении
        if TOTAL_X["right"] < main_window_resolution[0]//2 - 150 :

            #если эта плитка является дублем
            if tile_is_DUO :
                TOTAL_X["right"] += 36
                orientation = "vertical"
                tile_x = previous_position[0] + 70
                tile_y = previous_position[1] - 17

            #если эта плитка не является дублем
            else :

                if previous_tile_is_DUO :
                    TOTAL_X["right"] += 70
                    tile_x = previous_position[0] + 36
                    tile_y = previous_position[1] + 17

                else :
                    TOTAL_X["right"] += 70
                    tile_x = previous_position[0] + 70
                    tile_y = previous_position[1]

        #дошел до правого конца окна
        else :

            #ход в направлении вниз
            if TOTAL_Y["down"] < main_window_resolution[1]//4 - 110 :

                #это первая плитка, которая будет воспроизведена в направлении вниз
                if this_is_first_DOWN_tile :
                    this_is_first_DOWN_tile = 0

                    #если предыдущая плитка была - дубль
                    if previous_tile_is_DUO :
                        TOTAL_Y["down"] += 104  #34 + 70
                        orientation = "vertical"
                        tile_x = previous_position[0]
                        tile_y = previous_position[1] + 70

                    #если предыдущая плитка НЕ дубль
                    else :

                        if tile_is_DUO :
                            orientation = "vertical"
                            tile_x = previous_position[0] + 70
                            tile_y = previous_position[1] - 17

                            this_is_first_DOWN_tile = 1

                        else :
                            TOTAL_Y["down"] += 87  #17 + 70
                            orientation = "vertical"
                            tile_x = previous_position[0] + 34
                            tile_y = previous_position[1] + 36

                #это НЕ первая плитка, которая воспроизводится в направлении вниз
                else :

                    #если предыдущая плитка была дубль
                    if previous_tile_is_DUO :
                        TOTAL_Y["down"] += 70
                        orientation = "vertical"
                        tile_x = previous_position[0] + 17
                        tile_y = previous_position[1] + 36

                    #если предыдущая плитка НЕ была дубль
                    else :

                        if tile_is_DUO :
                            TOTAL_Y["down"] += 36
                            tile_x = previous_position[0] - 17
                            tile_y = previous_position[1] + 36

                        else :
                            TOTAL_Y["down"] += 70
                            orientation = "vertical"
                            tile_x = previous_position[0]
                            tile_y = previous_position[1] + 70

            #ВОСПРОИЗВЕДЕНИЕ В ЛЕВОМ НАПРАВЛЕНИИ (ПЕРЕВЕРНУТЫЕ ПЛИТКИ)
            else :

                #если эта плитка является первой плиткой, которая будет воспроизведена слева
                if this_is_first_LEFT_tile :
                    this_is_first_LEFT_tile = 0

                    #если предыдущая плитка была дубль
                    if previous_tile_is_DUO :
                        TOTAL_Y["down"] += 36
                        tile_x = previous_position[0] - 70
                        tile_y = previous_position[1]
                        reverse_tile = 1

                    #если предыдущая плитка не была дубль
                    else :

                        if tile_is_DUO :
                            TOTAL_Y["down"] += 36
                            tile_x = previous_position[0] - 17
                            tile_y = previous_position[1] + 70


                            this_is_first_LEFT_tile = 1

                        else :

                            TOTAL_Y["down"] += 36
                            tile_x = previous_position[0] - 70
                            tile_y = previous_position[1] + 34
                            reverse_tile = 1

                #если эта плитка НЕ является первой плиткой, которая будет воспроизведена СЛЕВА
                else :

                    #если предыдущая плитка была дубль
                    if previous_tile_is_DUO :
                        TOTAL_Y["down"] += 36
                        tile_x = previous_position[0] - 70
                        tile_y = previous_position[1] + 17
                        reverse_tile = 1

                    #если предыдущая плитка НЕ была дубль
                    else :

                        if tile_is_DUO :
                            orientation = "vertical"
                            tile_x = previous_position[0] - 36
                            tile_y = previous_position[1] - 17

                        else :
                            TOTAL_Y["down"] += 36
                            tile_x = previous_position[0] - 70
                            tile_y = previous_position[1]
                            reverse_tile = 1

        #ДОБАВЬТЕ ВОСПРОИЗВЕДЕННУЮ ПЛИТКУ В СПИСОК Пользователья
        PLAYED_TILES.append([tile,(tile_x, tile_y)])



    else :
        raise ValueError

    #Создание объекта плитки
    if reverse_tile :
        temp_tile = Tile(tile[1], tile[0], screen, tile_x, tile_y)
    else :
        temp_tile = Tile(tile[0], tile[1], screen, tile_x, tile_y)

    #покажите плитку в соответствии с ее подходящей ориентацией
    if orientation == "horizontal" :
        temp_tile.show_horizontal()

    else :
        temp_tile.show_vertical()

def computer_play(auto_player, screen):

        #эта функция берет объект изображение, затем выполняет все необходимые действия, связанные с ботом.


    #определение PASS как глобальную переменную
    global __PASS__


    #Попросите компьютер воспроизвести
    chosen_tile = auto_player.play(PLAYED_TILES)

    if chosen_tile != "PASS" :
        final_tile = tile_check(chosen_tile[0])
        pygame.time.wait(1000)
        pygame.event.clear()
        play(final_tile[0], screen, final_tile[1])
        hide_tile(chosen_tile[1][0], chosen_tile[1][1], screen)

        #установите для  PASS значение off
        __PASS__ = 0

        #обновите дисплей
        pygame.display.update()

    #если выделается "PASS"
    else :

        #Если пользователь выбрал "PASS" в прошлый раз, завершите игру
        if __PASS__ == 1 :
            END_GAME(screen)
            return


        else :
            ############
            __PASS__ = 1

            computer_note_x = main_window_resolution[0]//2 - 196
            computer_note_y = main_window_resolution[1]//2 - 190

            computer_note_img = pygame.image.load("images/comppas.png")
            clear_img = pygame.image.load("images/zad.png")




            screen.blit(computer_note_img,(computer_note_x,computer_note_y))
            pygame.display.update()
            pygame.time.wait(2000)
            screen.blit(clear_img,(computer_note_x,computer_note_y))


    #проверьте, может ли пользователь играть.
    if not human_has_suitable_tile() :

        #если компьютер сдался в прошлый раз, то игра окончена
        if __PASS__ == 1 :
            END_GAME(screen)

        #если игра не закончена, измените изображение кнопки на зеленое
        else :
            switch_pass_button("enable", screen)

#----------------------------------------------------------------------------

def human_play(tile, exact_tile, screen, position, auto_player):

        #эта функция отвечает за все действия, которые должны быть предприняты, когда человек нажимает на подходящую плитку.


    global __PASS__



    #фишка пользователя
    play(exact_tile, screen, position)
    HUMAN_TILES.remove(tile)
    hide_tile(tile[1][0], tile[1][1], screen)


    __PASS__ = 0


    pygame.display.update()

    #проверьте, выставил ли пользователь свои плитки
    if len(HUMAN_TILES) == 0 :
        END_GAME(screen)

    #если пользователь не выставил свои плитки
    else :

        #попросите компьютер воспроизвести
        computer_play(auto_player, screen)

        #проверьте, выставил ли компьютер свои плитки
        if len(COMPUTER_TILES) == 0 :
            END_GAME(screen)

        #проверьте, не может ли пользователь играть.
        elif not human_has_suitable_tile() :

            #если компьютер сдался, то игра окончена
            if __PASS__ == 1 :
                END_GAME(screen)

            #если игра не закончена, измените изображение кнопки  на зеленое
            else :
                switch_pass_button("enable", screen)

#----------------------------------------------------------------------------

def hide_tile(x, y, screen):

        #эта функция принимает положение плитки, а затем принимает цвет, определенный в глобальной переменной HIDE_TILE_COLOR.


    hiding_rectangle = Rect(x, y, 34, 68)
    pygame.draw.rect(screen, HIDE_TILE_COLOR, hiding_rectangle)

#----------------------------------------------------------------------------

def clear_area(x, y, width, height, screen, fill_color):

       # эта функция скрывает все, что имеет желаемый цвет.


    hiding_rectangle = Rect(x, y, width, height)
    pygame.draw.rect(screen, fill_color, hiding_rectangle)

#----------------------------------------------------------------------------

def switch_pass_button(action, screen):

        #переключает кнопку PASS в положение "включено" или "отключено" в соответствии с действием, которое вы передаете ему.


    #инициализируйте PASS_BUTTON_STATUS как глобальную переменную
    global PASS_BUTTON_STATUS

    #действие заключается в отключении кнопки пропуска
    if action == "enable" :

        #очистите место кнопки пропуска
        clear_area(PASS_BUTTON_PLACE[0], PASS_BUTTON_PLACE[1], 99, 44, screen, OUTER_COLOR)

        #измените изображение кнопки передачи обратно на зеленый цвет
        pass_button_image = pygame.image.load("images/propusk.png")
        screen.blit(pass_button_image, (PASS_BUTTON_PLACE[0], PASS_BUTTON_PLACE[1]))

        #измените PASS_BUTTON_STATUS, чтобы он был включен
        PASS_BUTTON_STATUS = 1

        #обновите дисплей
        pygame.display.update()


    #действие заключается в том, чтобы включить кнопку пропуска
    elif action == "disable":

        #очистите место кнопки пропуска
        clear_area(PASS_BUTTON_PLACE[0], PASS_BUTTON_PLACE[1], 99, 44, screen, OUTER_COLOR)

        #измените изображение кнопки передачи обратно на красный цвет
        pass_button_image = pygame.image.load("images/pered_propuskom.png")
        screen.blit(pass_button_image, (PASS_BUTTON_PLACE[0], PASS_BUTTON_PLACE[1]))

        #измените PASS_BUTTON_STATUS на отключенный
        PASS_BUTTON_STATUS = 0

        #обновите экран
        pygame.display.update()


    #если действие неправильное
    else :
        raise ValueError

#----------------------------------------------------------------------------

def human_has_suitable_tile():

        #эта функция возвращает значение True, если есть какая-либо плитка для воспроизведения в списке Ваши фишки.



    if len(PLAYED_TILES) == 0 :
        return True

    left_value = PLAYED_TILES[0][0][0]
    right_value = PLAYED_TILES[-1][0][1]

    for tile in HUMAN_TILES :

        #если мы нашли подходящую плитку
        if (left_value in tile[0]) or (right_value in tile[0]) :
            return True

        else :
            continue

    #если цикл завершен, не найдя ни одной подходящей плитки
    return False



def left_or_right(screen):

#эта функция вызывается всякий раз, когда пользователь нажимает на плитку, которую можно
#воспроизводить с обеих сторон, затем он выполняет все необходимые действия, то есть либо сходить влево, либо вправо.


    left_image = pygame.image.load("images/levo.png")
    right_image = pygame.image.load("images/pravo.png")

    x1 = PASS_BUTTON_PLACE[0] + 5
    y1 = PASS_BUTTON_PLACE[1] - 30

    x2 = PASS_BUTTON_PLACE[0] + 62
    y2 = PASS_BUTTON_PLACE[1] - 30

    for i in range(2) :

        screen.blit(left_image,(x1, y1))
        screen.blit(right_image,(x2, y2))

        pygame.display.update()

        pygame.time.wait(200)

        clear_area(x1, y1, 100, 22, screen, OUTER_COLOR)

        pygame.display.update()

        pygame.time.wait(200)

    screen.blit(left_image,(x1, y1))
    screen.blit(right_image,(x2, y2))

#----------------------------------------------------------------------------

def check_if_clicked_on_exit(screen, x, y, check_for_popup = 0):

        #эта функция проверяет, нажал ли пользователь на кнопку "выйти". или кнопки "заново", затем он выполняет необходимые действия


    #Проверка того, нажал ли пользователь на кнопку ВОСПРОИЗВЕДЕНИЯ
    if x > REPLAY_BUTTON_PLACE[0] and x < (REPLAY_BUTTON_PLACE[0] + 81)\
     and y > REPLAY_BUTTON_PLACE[1] and y< (REPLAY_BUTTON_PLACE[1] + 29) :

        pressed_replay = pygame.image.load("images/zanovo2.png")
        screen.blit(pressed_replay, (REPLAY_BUTTON_PLACE[0], REPLAY_BUTTON_PLACE[1]))
        pygame.display.update()
        pygame.time.wait(100)
        RESET_GAME()


    #Проверка того, нажал ли пользователь на кнопку ВЫХОДА
    elif x > EXIT_BUTTON_PLACE[0] and x < (EXIT_BUTTON_PLACE[0] + 81)\
     and y > EXIT_BUTTON_PLACE[1] and y< (EXIT_BUTTON_PLACE[1] + 29) :

        pressed_exit = pygame.image.load("images/vyhood2.png")
        screen.blit(pressed_exit,(EXIT_BUTTON_PLACE[0], EXIT_BUTTON_PLACE[1]))
        pygame.display.update()
        pygame.time.wait(100)
        exit()


    #если пользователь тоже хочет проверить всплывающее сообщение
    if check_for_popup == 1 :

        #Загрузка выделенного изображениея
        button_highlight_img = pygame.image.load("images/chto3.png")

        #получение места всплывающего сообщения
        popup_x = main_window_resolution[0]//2 - 252
        popup_y = main_window_resolution[1]//2 - 173

        #если игрок нажал на кнопку выхода во всплывающем сообщении
        if x > (popup_x + 113) and x < (popup_x + 230)\
         and y > (popup_y + 286) and y< (popup_y + 334) :
            screen.blit(button_highlight_img,(popup_x + 115,popup_y + 288))
            pygame.display.update()
            pygame.time.wait(100)
            #выход из игры
            exit()

        #если игрок нажал на кнопку воспроизведения во всплывающем сообщении
        elif x > (popup_x + 278) and x < (popup_x + 395)\
         and y > (popup_y + 288) and y< (popup_y + 336) :
            screen.blit(button_highlight_img,(popup_x + 278,popup_y + 288))
            pygame.display.update()
            pygame.time.wait(500)
            #перезагрузка игры
            RESET_GAME()

#----------------------------------------------------------------------------

def check_if_clicked_on_pass(screen, auto_player, x, y):

     #эта функция проверяет, нажал ли человек на кнопку PASS.


    global __PASS__

    #Проверка того, нажал ли пользователь на кнопку "PASS"
    if x > PASS_BUTTON_PLACE[0] and x < (PASS_BUTTON_PLACE[0] + 99)\
     and y > PASS_BUTTON_PLACE[1] and y < (PASS_BUTTON_PLACE[1] + 44):

        #если у пользователя есть какие-либо подходящие плитки для игры, игнорировать
        if human_has_suitable_tile() :

            #загрузка требуемого изображения
            bad_pass = pygame.image.load("images/fishki_estb.png")
            clear_img = pygame.image.load("images/zad.png")


            note_x = main_window_resolution[0]//2 - 196
            note_y = main_window_resolution[1] - main_window_resolution[1]/4 -35

            #просмотр заметки и воспроизведение звука
            screen.blit(bad_pass,(note_x, note_y))
            pygame.display.update()
            pygame.time.wait(2000)
            screen.blit(clear_img,(note_x,note_y))

        #если у пользователя нет подходящих плиток для игры.
        else :
            #проверьте, включена ли кнопка, завершите игру
            if __PASS__ == 1 :
                END_GAME(screen)

            else :


                __PASS__ = 1

                #отключение кнопки пропуска
                switch_pass_button("disable", screen)

                #попросите компьютер суграть
                computer_play(auto_player, screen)

                #проверяет, выложил ли компьютер свои плитки
                if len(COMPUTER_TILES) == 0 :
                    END_GAME(screen)

        return True

    else :
        return False

#----------------------------------------------------------------------------

def score_count(WHOS_TILE):

       # эта функция принимает "список плиток" и возвращает количество баллов.


    tiles_length = len(WHOS_TILE)
    tiles_count = 0
    for i in range(0, tiles_length):
        tiles_count += WHOS_TILE[i][0][0]
        tiles_count += WHOS_TILE[i][0][1]
    return tiles_count

#----------------------------------------------------------------------------

def END_GAME(screen):

     #Эта функция вызывается, когда игра заканчивается. Она определяет, кто выиграл, и показывает определённое сообщение




    game_over_bg = pygame.image.load("images/konec.png")
    won_game_img = pygame.image.load("images/izi_vin.png")
    lose_game_img = pygame.image.load("images/izi_luz.png")
    game_drawn_img = pygame.image.load("images/nichya.png")


    draw_x = main_window_resolution[0]//2 - 252
    draw_y = main_window_resolution[1]//2 - 173

    #определение GAME_OVER как глобальную переменную
    global GAME_OVER

    #установление для  GAME_OVER значение on
    GAME_OVER = 1

    #подсчитайте очки как у пользователя, так и у компьютера
    human_score = score_count(HUMAN_TILES)
    computer_score = score_count(COMPUTER_TILES)


    #Вы выиграли
    if human_score < computer_score :

        screen.blit(game_over_bg,(draw_x,draw_y))
        screen.blit(won_game_img,(draw_x + 120, draw_y + 220))

    #Если вы выиграли
    elif human_score > computer_score:
        screen.blit(game_over_bg,(draw_x,draw_y))
        screen.blit(lose_game_img,(draw_x + 141, draw_y + 220))

    #если игра закончилась вничью
    else:
        screen.blit(game_over_bg,(draw_x,draw_y))
        screen.blit(game_drawn_img,(draw_x + 187, draw_y + 220))


    #построение шрифта и вывод его на экран
    font = pygame.font.SysFont("arial", 25)
    screen.blit(font.render(str(human_score),True,(0,0,0)),(draw_x + 365,draw_y + 113))
    screen.blit(font.render(str(computer_score),True,(0,0,0)),(draw_x + 365,draw_y + 166))

#----------------------------------------------------------------------------

def RESET_GAME():

       #Сбрасывает все игровые счетчики и фишки, перераспределяет новые фишки для всех игроков и перерисовывает все на экране.


    global __PASS__
    global NUMBER_OF_PLAYERS
    global HUMAN_TILES
    global COMPUTER_TILES
    global PLAYED_TILES
    global REPLAY_BUTTON_PLACE
    global EXIT_BUTTON_PLACE
    global PASS_BUTTON_PLACE
    global TOTAL_X
    global TOTAL_Y
    global this_is_first_DOWN_tile
    global this_is_first_LEFT_tile
    global this_is_first_UP_tile
    global this_is_first_RIGHT_tile
    global GAME_OVER
    global BOTH_SIDES
    global ARGUMENTATIVE_TILE
    global ARGUMENTATIVE_RESULT
    global PASS_BUTTON_STATUS


    __PASS__ = 0
    NUMBER_OF_PLAYERS = 2

    HUMAN_TILES = []
    COMPUTER_TILES = []

    PLAYED_TILES = []

    REPLAY_BUTTON_PLACE = [0, 0]
    EXIT_BUTTON_PLACE = [0, 0]
    PASS_BUTTON_PLACE = [0, 0]

    TOTAL_X = {"left":0, "right":0}
    TOTAL_Y = {"up":0, "down":0}

    this_is_first_DOWN_tile = 1
    this_is_first_LEFT_tile = 1
    this_is_first_UP_tile = 1
    this_is_first_RIGHT_tile = 1

    GAME_OVER = 0

    BOTH_SIDES = 0

    ARGUMENTATIVE_TILE = None
    ARGUMENTATIVE_RESULT = None

    PASS_BUTTON_STATUS = 0
    main()



def main():


#Инициализирует игру и запускает основной игровой цикл.


    #определение глобальные переменные
    global __PASS__
    global GAME_OVER
    global BOTH_SIDES
    global ARGUMENTATIVE_TILE
    global ARGUMENTATIVE_TILE_CHECK_RESULT


    note_x = main_window_resolution[0]//2 - 196
    note_y = main_window_resolution[1] - main_window_resolution[1]//4 -35
    pygame.init()


    seticon('images/icon.png')

    #Главное окно
    screen = pygame.display.set_mode(main_window_resolution,FULLSCREEN, 32)
    pygame.display.set_caption("Dominos!")



    #загрузка изображений
    bad_tile = pygame.image.load("images/ne_podhodit.png")
    clear_img = pygame.image.load("images/zad.png")

    #инициализация в игру
    initialize(screen)
    auto_player = computer(COMPUTER_TILES)


    while True:

        event = pygame.event.wait()


        if event.type == QUIT:
            exit()


        elif GAME_OVER == 1 :


            if event.type == MOUSEBUTTONDOWN :

                #установите положение мыши
                x, y = event.pos

                #проверьте, нажал ли пользователь на кнопки выхода или воспроизведения
                check_if_clicked_on_exit(screen, x, y, 1)



        #Обработка событий Мыши, ЕСЛИ ИГРОК МОЖЕТ ИГРАТЬ НА ОБЕИХ СТОРОНАХ
        elif BOTH_SIDES == 1 :

            if event.type == MOUSEBUTTONDOWN :

                #установите положение мыши
                x, y = event.pos

                #проверьте, нажал ли пользователь на кнопки выхода или воспроизведения
                check_if_clicked_on_exit(screen, x, y)

                #на место стрелок
                x1 = PASS_BUTTON_PLACE[0] + 5
                y1 = PASS_BUTTON_PLACE[1] - 30
                x2 = PASS_BUTTON_PLACE[0] + 62
                y2 = PASS_BUTTON_PLACE[1] - 30

                #если пользователь решил играть слева
                if x > x1 and x < (x1 + 30) and y > y1 and y < (y1 + 22) :

                    #уберите стрелки с экрана
                    clear_area(x1, y1, 100, 22, screen, OUTER_COLOR)
                    pygame.display.update()
                    BOTH_SIDES = 0

                    human_play(ARGUMENTATIVE_TILE, ARGUMENTATIVE_RESULT[2], screen, ARGUMENTATIVE_RESULT[3], auto_player)

                #если пользователь решил играть справа
                elif x > x2 and x < (x2 + 30) and y > y2 and y < (y2 + 22) :

                    #уберите стрелки с экрана
                    clear_area(x1, y1, 100, 22, screen, OUTER_COLOR)
                    pygame.display.update()
                    BOTH_SIDES = 0

                    human_play(ARGUMENTATIVE_TILE, ARGUMENTATIVE_RESULT[0], screen, ARGUMENTATIVE_RESULT[1], auto_player)



        #Обработка событий Мыши, ЕСЛИ ИГРА ВСЕ ЕЩЕ ЗАПУЩЕНА
        elif event.type == MOUSEBUTTONDOWN :

            #установите положение мыши
            x,y = event.pos

            check_if_clicked_on_exit(screen, x, y)

            #Проверка того, нажал ли пользователь на кнопку "PASS"
            if check_if_clicked_on_pass(screen, auto_player, x, y):
                continue

            #проверьте, нажал ли пользователь на плитку
            else :


                for tile in HUMAN_TILES :

                    #если пользователь нажал на плитку
                    if clicked_on_tile(event.pos, tile[1]):

                        #проверьте, где играть
                        result = tile_check(tile[0])

                        #если пользователь нажал на НЕПОДХОДЯЩУЮ плитку
                        if result is None :

                            screen.blit(bad_tile,(note_x,note_y))
                            pygame.display.update()
                            pygame.time.wait(2000)
                            screen.blit(clear_img,(note_x,note_y))

                        #если пользователь нажал на подходящую
                        elif len(result) == 2 :
                            human_play(tile, result[0], screen, result[1], auto_player)

                        #если плитка может быть воспроизведена с обеих сторон
                        elif len(result) == 4 :
                            BOTH_SIDES = 1
                            ARGUMENTATIVE_TILE = tile
                            ARGUMENTATIVE_RESULT = result
                            left_or_right(screen)

        # нажмите Esc, чтобы выйти
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit()

        pygame.display.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())