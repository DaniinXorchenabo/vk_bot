from lib import *


def send_message(id, messege, keyboard=None):
    vk.method("messages.send",
              {"peer_id": id,
               "message": str(messege),
               "random_id": randint(1, 2147483647),
               "keyboard": keyboard})


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