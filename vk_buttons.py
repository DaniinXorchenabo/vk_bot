from lib import *
from structs import *


def create_all_button(*strings, name=None):
    print(")(((((()()()( --- ", strings)
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

buttonsItemsChoice = create_all_button("Информатика", 'Математика', 'Физика')
buttonsDivChoice = create_all_button(["Div 1", "Div 2", "Div 3"], [('К предметам', 'secondary')])
buttonReturn = create_all_button('бросить вызов', [('К предметам', 'secondary')])
buttonsChoice = create_all_button([('Нет', 'negative'), ('Да', 'positive')])
buttonsAgree = create_all_button([('Отбой', 'negative'), ('Согласен', 'positive')])
buttonAfterBadСall = create_all_button(['бросить вызов'], ['возобновить поиск'], [('к предметам', 'secondary')])