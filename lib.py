from dataclasses import dataclass, field
import time
from random import shuffle, random, randint
import json

import vk_api

#from config import cfg

debagFlag = [True]

token = "token"
vk = vk_api.VkApi(token=token, app_id=2685278)

print(type(None))

forbidden_list = []

last_messenges = dict()  # последнее сообщение, которое отправил бот key: int (ID) value: str (messenge)