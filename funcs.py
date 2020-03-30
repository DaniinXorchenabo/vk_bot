from lib import *
from structs import *
from vk_buttons import *


def work_in_forbidden_list(work="w", _list=[]):
    if work == "w":
        with open("forbidden_list.txt", "w") as f:
            f.write("\n".join(list(map(str, _list))))
    elif work == "a":
        if type(_list) != list:
            _list = [str(_list)]
        with open("forbidden_list.txt", "a") as f:
            f.write("\n" + "\n".join(list(map(str, _list))))
    elif work == "del":
        if type(_list) != list:
            _list = [str(_list)]
        _list = map(str, _list)
        with open("forbidden_list.txt", "+") as f:
            forbidden_list_new = f.read().split()
            for i in _list:
                forbidden_list_new.remove(i)
            f.write("\n".join(list(map(str, forbidden_list_new))))
    elif work == "r":
        with open("forbidden_list.txt", "r") as f:
            return f.read().split()


def formating_id(herf):
    if herf.isdigit():
        return herf
    if "@" in herf:
        herf = herf.split()[-1]
    if herf[:4] == "http":
        herf = herf.split("://vk.com/")[1]
    if herf[2:].isdigit() and herf[:2] == "id":
        return herf[2:]
    else:
        try:
            user_id = vk.method("utils.resolveScreenName", {"screen_name": herf})['object_id']
            print(user_id)
            return user_id
        except Exception as e:
            print("произошла какая-то ошибка при выяснении id пользователя", e)
    return None


