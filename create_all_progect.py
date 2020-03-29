main = """from funcs import *
from structs import *
from vk_buttons import *


# Главный цикл
text = ""
while True:
    try:
        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
        if messages["count"] >= 1:
            ID = messages["items"][0]["last_message"]["from_id"]
            last_text = text
            text = messages["items"][0]["last_message"]["text"]
            statusID[ID] = statusID.get(ID, 0)

            # Выводит StatusID(для дебага)
            if text.lower() == '/id':
                debag_func("id")
                send_message(ID, statusID[ID])

            # Начать --> Выбор предмета
            elif text.lower() == 'начать' and statusID[ID] == 0:
                debag_func("начать")
                send_message(ID, "Выберите предмет", keyboard=buttonsItemsChoice)

            # Выбор предмета --> Выбор дивизиона/Обратно к предметам
            elif text.lower() in ['информатика', 'математика', "физика"] and statusID[ID] == 0:
                debag_func("выбор предмета")
                send_message(ID, "Выбери дивизион", keyboard=buttonsDivChoice)
                statusID[ID] = (['информатика', 'математика', "физика"].index(text.lower()) + 1) * 10
                print("************", ID, statusID[ID])

            # Выбор дивизиона --> Поиск противника
            elif text.lower() in map(lambda x: x.lower(), DIVISIONS) and statusID[ID] // 10 != 0:
                debag_func("выбор дивизиона")
                statusID[ID] += int(text[-1])
                print("******------", ID, statusID[ID])
                start_battle(ID)
                '''
                # Нет противника
                if search[statusID[ID] // 10 - 1][statusID[ID] % 10 - 1] == -1:
                    search[statusID[ID] // 10 - 1][statusID[ID] % 10 - 1] = ID
                    print(statusID[ID] // 10 - 1, statusID[ID] % 10 - 1)
                    temp = 'Поиск противника'
                    send_message(ID, temp, keyboard=buttonReturn)
                # Противник в очереди
                else:
                    id1 = search[statusID[ID] // 10 - 1][statusID[ID] % 10 - 1]
                    print("id1 - ", id1, "id2 - ", ID)
                    temp = 'Противник найден'
                    print("test 1")
                    q, a = generatequestion(sub=statusID[ID] // 10, div=statusID[ID] % 10)
                    print("len(q)", len(q), " len(a)", len(a))
                    print(*search, (statusID[ID] // 10 - 1, statusID[ID] % 10 - 1), sep='\n')
                    print(search[statusID[ID] // 10 - 1][statusID[ID] % 10 - 1])
                    print("--", q)
                    print("++", a)

                    battles.append(Battle(id1, ID,
                                          statusID[ID] // 10 - 1,
                                          statusID[ID] % 10 - 1,
                                          q, a))

                    print("test 2")
                    statusID[search[statusID[ID] // 10 - 1][statusID[ID] % 10 - 1]] = 100 + countOfBattles
                    print("test 3")
                    search[statusID[ID] // 10 - 1][statusID[ID] % 10 - 1] = -1
                    print("test 4")
                    statusID[ID] = 100 + countOfBattles
                    countOfBattles += 1
                    print("test 5")
                    for i in [battles[-1].id1, battles[-1].id2]:
                        message = temp + "\n\nПервый вопрос:\n" + battles[-1].questions[0]
                        send_message(i, message, keyboard=buttonsChoice)

                    print("test 6")
                '''

            elif text.lower() == "возобновить поиск":
                statusID[ID] = int(100*statusID[ID])
                send_message(ID, "поиск противника...", keyboard=buttonReturn)

            # Возрат из div к предметам --> Выбор предметов
            elif text.lower() == 'к предметам':
                debag_func("к предметам")
                send_message(ID, "Опять ты?", keyboard=buttonsItemsChoice)

                statusID[ID] = 0

            # Остановить поиск --> Выбор предметов
            elif text.lower() == 'остановить поиск' and '0' not in str(statusID[ID]):
                search[statusID[ID] // 10 - 1][statusID[ID] % 10 - 1] = -1
                statusID[ID] = 0
                debag_func("остановить поиск")
                send_message(ID, "Поиск остановлен", keyboard=buttonsItemsChoice)

            elif text.lower() == 'бросить вызов' and statusID[ID] % 10 != 0:
                print("бросить вызов")
                if statusID[ID] == int(statusID[ID]): # если еще не бросал вызов
                    print("бросить вызов в первый раз", statusID[ID])
                    search[statusID[ID] // 10 - 1][statusID[ID] % 10 - 1] = -1
                    statusID[ID] = statusID[ID]/100
                    print(statusID[ID])

                send_message(ID, "выбери друга для батла:\n https://vk.com/friends и вставь его id сюда")

            #  отправка приглашения на батл
            elif 0 < statusID[ID] < 1 and text != last_text:
                text = formating_id(text)
                print("--------text", text)
                if text and not(-1 < statusID.get(int(text), 0) < 0):
                    text = int(text)
                    print("вас пригласили на батл")
                    try:
                        print('1')
                        send_message(text, "вас пригласили на батл", keyboard=buttonsAgree)
                        send_message(ID, "Друг был приглашен на батл, ожидайте ответа")
                        print(2)
                        statusID[text] = -statusID[ID]
                        print("statusID[text]", statusID[text], text)
                        calls_dict[ID] = text
                        calls_dict[text] = ID
                    except Exception as e:
                        print("----", e)
                        send_message(ID, "Не получилось пригласить на батл", keyboard=buttonAfterBadСall)
                        if "Can't send messages for users without permission" in str(e):
                            send_message(ID,"Бот не может отправлять сообщения этому человеку. Попросите его отправить сообщение боту, переслав эту ссылку")
                            send_message(ID, "https://vk.com/markovbt")
                elif type(text) == "NoneType":
                    print(5)
                    send_message(ID, "человека с таким ID не было найдено", keyboard=buttonAfterBadСall)
                else:
                    print(6)
                    send_message(ID, "произошло какое-то недоразумение, попробуйте ввести другого человека", keyboard=buttonAfterBadСall)

            # если противник отказался от батла
            elif (-1 < statusID[ID] < 0 or calls_dict.get(ID, "--") != "--") and text == "Отбой":
                statusID[ID] = 0
                send_message(calls_dict[ID], "друг отказался от батла", keyboard=buttonAfterBadСall)
                send_message(ID, "вы отказались от батла")
                del calls_dict[calls_dict[ID]]
                del calls_dict[ID]

            # если противник согласился на батл
            elif (-1 < statusID[ID] < 0 or calls_dict.get(ID, "--") != "--") and text == "Согласен":
                temp = "Батл начался"
                send_message(calls_dict[ID], "друг согласился, начинаем бой")
                statusID[ID] = int(abs(statusID[ID]) * 100) if statusID[ID] % 1 != 0 else int(statusID[ID])
                q, a = generatequestion(sub=statusID[ID] // 10, div=statusID[ID] % 10)
                battles.append(Battle(calls_dict[ID], ID,
                                      statusID[ID] // 10 - 1,
                                      statusID[ID] % 10 - 1,
                                      q, a))
                statusID[ID] = 100 + countOfBattles
                for i in [battles[-1].id1, battles[-1].id2]:
                    message = temp + "\n\nПервый вопрос:\n" + battles[-1].questions[0]
                    send_message(i, message, keyboard=buttonsChoice)
                    statusID[i] = 100 + countOfBattles

                countOfBattles += 1


            elif statusID[ID] >= 100 and text.lower() in ['да', 'нет']:
                debag_func("ожидание ответа при бое")
                battlesID = statusID[ID] - 100
                temp = "если вы это читаете, значит что-то пошло не так...((("
                q = "тут должен быть ворпос, но что-то пошло не так...((("
                flag = True
                if battles[battlesID].id1 == ID:

                    if len(battles[battlesID].questions) > battles[battlesID].counter1 + 1:
                        battles[battlesID].counter1 += 1
                        loc_cnt = battles[battlesID].counter1
                        print('сейчас попытка индекса 1', end=' ')
                        q = battles[battlesID].questions[loc_cnt]
                        print("которая прошла успешно")
                    else:
                        battles[battlesID].counter1 += 1
                        loc_cnt = battles[battlesID].counter1
                        flag = False
                    print('сейчас попытка индекса 2', end=' ')
                    if battles[battlesID].answers[loc_cnt - 1] and text.lower() == 'да' or \
                            not (battles[battlesID].answers[loc_cnt - 1]) and text.lower() == 'нет':
                        print("верный ответ на вопрос (id1)", end=' ')
                        temp = 'Верно, '
                        battles[battlesID].point1 += 1
                    else:
                        temp = 'Неверно, '
                        print("неверный ответ на вопрос (id2)")
                    print("которая прошла успешно")


                elif battles[battlesID].id2 == ID:
                    if len(battles[battlesID].questions) > battles[battlesID].counter2 + 1:
                        battles[battlesID].counter2 += 1
                        loc_cnt = battles[battlesID].counter2
                        print('сейчас попытка индекса 3', end=' ')
                        q = battles[battlesID].questions[loc_cnt]
                        print("которая прошла успешно")
                    else:
                        battles[battlesID].counter2 += 1
                        loc_cnt = battles[battlesID].counter2
                        flag = False
                    print('сейчас попытка индекса 4', end=' ')
                    if battles[battlesID].answers[loc_cnt - 1] and text.lower() == 'да' or \
                            not (battles[battlesID].answers[loc_cnt - 1]) and text.lower() == 'нет':
                        print("верный ответ на вопрос (id2)", end=' ')
                        temp = 'Верно, '
                        battles[battlesID].point2 += 1
                    else:
                        print("неверный ответ на вопрос (id2)")
                        temp = 'Неверно, '
                    print("которая прошла успешно")

                if flag:
                    print("--=-=-=-=-=")
                    send_message(ID, temp + "\n\nCледующий вопрос:\n" + q,
                                 keyboard=buttonsChoice)

                else:
                    print("flag", flag)
                    if statusID[battles[battlesID].id1] == 98 or statusID[battles[battlesID].id2] == 98:
                        print("бой закончен")
                        score = str(battles[battlesID].point1) + ":" + str(battles[battlesID].point2)

                        if battles[battlesID].point1 > battles[battlesID].point2:
                            temp1 = "Победа)"
                            temp2 = "Луз(("
                        elif battles[battlesID].point1 < battles[battlesID].point2:
                            temp1 = "Луз(("
                            temp2 = "Победа)"
                        else:
                            temp1 = "Ничья"
                            temp2 = "Ничья"
                        send_message(ID, temp + "\n\nБой окончен!", keyboard=buttonsChoice)

                        for i in [[battles[battlesID].id1, temp1], [battles[battlesID].id2, temp2]]:
                            send_message(i[0], score + " " + i[1], keyboard=buttonsItemsChoice)

                            statusID[i[0]] = 0
                        battles[battlesID] = "тут был батл, но он закончился"
                    else:
                        print("ожидаю окончание собеседника....")
                        statusID[ID] = 98
                        send_message(ID, temp + "Ожидайте соперника...")


            # ОшибкаID
            else:
                print("ОшибкаID ", str(ID), str(statusID[ID]) , text)
                print(-1 < statusID[ID] < 0 or calls_dict.get(ID, "--") != "--", text.lower() == "cогласен")
                if statusID[ID] == 0:
                    localKeyboard = buttonsItemsChoice
                elif statusID[ID] >= 100:
                    localKeyboard = buttonsChoice
                elif statusID[ID] // 10 != 0:
                    localKeyboard = buttonsDivChoice
                elif statusID[ID] == 98:
                    localKeyboard = ''
                elif 0 < statusID[ID] < 1: #ожидаем, когда игрок скинет ID противника
                    localKeyboard = ''
                elif -1 < statusID[ID] < 0: #ожидаем, когда игрок согласится на батл
                    localKeyboard = ''
                else:
                    localKeyboard = buttonReturn
                send_message(ID, "Ошибка, так нельзя(((", keyboard=localKeyboard)

    except Exception as E:
        time.sleep(1)
        print("не опознанная ошибка", E)
        try:
            if "Can't send messages for users without permission" in str(E):
                send_message(ID, "Бот не может отправлять сообщения этому человеку. Попросите его отправить сообщение боту, переслав эту ссылку")
                send_message(ID, "https://vk.com/markovbt")
        except Exception as e:
            print("повторная ошибка", e)
"""

