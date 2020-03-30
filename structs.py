from lib import *


# структура для хранения информации о текущих битвах(так удобнее)
@dataclass  # ничего подобного, оно должно реализовываться по-другому
class Battle:
    sub: int
    div: int
    questions: list
    answers: list
    people: list  # type: list[Participant]

@dataclass
class Participant:
    id: int
    point: int = 0
    counter: int = 0

# Словарь состояний
statusID = {}

# Массив очереди
search = [[-1] * 3 for _ in range(3)]

# Массив боёв
battles = []

#массив вызовов на бой
calls = []
calls_dict = dict()

# переменная для подсчета кол-во боев(зачем она?)
countOfBattles = 0

subgects_key = {1: "inf", 2: "mat", 3: "phys"}
DIVISIONS = ["Div 1", "Div 2", "Div 3"]

forbidden_list = []

last_messenges = dict()  # последнее сообщение, которое отправил бот key: int (ID) value: str (messenge)

buttons = dict()