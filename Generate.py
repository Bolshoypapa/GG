from random import randrange

def generate_tiles():

       #эта функция ничего не принимает и возвращает полный список костяшек из 28 элементов
   # каждый элемент этого списка является «кортежем»

    temp = []
    for i in range(0,7):
        for j in range(i,7):
            temp.append((i,j))
    return temp


def distribute_tiles(tiles_set, players_count):

        #Принимает полный список домино каждый список содержит 7 плиток в виде кортежей.

    #проверztn правильность количества игроков
    if players_count > 4 :
        raise ValueError

    #создаёт пустой список списков для хранения фишек игрока
    final_list= [[] for x in range(players_count)]

    #заполняет «final_list» случайными плитками
    for i in range(0, 7):
        for j in range(players_count):
            random_number = randrange(0, len(tiles_set))
            final_list[j].append(tiles_set.pop(random_number))

    return final_list


