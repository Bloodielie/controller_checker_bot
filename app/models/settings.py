from enum import Enum

from tortoise import models, fields


class Representation(str, Enum):
    text = "TEXT"
    photo = "PHOTO"


class City(str, Enum):
    brest = "BREST"


class Settings(models.Model):
    id = fields.IntField(pk=True)
    representation = fields.CharEnumField(Representation, default=Representation.text)
    city = fields.CharEnumField(City, default=City.brest)
    number_of_posts = fields.IntField(default=15)
