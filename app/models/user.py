from tortoise import models, fields

from app.models.settings import Settings


class Users(models.Model):
    id = fields.IntField(pk=True)
    telegram_id = fields.IntField(max_length=50, unique=True)
    username = fields.CharField(max_length=100, null=True)
    time_of_last_receipt = fields.DatetimeField(null=True)
    settings: fields.ForeignKeyRelation[Settings] = fields.ForeignKeyField("models.Settings", on_delete=fields.CASCADE)