vk_buttons = """from lib import *



# доп функция для кнопок (так удобнее)
def create_button(label, color, payload=''):
    return {
        "action": {
            "type": "text",
            "payload": json.dumps(payload),
            "label": label
        },
        "color": color
    }

# кнопки выбора предметов
buttonsItemsChoice = {
    "one_time": True,
    "buttons": [
        [create_button('Информатика', 'primary')],
        [create_button('Математика', 'primary')],
        [create_button('Физика', 'primary')]
    ]}
buttonsItemsChoice = json.dumps(buttonsItemsChoice, ensure_ascii=False).encode('utf-8')
buttonsItemsChoice = str(buttonsItemsChoice.decode('utf-8'))

# кнопки выбора дивизиона
DIVISIONS = ["Div 1", "Div 2", "Div 3"]
buttonsDivChoice = {
    "one_time": True,
    "buttons": [
        [
            create_button(div, 'primary')
            for div in DIVISIONS
        ],
        [
            create_button('К предметам', 'secondary')
        ]
    ]}
buttonsDivChoice = json.dumps(buttonsDivChoice, ensure_ascii=False).encode('utf-8')
buttonsDivChoice = str(buttonsDivChoice.decode('utf-8'))

# кнопка возрата
buttonReturn = {
    "one_time": True,
    "buttons": [
        [create_button('бросить вызов', 'primary')],
        [create_button('Остановить поиск', 'secondary')]

    ]}
buttonReturn = json.dumps(buttonReturn, ensure_ascii=False).encode('utf-8')
buttonReturn = str(buttonReturn.decode('utf-8'))

# кнопки выбора
buttonsChoice = {
    "one_time": True,
    "buttons": [
        [
            (create_button('Нет', 'negative')),
            (create_button('Да', 'positive'))
        ]
        # // Кнопка выхода из боя("сдаться")
    ]}
buttonsChoice = json.dumps(buttonsChoice, ensure_ascii=False).encode('utf-8')
buttonsChoice = str(buttonsChoice.decode('utf-8'))

# кнопки выбора
buttonsAgree = {
    "one_time": True,
    "buttons": [
        [
            (create_button('Отбой', 'negative')),
            (create_button('Согласен', 'positive'))
        ]
    ]}
buttonsAgree = json.dumps(buttonsAgree, ensure_ascii=False).encode('utf-8')
buttonsAgree = str(buttonsAgree.decode('utf-8'))


buttonAfterBadСall = {
    "one_time": True,
    "buttons": [
        [create_button('бросить вызов', 'primary')],
        [create_button('возобновить поиск', 'primary')],
        [create_button('к предметам', 'secondary')]

    ]}
buttonAfterBadСall = json.dumps(buttonAfterBadСall, ensure_ascii=False).encode('utf-8')
buttonAfterBadСall = str(buttonAfterBadСall.decode('utf-8'))
"""
structs = """from lib import *


# структура для хранения информации о текущих битвах(так удобнее)
@dataclass  # ничего подобного, оно должно реализовываться по-другому
class Battle:
    id1: int
    id2: int
    sub: int
    div: int
    questions: list
    answers: list
    point1: int = 0
    point2: int = 0
    counter1: int = 0
    counter2: int = 0


# Словарь состояний
statusID = {}

# Массив очереди
search = [[-1] * 3 for _ in range(3)]

# Массив боёв
battles = []

#массив вызовов на бой
calls = []
calls_dict = dict()

# переменная для подсчета кол-во боев(зачем она?)
countOfBattles = 0

subgects_key = {1: "inf", 2: "mat", 3: "phys"} """

