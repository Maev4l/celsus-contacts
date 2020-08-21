import json
from enum import Enum


def makeResponse(statusCode, body=None):
    return {
        'statusCode': statusCode,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': 'true',
        },
        'body': json.dumps(body)
    }


def get_attribute(data, attribute, default_value):
    return data.get(attribute) or default_value


class IncomingOperations(Enum):
    VALIDATE_BOOK_BORROWER = 'VALIDATE_BOOK_BORROWER'
    RETURN_LENT_BOOK = 'RETURN_LENT_BOOK'


class OutgoingOperations(Enum):
    VALIDATE_BOOK_BORROWER = 'VALIDATE_BOOK_BORROWER'


class BorrowingStatus(Enum):
    BORROWER_VALIDATED = 'BORROWER_VALIDATED'
    BORROWER_NOT_VALIDATED = 'BORROWER_NOT_VALIDATED'
