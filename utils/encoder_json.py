# subclass JSONEncoder
from json import JSONEncoder

from utils.json_utils import json_default


class Encoder(JSONEncoder):
    def default(self, o):
        return json_default(o)
