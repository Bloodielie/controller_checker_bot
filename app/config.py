from app.utils.config import Config

config = Config(".env")

DB_URL = config("DB_URL", cast=str, default="postgres://postgres:1234@localhost/controllercheckerbot",)
VK_API_TOKEN = config("VK_API_TOKEN", cast=str)
TELEGRAM_API_TOKEN = config("TELEGRAM_API_TOKEN", cast=str)
BREST_GROUP_ID = config("BREST_GROUP_ID", cast=int)

TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {"models": ["app.models.user", "app.models.bus_stop", "app.models.settings"], "default_connection": "default",},
    },
}
