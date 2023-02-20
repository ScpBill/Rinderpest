# == PyCharm version ==
import os
from abc import ABC
from typing import Final


class Env(ABC):
    TOKEN: Final = os.environ.get('TOKEN', 'define me!')


# == PythonAnywhere ==
# ...
# from dotenv import load_dotenv
#
#
# load_dotenv('.env')
#
#
# class Env(ABC):
#     TOKEN: Final = os.getenv('TOKEN')
