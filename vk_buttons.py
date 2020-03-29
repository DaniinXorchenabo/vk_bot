from lib import *
from structs import *


def create_all_button(*strings, name=None):
    strings = [[((i, 'primary') if type(i) == str else i)
                for i in ([string] if type(string) == str else string)]
               for string in strings]
    print(*strings, sep="\n")
    button = {
        "one_time": True,
        "buttons": [
            [create_button(*button) for button in string]
            for string in strings
        ]}
    button = json.dumps(button, ensure_ascii=False).encode('utf-8')
    if not name:
        return str(button.decode('utf-8'))
    buttons[str(name)] = button


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
'''
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
'''
buttonsItemsChoice = create_all_button("Информатика", 'Математика', 'Физика')
#buttonsItemsChoice = buttons["create_all_button"]
'''
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
'''
buttonsDivChoice = create_all_button(["Div 1", "Div 2", "Div 3"], [('К предметам', 'secondary')])
'''
# кнопка возрата
buttonReturn = {
    "one_time": True,
    "buttons": [
        [create_button('бросить вызов', 'primary')],
        [create_button('Остановить поиск', 'secondary')]

    ]}
buttonReturn = json.dumps(buttonReturn, ensure_ascii=False).encode('utf-8')
buttonReturn = str(buttonReturn.decode('utf-8'))
'''
buttonReturn = create_all_button('бросить вызов', [('К предметам', 'secondary')])
'''
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
'''
buttonsChoice = create_all_button([('Нет', 'negative'), ('Да', 'positive')])

'''
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
'''
buttonsAgree = create_all_button([('Отбой', 'negative'), ('Согласен', 'positive')])

'''
buttonAfterBadСall = {
    "one_time": True,
    "buttons": [
        [create_button('бросить вызов', 'primary')],
        [create_button('возобновить поиск', 'primary')],
        [create_button('к предметам', 'secondary')]

    ]}
buttonAfterBadСall = json.dumps(buttonAfterBadСall, ensure_ascii=False).encode('utf-8')
buttonAfterBadСall = str(buttonAfterBadСall.decode('utf-8'))
'''

buttonAfterBadСall = create_all_button(['бросить вызов'], ['возобновить поиск'], [('к предметам', 'secondary')])