import enum
from enum import Enum, auto

class Status(Enum):
    NONE = auto(),
    SAFE = auto(),
    ALERT = auto()