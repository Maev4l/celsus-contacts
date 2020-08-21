from contacts.message_callbacks import validate_borrower, return_book
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
            IncomingOperations.VALIDATE_BOOK_BORROWER.value: self.dispatch_validate_book_borrower,
            IncomingOperations.RETURN_LENT_BOOK.value: self.dispatch_return_book
        }

    def dispatch_validate_book_borrower(self, payload, reply_address):
        user_id = payload['userId']
        contact_id = payload['contactId']
        lending_id = payload['lendingId']
        book_id = payload['bookId']
        validate_borrower(user_id, contact_id,
                          lending_id, book_id, reply_address)

    def dispatch_return_book(self, payload, reply_address=None):
        user_id = payload['userId']
        contact_id = payload['contactId']
        lending_id = payload['lendingId']
        book_id = payload['bookId']
        return_book(user_id, contact_id, lending_id, book_id)

    def dispatch(self, operation, payload, reply_address):
        handler = self._handlers.get(operation)
        handler(payload, reply_address)
