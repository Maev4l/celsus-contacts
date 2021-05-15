from abc import ABC, abstractmethod
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import json
import logging
import os


logger = logging.getLogger()


class Messaging(ABC):
    @abstractmethod
    def send_message(self, message, destination):
        pass


class Sqs(Messaging):
    def __init__(self):
        config = Config(region_name = os.getenv('REGION'))
        self._client = boto3.client('sqs', config=config)

    def send_message(self, message, destination):
        data = json.dumps(message)
        try:
            response = self._client.send_message(
                QueueUrl=destination, MessageBody=data)
            logger.info(f'Message sent: {response["MessageId"]}')
        except ClientError as e:
            logger.error(f'Failed to send message to {url}: {e}')


def get_messaging():
    return Sqs()
