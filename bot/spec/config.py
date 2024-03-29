from abc import ABC
from typing import Final


class Config(ABC):
    CMD_PREFIX: Final = '.'
    ID_GUILD: Final = 1101622403693547630
    STANDARD_EXTENSIONS: Final = ['owner.loader', 'owner.command', 'owner.presence']
