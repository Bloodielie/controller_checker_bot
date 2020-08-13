from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, DateTime, Text
from datetime import datetime

from app.db.enum import City, Representation

metadata = MetaData()
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("telegram_id", Integer),
    Column("username", String(100), nullable=True),
    Column("time_of_last_receipt", DateTime, nullable=True),
    Column("settings_id", ForeignKey("settings.id")),
)

settings = Table(
    "settings",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("number_of_posts", Integer, default=15),
    Column("city", String(20), default=City.brest.value),
    Column("representation", String(40), default=Representation.text.value),
)

bus_stop = Table(
    "busstop",
    metadata,
    Column("id", Integer, primary_key=True, unique=True),
    Column("message_text", Text),
    Column("city", String(20), default=City.brest.value),
    Column("created", DateTime, default=datetime.now()),
    Column("creator_id", ForeignKey("users.id")),
)
