from lib import *
from funcs import *

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
