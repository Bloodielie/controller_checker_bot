from app.utils.config import Config

config = Config(".env")

DB_URL = config("DB_URL", cast=str)
VK_API_TOKEN = config("VK_API_TOKEN", cast=str)
TELEGRAM_API_TOKEN = config("TELEGRAM_API_TOKEN", cast=str)
BREST_GROUP_ID = config("BREST_GROUP_ID", cast=int)
storage_dsn = config("storage_dsn", cast=str)

TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {"models": ["app.models.user", "app.models.bus_stop", "app.models.settings"], "default_connection": "default",},
    },
}

# img
PATH_TO_BASE_IMG = config("PATH_TO_BASE_IMG", cast=str, default="./images/base.jpg")
PATH_TO_BASE_FONT = config("PATH_TO_BASE_FONT", cast=str, default="./images/font/comfortaa.ttf")
PATH_TO_IMAGES = config("PATH_TO_IMAGES", cast=str, default="./images")
x_time_cordinate = config("x_time_cordinate", cast=int, default=20)
x_message_cordinate = config("x_message_cordinate", cast=int, default=380)
y_cordinate = config("y_cordinate", cast=int, default=142)
y_step = config("y_step", cast=int, default=92)
