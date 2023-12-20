import os
from typing import Final
from dotenv import load_dotenv


def env_load():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)


class TgKeys:
    TOKEN: Final = os.getenv('TOKEN', 'define me!')
    DB_NAME: Final = os.getenv('DB_NAME', 'define me!')
