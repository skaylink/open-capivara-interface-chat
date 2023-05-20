from shared.bots.base import BaseBot

BOT = BaseBot()

try:
    from shared.customizations import *  # noqa
except ImportError:
    pass