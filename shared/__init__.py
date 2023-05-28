import os

from shared.connectors import QnAConnector
from shared.bots.base import BaseBot

import dotenv
dotenv.load_dotenv() # TODO: this is temporary, they will be in keyvault

qna_connector = QnAConnector(
    endpoint = os.getenv('QNA_ENDPOINT'),
    credential = os.getenv('QNA_CREDENTIAL'),
    project_name = os.getenv('QNA_PROJECT'),
    deployment_name = os.getenv('QNA_DEPLOYMENT'),
)

BOT = BaseBot(qna_connector=qna_connector)

try:
    from shared.customizations import *  # noqa
except ImportError:
    pass