def start_battle(ID, text=''):  # начало батла, созданного при поиске в таблице
    global countOfBattles
    # Нет противника
    if search[id_info[ID].statusID // 10 - 1][id_info[ID].statusID % 10 - 1] in [-1, ID]:
        search[id_info[ID].statusID // 10 - 1][id_info[ID].statusID % 10 - 1] = ID
        print(id_info[ID].statusID // 10 - 1, id_info[ID].statusID % 10 - 1)
        temp = 'Поиск противника'
        send_message(ID, temp, keyboard=buttonReturn, text=text)
    # Противник в очереди
    else:
        temp = 'Противник найден'
        create_battle(ID, search[id_info[ID].statusID // 10 - 1][id_info[ID].statusID % 10 - 1])
        send_first_question(temp, text=text)


def answ_and_qw(ID, text):
    battlesID = id_info[ID].statusID - 100
    temp = "если вы это читаете, значит что-то пошло не так...((("
    q = "тут должен быть ворпос, но что-то пошло не так...((("
    flag = True
    loc_buttle = battles[battlesID]
    buttle_hum = [i for i in loc_buttle.people if i.id == ID]
    if bool(buttle_hum):
        buttle_hum = buttle_hum[0]
        if len(loc_buttle.questions) > buttle_hum.counter + 1:
            buttle_hum.counter += 1
            loc_cnt = buttle_hum.counter
            print('сейчас попытка индекса 1', end=' ')
            q = loc_buttle.questions[loc_cnt]
            print("которая прошла успешно")
        else:
            buttle_hum.counter += 1
            loc_cnt = buttle_hum.counter
            flag = False
        print(loc_buttle.good_answers, loc_cnt - 1)
        if len(loc_buttle.good_answers) > loc_cnt - 1:
            if loc_buttle.good_answers[loc_cnt - 1] == text:
                print("верный ответ на вопрос (id1)", end=' ')
                temp = 'Верно, '
                buttle_hum.point += 1
            else:
                temp = 'Неверно, '
                print("неверный ответ на вопрос (id2)")
        else:
            temp = "произошла какая-то ошибка"
        print("которая прошла успешно", loc_buttle.answers[loc_cnt - 1], text)
    else:
        return None

    if flag:
        print("--=-=-=-=-=")
        print("--", loc_buttle.answers[buttle_hum.counter - 1])
        keywordd = ganerate_answer_button(*loc_buttle.answers[buttle_hum.counter - 1])
        print("answ_and_qw", keywordd)
        send_message(ID, temp + "\n\nCледующий вопрос:\n" + q,
                     keyboard=keywordd, text=text)

    else:
        print("flag", flag)
        if bool([i for i in battles[battlesID].people if id_info[i.id].statusID == 98]):
            print("бой закончен")
            score = ":".join([str(i.point) for i in battles[battlesID].people])
            print("score", score)
            temps = ["Победа)"] + [str(i) + " место" for i in range(2, len(loc_buttle.people))] + ["Луз(("]
            sort_id = sorted([(i.id, i.point) for i in loc_buttle.people],
                             key=lambda i: i[1],
                             reverse=True)

            send_message(ID, temp + "\n\nБой окончен!", text=text,
                         keyboard=buttonsChoice)

            for ind, [_id, point] in enumerate(sort_id):
                send_message(_id, score + " " + temps[ind], text=text,
                             keyboard=buttonsItemsChoice)
                id_info[_id].statusID = 0
            battles[battlesID] = "тут был батл, но он закончился"
        else:
            print("ожидаю окончание собеседника....")
            id_info[ID].statusID = 98
            send_message(ID, temp + "Ожидайте соперника...", text=text)


def send_first_question(temp, text=''):
    for i in battles[-1].people:
        message = temp + "\n\nПервый вопрос:\n" + battles[-1].questions[0]
        print(battles[-1].answers[0])
        send_message(i.id, message, text=text,
                     keyboard=ganerate_answer_button(*battles[-1].answers[0]))


def create_battle(ID, id1=None):
    global countOfBattles
    if not bool(id1):
        id1 = search[id_info[ID].statusID // 10 - 1][id_info[ID].statusID % 10 - 1]
    battles.append(create_battle_obj([id1, ID],
                                     id_info[ID].statusID // 10 - 1,
                                     id_info[ID].statusID % 10 - 1,
                                     *generatequestion(sub=id_info[ID].statusID // 10,
                                                       div=id_info[ID].statusID % 10)
                                     )
                   )
    if id_info[ID].statusID % 1 == 0:
        search[id_info[ID].statusID // 10 - 1][id_info[ID].statusID % 10 - 1] = -1
    id_info[ID].statusID = 100 + countOfBattles
    id_info[id1].statusID = 100 + countOfBattles
    print("=======! create_battle !=======")
    print(ID, id1)
    countOfBattles += 1


def send_message(_id, messege, keyboard=None, text=''):
    print(f"попытка отправеи сообщения человеку {_id}")
    if not(id_info.get(int(_id))) or (id_info[int(_id)].last_messenge != messege) or text != id_info[int(_id)].last_come_messenge:
        id_info[int(_id)] = id_info.get(int(_id), idInfo(0))
        print(f"отправка сообщения человеку {_id}")
        id_info[int(_id)].last_messenge = messege
        id_info[int(_id)].last_keyboard = keyboard
        _dict = {"peer_id": _id,
                 "message": str(messege),
                 "random_id": randint(1, 2147483647),
                 "keyboard": keyboard}
        vk.method("messages.send", _dict)
    else:
        print((id_info[int(_id)].last_messenge != messege), text != id_info[int(_id)].last_come_messenge)
        print(id_info[int(_id)].last_messenge, messege, text, id_info[int(_id)].last_come_messenge )

# функция для генерации вопросов и ответов(параша)
def generatequestion(deep=0, sub=1, div="1"):
    question = []
    answers = []
    good_answers = []
    debag_func("инициализация списков **generatequestion")
    file = open('questions/question_' + str(subgects_key[int(sub)]) + '_' + str(div) + '.txt', encoding='utf-8')
    text = file.readlines()
    file.close()
    shuffle(text)
    for i in text[:5]:
        temp = i.strip() # убираем \n

        debag_func(str([temp]) + " - случайный вопрос из файла **generatequestion")
        if "&" in temp:
            quest, answs = temp.split("&")
            answers.append([((i.strip().replace("!", ""),
                              good_answers.append(i.replace("!", "")))[0] if "!" in i else i.strip())
                            for ind, i in enumerate(answs.split(';'))])
            # answers.append(answs)
            question.append(quest)
        elif temp[-1] == '.':
            answers.append(["Нет", "Да"])
            good_answers.append("Да")
            question.append(temp[:-1])
        else:
            answers.append(["Нет", "Да"])
            good_answers.append("Нет")
            question.append(temp)
    if question == [] and deep < 10:
        question, answers, good_answers = generatequestion(deep=deep + 1, sub=sub, div=div)
    return question, answers, good_answers


debag_func = lambda st, flag=debagFlag: print(st) if flag[0] else st


def mechanics_of_dialogue():
    pass


def create_battle_obj(ids: list, sub: int, div: int,
                      questions: list,
                      answers: list,
                      good_answers: list):
    return Battle(sub, div, questions, answers, good_answers, [Participant(_id) for _id in ids])


def ganerate_answer_button(*buttons: list, size=2):
    print("-=-=-=-=-********", buttons)
    if bool(buttons):
        if len(buttons) and "Да" in buttons and "Нет" in buttons:
            print("buttonsChoice")
            return buttonsChoice
        else:
            _len = len(buttons)
            print("generate_bot")
            return create_all_button(
                *[[(buttons[i + j]) for j in range((
                    _len - i if 0 < _len - i < size else size
                ))]
                  for i in range(0, _len, size)]
            )


def check_correct_answer(ID, text):
    loc_battles = battles[id_info[ID].statusID - 100]
    if text in list(chain(
            *[loc_battles.answers[i.counter]
              for i in loc_battles.people if i.counter < len(loc_battles.answers)])):
        return True
