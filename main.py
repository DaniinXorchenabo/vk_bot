from dataclasses import dataclass, field
import time
from random import shuffle, random, randint
import json

import vk_api

from config import cfg

# токен группы
vk = vk_api.VkApi(token=cfg.get("vk", "token"))

# переменная для подсчета кол-во боев(зачем она?)
countOfBattles = 0

debagFlag = [True]
debag_func = lambda st, flag=debagFlag: print(st) if flag[0] else st
subgects_key = {1: "inf", 2: "mat", 3: "phys"}


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


# функция для генерации списка из 5 рандомных чисел
# теперь не нужна (вроде)
def randomlist5():
    lst = []
    while len(lst) < 5:
        t = randint(1, 10)
        if t not in lst:
            lst.append(t)
    return lst


# функция для генерации вопросов и ответов(параша)
def generatequestion(deep=0, sub=1, div="1"):
    question = []
    answers = []
    debag_func("инициализация списков **generatequestion")
    # s = randomlist5()
    file = open('questions/question_' + str(subgects_key[int(sub)]) + '_' + str(div) + '.txt', encoding='utf-8')
    # s = randomlist5()
    file = open('question.txt', encoding='utf-8')
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

# Словарь состояний
statusID = {}

# Массив очереди
search = [[-1] * 3 for _ in range(3)]

# Массив боёв
battles = []

# Главный цикл
while True:
    try:
        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
        if messages["count"] >= 1:

            ID = messages["items"][0]["last_message"]["from_id"]
            text = messages["items"][0]["last_message"]["text"]
            statusID[ID] = statusID.get(ID, 0)

            # Выводит StatusID(для дебага)
            if text.lower() == '/id':
                debag_func("id")
                vk.method("messages.send",
                          {"peer_id": ID,
                           "message": str(statusID[ID]),
                           "random_id": randint(1, 2147483647)})

            # Начать --> Выбор предмета
            elif text.lower() == 'начать' and statusID[ID] == 0:
                debag_func("начать")
                vk.method("messages.send",
                          {"peer_id": ID,
                           "message": "Выберите предмет",
                           "random_id": randint(1, 2147483647),
                           "keyboard": buttonsItemsChoice})

            # Выбор предмета --> Выбор дивизиона/Обратно к предметам
            elif text.lower() in ['информатика', 'математика', "физика"] and statusID[ID] == 0:
                debag_func("выбор предмета")
                vk.method("messages.send",
                          {"peer_id": ID,
                           "message": "Выбери дивизион",
                           "random_id": randint(1, 2147483647),
                           "keyboard": buttonsDivChoice})
                statusID[ID] = (['информатика', 'математика', "физика"].index(text.lower()) + 1) * 10
                print("************", ID, statusID[ID])
            # Выбор дивизиона --> Поиск противника
            elif text.lower() in map(lambda x: x.lower(), DIVISIONS) and statusID[ID] // 10 != 0:
                debag_func("выбор дивизиона")
                statusID[ID] += int(text[-1])
                print("******------", ID, statusID[ID])
                # Нет противника
                if search[statusID[ID] // 10 - 1][statusID[ID] % 10 - 1] == -1:
                    search[statusID[ID] // 10 - 1][statusID[ID] % 10 - 1] = ID
                    print(statusID[ID] // 10 - 1, statusID[ID] % 10 - 1)
                    temp = 'Поиск противника'
                    vk.method("messages.send",  # отображение надписи противник найден для второго человека
                              {"peer_id": ID,
                               "message": temp,
                               "random_id": randint(1, 2147483647),
                               "keyboard": buttonReturn})
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
                        vk.method("messages.send",  # отображение надписи противник найден
                                  {"peer_id": i,
                                   "message": temp + "\n\nПервый вопрос:\n" + battles[statusID[ID] - 100].questions[0],
                                   "random_id": randint(1, 2147483647),
                                   "keyboard": buttonsChoice})
                        '''
                        vk.method("messages.send",
                                  {"peer_id": i,
                                   "message": battles[statusID[ID] - 100].questions[0],
                                   "random_id": randint(1, 2147483647),
                                   "keyboard": buttonsChoice})
                        '''
                    print("test 6")
            # Возрат из div к предметам --> Выбор предметов
            elif text.lower() == 'к предметам':
                debag_func("к предметам")
                vk.method("messages.send",
                          {"peer_id": ID,
                           "message": "Опять ты?",
                           "random_id": randint(1, 2147483647),
                           "keyboard": buttonsItemsChoice})
                statusID[ID] = 0

            # Остановить поиск --> Выбор предметов
            elif text.lower() == 'остановить поиск' and '0' not in str(statusID[ID]):
                debag_func("остановить поиск")
                vk.method("messages.send",
                          {"peer_id": ID,
                           "message": "Поиск остановлен",
                           "random_id": randint(1, 2147483647),
                           "keyboard": buttonsItemsChoice})
                search[statusID[ID] // 10 - 1][statusID[ID] % 10 - 1] = -1
                statusID[ID] = 0

            # Типо бой(ВНИМАНИЕ БУДЬТЕ АКУРАТНЕЕ ПРИСУТСТВУЕТ ГОВНОКОД, ПО ВОЗМОЖНОСТЕ ПЕРЕПИШИТЕ ПО НОРМАЛЬНОМУ!!!!!)
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
                    vk.method("messages.send",
                              {"peer_id": ID,
                               "message": temp + "\n\nCледующий вопрос:\n" + q,
                               "random_id": randint(1, 2147483647),
                               "keyboard": buttonsChoice})
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
                        vk.method("messages.send",
                                  {"peer_id": ID,
                                   "message": temp + "\n\nБой окончен!",
                                   "random_id": randint(1, 2147483647),
                                   "keyboard": buttonsChoice})
                        for i in [[battles[battlesID].id1, temp1], [battles[battlesID].id2, temp2]]:
                            vk.method("messages.send",
                                      {"peer_id": i[0],
                                       "message": score + " " + i[1],
                                       "random_id": randint(1, 2147483647),
                                       "keyboard": buttonsItemsChoice})
                            statusID[i[0]] = 0
                        battles[battlesID] = "тут был батл, но он закончился"
                    else:
                        print("ожидаю окончание собеседника....")
                        statusID[ID] = 98
                        vk.method("messages.send", {
                            "peer_id": ID,
                            "message": temp + "Ожидайте соперника...",
                            "random_id": randint(1, 2147483647)
                        })

            # ОшибкаID
            else:
                debag_func("ОшибкаID")
                if statusID[ID] == 0:
                    localKeyboard = buttonsItemsChoice
                elif statusID[ID] >= 100:
                    localKeyboard = buttonsChoice
                elif statusID[ID] // 10 != 0:
                    localKeyboard = buttonsDivChoice
                elif statusID[ID] == 98:
                    localKeyboard = ''
                else:
                    localKeyboard = buttonReturn
                vk.method("messages.send",
                          {"peer_id": ID,
                           "message": "Ошибка, так нельзя(((",
                           "random_id": randint(1, 2147483647),
                           "keyboard": localKeyboard})

    except Exception as E:
        time.sleep(1)
        print("не опознанная ошибка", E)
