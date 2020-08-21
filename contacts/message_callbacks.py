

from contacts.storage import get_storage
from contacts.messaging import get_messaging
from contacts.utils import OutgoingOperations, BorrowingStatus
import logging

logger = logging.getLogger()


def return_book(user_id, contact_id, lending_id, book_id):
    with get_storage() as storage:
        storage.remove_borrowing(user_id, contact_id, book_id, lending_id)
        logger.info(f'Book {book_id} returned by {contact_id}')


def validate_borrower(user_id, contact_id, lending_id, book_id, reply_address):
    # Ensure contact exists and belongs to the current user
    with get_storage() as storage:
        # Save borrowing firts in order to avoid race condition, if the contact
        # is deleted between existence check and borrowing save
        storage.save_borrowing(user_id, contact_id, book_id, lending_id)
        contact = storage.get_contact(user_id, contact_id)
        if contact is None:
            # if contact does not exists, remove borrowing
            # and reply with cancellation
            storage.remove_borrowing(user_id, contact_id, book_id, lending_id)

        logger.info(f'Reply borrower validation - lending: {lending_id}')
        result = {
            'status': BorrowingStatus.BORROWER_NOT_VALIDATED.value if contact is None else BorrowingStatus.BORROWER_VALIDATED.value,
            'contact': None if contact is None else contact['nickname']
        }
        # Reply with confirmation
        get_messaging().send_message({
            'operation': OutgoingOperations.VALIDATE_BOOK_BORROWER.value,
            'userId': user_id,
            'lendingId': lending_id,
            'bookId': book_id,
            'result': result
        }, reply_address)