funcs = """from lib import *
from structs import *
from vk_buttons import *

def formating_id(herf):
    if herf.isdigit():
        return herf
    if herf[:4] == "http":
        herf = herf.split("://vk.com/")[1]
    if herf[2:].isdigit():
        return herf[2:]
    else:
        try:
            user_id = vk.method("utils.resolveScreenName", {"screen_name": herf})['object_id']
            print(user_id)
            return user_id
        except Exception as e:
            print("произошла какая-то ошибка при выяснении id пользователя", e)
    return None


def start_battle(ID):
    # Нет противника
    if search[statusID[ID] // 10 - 1][statusID[ID] % 10 - 1] == -1:
        search[statusID[ID] // 10 - 1][statusID[ID] % 10 - 1] = ID
        print(statusID[ID] // 10 - 1, statusID[ID] % 10 - 1)
        temp = 'Поиск противника'
        send_message(ID, temp, keyboard=buttonReturn)
    # Противник в очереди
    else:
        id1 = search[statusID[ID] // 10 - 1][statusID[ID] % 10 - 1]
        print("id1 - ", id1, "id2 - ", ID)
        temp = 'Противник найден'
        print("test 1")
        q, a = generatequestion(sub=statusID[ID] // 10, div=statusID[ID] % 10)
        print("len(q)", len(q), " len(a)", len(a))
        print(*search, (statusID[ID] // 10 - 1, statusID[ID] % 10 - 1), sep='\n')
        print(search[statusID[ID] // 10 - 1][statusID[ID] % 10 - 1])
        print("--", q)
        print("++", a)

        battles.append(Battle(id1, ID,
                              statusID[ID] // 10 - 1,
                              statusID[ID] % 10 - 1,
                              q, a))

        print("test 2")
        statusID[search[statusID[ID] // 10 - 1][statusID[ID] % 10 - 1]] = 100 + countOfBattles
        print("test 3")
        search[statusID[ID] // 10 - 1][statusID[ID] % 10 - 1] = -1
        print("test 4")
        statusID[ID] = 100 + countOfBattles
        countOfBattles += 1
        print("test 5")
        for i in [battles[-1].id1, battles[-1].id2]:
            message = temp + "\n\nПервый вопрос:\n" + battles[-1].questions[0]
            send_message(i, message, keyboard=buttonsChoice)

        print("test 6")


def send_message(id, messege, keyboard=None):
    vk.method("messages.send",
              {"peer_id": id,
               "message": str(messege),
               "random_id": randint(1, 2147483647),
               "keyboard": keyboard})





# функция для генерации вопросов и ответов(параша)
def generatequestion(deep=0, sub=1, div="1"):
    question = []
    answers = []
    debag_func("инициализация списков **generatequestion")
    # s = randomlist5()
    file = open('questions/question_' + str(subgects_key[int(sub)]) + '_' + str(div) + '.txt', encoding='utf-8')
    # s = randomlist5()
    #file = open('question.txt', encoding='utf-8')
    text = file.readlines()
    file.close()
    shuffle(text)
    for i in text[:5]:
        temp = i[:-1]  # убираем \n
        debag_func(str([temp]) + " - случайный вопрос из файла **generatequestion")
        if temp[-1] == '.':
            answers.append(True)
            question.append(temp[:-1])
        else:
            answers.append(False)
            question.append(temp)
    if question == [] and deep < 10:
        question, answers = generatequestion(deep=deep + 1, sub=sub, div=div)
    return question, answers

debag_func = lambda st, flag=debagFlag: print(st) if flag[0] else st









'''
# функция для генерации списка из 5 рандомных чисел
# теперь не нужна (вроде)
def randomlist5():
    lst = []
    while len(lst) < 5:
        t = randint(1, 10)
        if t not in lst:
            lst.append(t)
    return lst
'''"""

