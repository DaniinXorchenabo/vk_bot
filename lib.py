from dataclasses import dataclass, field
import time
from random import shuffle, random, randint
import json
from itertools import chain
from typing import Any
import vk_api

#from config import cfg

debagFlag = [True]




try:
    with open("conf.txt", "r") as f:
        token = f.read().strip()
except Exception:
    with open("conf.txt", "w") as f:
        f.write("тут_должен_быть_токен_но_его_тут_нет_Для_работы_бота_вставьте_сюда_ваш_токен")
        raise FileNotFoundError('введите токен от бота в файл /conf.txt')

vk = vk_api.VkApi(token=token, app_id=2685278)

