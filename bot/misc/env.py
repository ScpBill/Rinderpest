# == Getting the secret information ==
import os
from abc import ABC
from typing import Final
from dotenv import load_dotenv


load_dotenv('./.env')


class Env(ABC):
    TOKEN: Final = os.environ.get('TEST_TOKEN', '0_0')