lib = """from dataclasses import dataclass, field
import time
from random import shuffle, random, randint
import json

import vk_api

#from config import cfg

debagFlag = [True]

token = "ac7b695bc7d4e43747629c8918a08aada6954976ccfe5e9db4c9756675b7c9230a6ef46e481258629730b"
vk = vk_api.VkApi(token=token)

print(type(None))"""

qwest = """Динамическое программирование в теории управления и теории вычислительных систем — способ решения сложных задач путём разбиения их на более простые подзадачи.
Примеры алгоритма устойчивой сортировки - это сортировка пузырьком и сортировка слиянием.
Блочная сортировка и сортировка подсчетом - это алгоритмы, не основанные на сравнениях.
Рекурсия — определение, описание, изображение какого-либо объекта или процесса внутри самого этого объекта или процесса, то есть ситуация, когда объект является частью самого себя.
Жадный алгоритм — алгоритм, заключающийся в принятии локально оптимальных решений на каждом этапе, допуская, что конечное решение также окажется оптимальным.
Цикл называется Эйлеровым циклом, если граф имеет цикл, содержащий все рѐбра графа по одному разу.
Примеры алгоритма устойчивой сортировки - это пирамидальная сортировка и быстрая сортировка
Динамическое программирование в теории управления и теории вычислительных систем — способ решения сложных задач с использованием искусственного интеллекта
Граф — абстрактный географический объект, представляющий собой множество вершин графа и набор рёбер, то есть соединений между парами вершин
Жадный алгоритм — алгоритм, подразумевающий решение задач в лоб, не тратя много времени на обдумывание задачи"""

_dict = {"main.py": main,
         "vk_buttons.py": vk_buttons,
         "structs.py": structs,
         "funcs.py": funcs,
         "lib.py": lib}

from os import mkdir

try:
    mkdir("bot/questions")
except Exception:
    pass

f = open('forbidden_list.txt', "w")
f.close()

for i in _dict:
    f = open("bot/" + i, "w")
    f.write(_dict[i])
    f.close()

for i in ["inf_", "mat_", "phys_"]:
    for j in range(1, 4):
        f = open("bot/questions/question_" + i + str(j), "w")
        f.write(qwest)
        f.close()
