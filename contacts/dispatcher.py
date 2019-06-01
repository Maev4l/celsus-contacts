from contacts.message_callbacks import validate_borrower
from contacts.utils import IncomingOperations


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Dispatcher(metaclass=Singleton):

    def __init__(self):
        self._handlers = {
            IncomingOperations.VALIDATE_BOOK_BORROWER.value: validate_borrower
        }

    def dispatch(self, operation, payload, reply_address):
        handler = self._handlers.get(operation)
        handler(payload, reply_address)
