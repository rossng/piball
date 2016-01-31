from enum import Enum


class PiballEvent(Enum):
    left_flipper_button_on = 1
    left_flipper_button_off = 2
    right_flipper_button_on = 3
    right_flipper_button_off = 4
    fail_on = 5
    fail_off = 6
    bumper_1_on = 7
    bumper_1_off = 8
    bumper_2_on = 9
    bumper_2_off = 10
    bumper_3_on = 11
    bumper_3_off = 12
    plunger_button_on = 13
    plunger_button_off = 14