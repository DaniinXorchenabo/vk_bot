from dataclasses import dataclass, field
import time
from random import shuffle, random, randint
import json

import vk_api

#from config import cfg

debagFlag = [True]

token = "91ee129261aa99a1657f987a1fa868d922352e89fe4fc21921c578e17f689e2c92bc8f1870faa9688b82b"
vk = vk_api.VkApi(token=token)