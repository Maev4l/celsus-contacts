from contacts.callbacks import validate_borrower


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Dispatcher(metaclass=Singleton):

    def __init__(self):
        self._handlers = dict()

    def dispatch(self, operation, payload, reply_address):
        callback = self._handlers.get(operation)
        callback(payload, reply_address)
