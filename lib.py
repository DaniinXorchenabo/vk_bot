from dataclasses import dataclass, field
import time
from random import shuffle, random, randint
import json

import vk_api

from config import cfg

debagFlag = [True]