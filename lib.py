from dataclasses import dataclass, field
import time
from random import shuffle, random, randint
import json

import vk_api

#from config import cfg

debagFlag = [True]

token = "ac7b695bc7d4e43747629c8918a08aada6954976ccfe5e9db4c9756675b7c9230a6ef46e481258629730b"
vk = vk_api.VkApi(token=token)

print(type(None))