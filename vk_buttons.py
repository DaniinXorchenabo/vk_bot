from lib import *



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