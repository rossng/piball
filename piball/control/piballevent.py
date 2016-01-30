from enum import Enum


class PiballEvent(Enum):
    left_flipper_button_on = 1
    left_flipper_button_off = 2
    right_flipper_button_on = 3
    right_flipper_button_off = 4