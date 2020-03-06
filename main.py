from funcs import *
from structs import *
from vk_buttons import *

# токен группы
vk = vk_api.VkApi(token=cfg.get("vk", "token"))

# переменная для подсчета кол-во боев(зачем она?)
countOfBattles = 0


subgects_key = {1: "inf", 2: "mat", 3: "phys"}

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
