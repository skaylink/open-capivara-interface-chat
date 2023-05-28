from typing import Tuple
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient
from azure.ai.language.questionanswering import models as qna

class QnAConnector():
    default_answer: str = "Sorry, I don't know the answer to that question."
    def __init__(self, endpoint: str, credential: str, project_name: str, deployment_name: str):
        self.client = QuestionAnsweringClient(
            endpoint = endpoint,
            credential = AzureKeyCredential(credential),
        )
        self.project_name = project_name
        self.deployment_name = deployment_name

    async def get_answers(self, question: str, confidence_threshold: float = 0.9) -> Tuple[bool, str]:
        output = self.client.get_answers(
            question = question,
            project_name = self.project_name,
            deployment_name = self.deployment_name
        )
        if (len(output.answers) == 0) or (output.answers[0].confidence < confidence_threshold):
            return False, ""
        return True, output.answers[0].answer
