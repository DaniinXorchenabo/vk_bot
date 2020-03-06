from lib import *


# структура для хранения информации о текущих битвах(так удобнее)
@dataclass  # ничего подобного, оно должно реализовываться по-другому
class Battle:
    id1: int
    id2: int
    sub: int
    div: int
    questions: list
    answers: list
    point1: int = 0
    point2: int = 0
    counter1: int = 0
    counter2: int = 0


# Словарь состояний
statusID = {}

# Массив очереди
search = [[-1] * 3 for _ in range(3)]

# Массив боёв
battles = []
