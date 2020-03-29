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


def send_message(_id, messege, keyboard=None):
    if last_messenges.get(int(_id), "") != messege:
        last_messenges[int(_id)] = messege
        vk.method("messages.send",
                  {"peer_id": _id,
                   "message": str(messege),
                   "random_id": randint(1, 2147483647),
                   "keyboard": keyboard})





# функция для генерации вопросов и ответов(параша)
def generatequestion(deep=0, sub=1, div="1"):
    question = []
    answers = []
    debag_func("инициализация списков **generatequestion")
    file = open('questions/question_' + str(subgects_key[int(sub)]) + '_' + str(div) + '.txt', encoding='utf-8')
    text = file.readlines()
    file.close()
    shuffle(text)
    for i in text[:5]:
        temp = i[:-1]  # убираем

        debag_func(str([temp]) + " - случайный вопрос из файла **generatequestion")
        if "&" in temp:
            quest, answs = temp.split("&")
            good_ans = []
            answs = [((i.strip().replase("!", ""),
                       good_ans.append(ind))[0] if "!" in i else i.strip())
                     for ind, i in enumerate(answs.split(';'))]
            answers.append([good_ans[:], answs[:]])
            question.append(quest)
        elif temp[-1] == '.':
            answers.append([1, ["Да", "Нет"]])
            question.append(temp[:-1])

        else:
            answers.append([0, ["Да", "Нет"]])
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
'''