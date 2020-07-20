from tortoise import fields, models

from app.models.user import Users
from app.models.settings import City


class BusStop(models.Model):
    id = fields.IntField(pk=True)
    message_text = fields.TextField()
    city = fields.CharEnumField(City, default=City.brest)
    created = fields.DatetimeField(auto_now_add=True)
    creator: fields.ForeignKeyRelation[Users] = fields.ForeignKeyField("models.Users", on_delete=fields.CASCADE)
