from funcs import *
from structs import *
from vk_buttons import *

# print(*generatequestion(sub=1, div=2), sep="\n")


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
            id_info[ID] = id_info.get(ID, idInfo(0,
                                                 last_keyboard=buttonsItemsChoice))
            if str(ID) in forbidden_list:
                work_in_forbidden_list("del", ID)

            # Выводит StatusID (для дебага)
            if text.lower() == '/id':
                debag_func("id")
                send_message(ID, id_info[ID].statusID)

            # Начать --> Выбор предмета
            elif text.lower() == 'начать' and id_info[ID].statusID == 0:
                debag_func("начать")
                send_message(ID, "Выберите предмет", keyboard=buttonsItemsChoice)

            # Выбор предмета --> Выбор дивизиона/Обратно к предметам
            elif text.lower() in ['информатика', 'математика', "физика"] and id_info[ID].statusID == 0:
                debag_func("выбор предмета")
                send_message(ID, "Выбери дивизион", keyboard=buttonsDivChoice)
                id_info[ID].statusID = (['информатика', 'математика', "физика"].index(text.lower()) + 1) * 10
                print("************", ID, id_info[ID].statusID)

            # Выбор дивизиона --> Поиск противника
            elif text.lower() in map(lambda x: x.lower(), DIVISIONS) and id_info[ID].statusID // 10 != 0:
                debag_func("выбор дивизиона")
                id_info[ID].statusID += int(text[-1])
                print("******------", ID, id_info[ID].statusID)
                start_battle(ID, text=text)

            elif text.lower() == "возобновить поиск":
                print(*search, id_info[ID].statusID, sep="\n")
                id_info[ID].statusID = int(100 * id_info[ID].statusID)
                start_battle(ID, text=text)
                # send_message(ID, "поиск противника...", keyboard=buttonReturn)

            # Возрат из div к предметам --> Выбор предметов
            elif text.lower() == 'к предметам':
                debag_func("к предметам")
                send_message(ID, "Опять ты?", keyboard=buttonsItemsChoice)
                id_info[ID].statusID = 0

            # Остановить поиск --> Выбор предметов
            elif text.lower() == 'остановить поиск' and '0' not in str(id_info[ID].statusID):
                search[id_info[ID].statusID // 10 - 1][id_info[ID].statusID % 10 - 1] = -1
                id_info[ID].statusID = 0
                debag_func("остановить поиск")
                send_message(ID, "Поиск остановлен", keyboard=buttonsItemsChoice)

            elif text.lower() == 'бросить вызов' and id_info[ID].statusID % 10 != 0:
                print(*search, id_info[ID].statusID, sep="\n")
                print("бросить вызов")
                if id_info[ID].statusID == int(id_info[ID].statusID):
                    # если еще не бросал вызов
                    search[id_info[ID].statusID // 10 - 1][id_info[ID].statusID % 10 - 1] = -1
                    id_info[ID].statusID = id_info[ID].statusID / 100
                send_message(ID, """выбери друга для батла:
                                    https://vk.com/friends и вставь его id (или ссылку) сюда""")
                print(*search, id_info[ID].statusID, sep="\n")

            #  отправка приглашения на батл
            elif 0 < id_info[ID].statusID < 1 and text != last_text:
                print(*search, id_info[ID].statusID, sep="\n")
                text = formating_id(text)
                print("--------text", text)
                if text and not (id_info.get(int(text)) and (-1 < id_info[int(text)].statusID < 0)):
                    text = int(text)
                    print("вас пригласили на батл")
                    try:
                        assert ID != text
                        print('1')
                        send_message(text, "вас пригласили на батл", keyboard=buttonsAgree)
                        send_message(ID, "Друг был приглашен на батл, ожидайте ответа")
                        print(2)
                        id_info[text].statusID = -id_info[ID].statusID
                        print("id_info[text].statusID", id_info[text].statusID, text)
                        calls_dict[ID] = text
                        calls_dict[text] = ID
                    except AssertionError:
                        send_message(ID, "Тёмные силы не разрешают приглашать на батл самого себя!",
                                     keyboard=buttonAfterBadСall)
                    except vk_api.exceptions.ApiError:
                        send_message(ID, """Бот не может отправлять сообщения этому человеку.
                                      Попросите его отправить сообщение боту, переслав эту ссылку""")
                        send_message(ID, "https://vk.com/markovbt", keyboard=buttonAfterBadСall)
                    except FileNotFoundError as e11:
                        print("error in отправеке приглажения на батл", e11)
                        send_message(ID, "Не получилось пригласить на батл", keyboard=buttonAfterBadСall)

                elif type(text) == "NoneType":
                    print(5)
                    send_message(ID, "человека с таким ID не было найдено", keyboard=buttonAfterBadСall)
                else:
                    print(6)
                    print(*search, sep="\n")
                    send_message(ID, "произошло какое-то недоразумение, попробуйте ввести другого человека",
                                 keyboard=buttonAfterBadСall)

            # если противник отказался от батла
            elif (-1 < id_info[ID].statusID < 0 or calls_dict.get(ID, "--") != "--") and text == "Отбой":
                id_info[ID].statusID = 0
                send_message(calls_dict[ID], "друг отказался от батла", keyboard=buttonAfterBadСall)
                send_message(ID, "вы отказались от батла")
                del calls_dict[calls_dict[ID]]
                del calls_dict[ID]

            # если противник согласился на батл
            elif (-1 < id_info[ID].statusID < 0 or calls_dict.get(ID, "--") != "--") and text == "Согласен":
                id_info[ID].statusID = int(abs(id_info[ID].statusID) * 100) if id_info[ID].statusID % 1 != 0 else int(
                    id_info[ID].statusID)
                create_battle(ID, calls_dict.get(ID, "--"))
                send_message(calls_dict[ID], "друг согласился, начинаем бой")
                send_first_question("Батл начался")

            elif id_info[ID].statusID >= 100 and len(battles) > id_info[ID].statusID - 100 and check_correct_answer(ID,
                                                                                                                    text):
                answ_and_qw(ID, text)

            # ОшибкаID
            else:
                print("ОшибкаID ", str(ID), str(id_info[ID].statusID), text)
                print(-1 < id_info[ID].statusID < 0 or calls_dict.get(ID, "--") != "--", text.lower() == "cогласен")
                if id_info[ID].statusID == 0:
                    localKeyboard = id_info[ID].last_keyboard
                elif id_info[ID].statusID >= 100:
                    localKeyboard = id_info[ID].last_keyboard
                elif id_info[ID].statusID // 10 != 0:
                    localKeyboard = buttonsDivChoice
                elif id_info[ID].statusID == 98:
                    localKeyboard = id_info[ID].last_keyboard
                elif 0 < id_info[ID].statusID < 1:  # ожидаем, когда игрок скинет ID противника
                    localKeyboard = ''
                elif -1 < id_info[ID].statusID < 0:  # ожидаем, когда игрок согласится на батл
                    localKeyboard = ''
                else:
                    localKeyboard = id_info[ID].last_keyboard
                if str(ID) not in forbidden_list:
                    print([ID])
                    send_message(ID, "Ошибка, так нельзя(((", keyboard=localKeyboard)
    except vk_api.exceptions.ApiError:
        try:
            send_message(ID, """Бот не может отправлять сообщения этому человеку.
                                Попросите его отправить сообщение боту, переслав эту ссылку""")
            send_message(ID, "https://vk.com/markovbt", keyboard=id_info[ID].last_keyboard)
        except vk_api.exceptions.ApiError:
            work_in_forbidden_list(work='a', _list=ID)
            forbidden_list.append(str(ID))
            print(f"ID {ID} добавлено в чкрный список")
        except Exception as e:
            print("повторная ошибка", e)
    except FileNotFoundError as E:
        time.sleep(1)
        print("не опознанная ошибка", E)
