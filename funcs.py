from lib import *
from structs import *
from vk_buttons import *


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
'''