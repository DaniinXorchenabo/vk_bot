from funcs import *
from structs import *
from vk_buttons import *


#print(*generatequestion(sub=1, div=2), sep="\n")


work_in_forbidden_list("w")

forbidden_list = work_in_forbidden_list("r")  # ['189276351', "-189276351"]



# Главный цикл
text = ""
while True:
    try:
        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
        if messages["count"] >= 1:
            ID = messages["items"][0]["last_message"]["from_id"]

            last_text = text
            text = messages["items"][0]["last_message"]["text"]
            if "Проверьте свои личные данные, данная группа была взломана!" in text:
                continue
            statusID[ID] = statusID.get(ID, 0)
            if str(ID) in forbidden_list:
                work_in_forbidden_list("del", ID)

            # Выводит StatusID (для дебага)
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

            elif text.lower() == "возобновить поиск":
                print(*search, statusID[ID], sep="\n")
                statusID[ID] = int(100 * statusID[ID])
                start_battle(ID)
                # send_message(ID, "поиск противника...", keyboard=buttonReturn)

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
                print(*search, statusID[ID], sep="\n")
                print("бросить вызов")
                if statusID[ID] == int(statusID[ID]):
                    # если еще не бросал вызов
                    search[statusID[ID] // 10 - 1][statusID[ID] % 10 - 1] = -1
                    statusID[ID] = statusID[ID] / 100
                send_message(ID, """выбери друга для батла:
                                    https://vk.com/friends и вставь его id (или ссылку) сюда""")
                print(*search, statusID[ID], sep="\n")

            #  отправка приглашения на батл
            elif 0 < statusID[ID] < 1 and text != last_text:
                print(*search, statusID[ID], sep="\n")
                text = formating_id(text)
                print("--------text", text)
                if text and not (-1 < statusID.get(int(text), 0) < 0):
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
                            send_message(ID,
                                         "Бот не может отправлять сообщения этому человеку. Попросите его отправить сообщение боту, переслав эту ссылку")
                            send_message(ID, "https://vk.com/markovbt")
                elif type(text) == "NoneType":
                    print(5)
                    send_message(ID, "человека с таким ID не было найдено", keyboard=buttonAfterBadСall)
                else:
                    print(6)
                    print(*search, sep="\n")
                    send_message(ID, "произошло какое-то недоразумение, попробуйте ввести другого человека",
                                 keyboard=buttonAfterBadСall)

            # если противник отказался от батла
            elif (-1 < statusID[ID] < 0 or calls_dict.get(ID, "--") != "--") and text == "Отбой":
                statusID[ID] = 0
                send_message(calls_dict[ID], "друг отказался от батла", keyboard=buttonAfterBadСall)
                send_message(ID, "вы отказались от батла")
                del calls_dict[calls_dict[ID]]
                del calls_dict[ID]

            # если противник согласился на батл
            elif (-1 < statusID[ID] < 0 or calls_dict.get(ID, "--") != "--") and text == "Согласен":
                statusID[ID] = int(abs(statusID[ID]) * 100) if statusID[ID] % 1 != 0 else int(statusID[ID])
                create_battle(ID, calls_dict.get(ID, "--"))
                send_message(calls_dict[ID], "друг согласился, начинаем бой")
                send_first_question("Батл начался")

            elif statusID[ID] >= 100 and len(battles) > statusID[ID] - 100 and check_correct_answer(ID, text):
                answ_and_qw(ID, text)

            # ОшибкаID
            else:
                print("ОшибкаID ", str(ID), str(statusID[ID]), text)
                print(-1 < statusID[ID] < 0 or calls_dict.get(ID, "--") != "--", text.lower() == "cогласен")
                if statusID[ID] == 0:
                    localKeyboard = buttonsItemsChoice
                elif statusID[ID] >= 100:
                    localKeyboard = buttonsChoice
                elif statusID[ID] // 10 != 0:
                    localKeyboard = buttonsDivChoice
                elif statusID[ID] == 98:
                    localKeyboard = ''
                elif 0 < statusID[ID] < 1:  # ожидаем, когда игрок скинет ID противника
                    localKeyboard = ''
                elif -1 < statusID[ID] < 0:  # ожидаем, когда игрок согласится на батл
                    localKeyboard = ''
                else:
                    localKeyboard = buttonReturn
                if str(ID) not in forbidden_list:
                    print([ID])
                    send_message(ID, "Ошибка, так нельзя(((", keyboard=localKeyboard)

    except FileNotFoundError as E:
        time.sleep(1)
        print("не опознанная ошибка", E)
        try:
            if "Can't send messages for users without permission" in str(E):
                send_message(ID,
                             "Бот не может отправлять сообщения этому человеку. Попросите его отправить сообщение боту, переслав эту ссылку")
                send_message(ID, "https://vk.com/markovbt")
        except Exception as e:
            print("повторная ошибка", e)
            if "Can't send messages for users without permission" in str(e):
                work_in_forbidden_list('a', ID)
                forbidden_list.append(str(ID))
                print(f"ID {ID} добавлено в чкрный список")
