from app.utils.config import Config
from dotenv import load_dotenv
load_dotenv()

config = Config(".env")

DB_URL = config("DB_URL", cast=str)
VK_API_TOKEN = config("VK_API_TOKEN", cast=str)
TELEGRAM_API_TOKEN = config("TELEGRAM_API_TOKEN", cast=str)
BREST_GROUP_ID = config("BREST_GROUP_ID", cast=int)
# storage_dsn = config("storage_dsn", cast=str)

# img
PATH_TO_BASE_IMG = config("PATH_TO_BASE_IMG", cast=str, default="./images/base.jpg")
PATH_TO_BASE_FONT = config("PATH_TO_BASE_FONT", cast=str, default="./images/font/comfortaa.ttf")
PATH_TO_IMAGES = config("PATH_TO_IMAGES", cast=str, default="./images")
x_time_cordinate = config("x_time_cordinate", cast=int, default=20)
x_message_cordinate = config("x_message_cordinate", cast=int, default=380)
y_cordinate = config("y_cordinate", cast=int, default=142)
y_step = config("y_step", cast=int, default=92)
