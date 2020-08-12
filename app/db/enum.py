from enum import Enum


class Representation(str, Enum):
    text = "TEXT"
    photo = "PHOTO"


class City(str, Enum):
    brest = "BREST"
