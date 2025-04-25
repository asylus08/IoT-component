from enum import Enum, auto

class ActionType(Enum):
    OPEN_DOOR = "OPEN_DOOR"
    CLOSE_DOOR = "CLOSE_DOOR"
    ACTIVATE_ALARM = "ACTIVATE_ALARM"
    DEACTIVATE_ALARM = "DEACTIVATE_ALARM"
    RISE_TEMP = "RISE_TEMP"
    LOWER_TEMP = "LOWER_TEMP"

    @classmethod
    def convert_str_action_to_enum(cls, action: str):
        try:
            return cls[action.upper()]
        except KeyError:
            return False