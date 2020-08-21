import pytest
import os
from contextlib import closing
from psycopg2.extras import NamedTupleCursor
try:
    from mock import patch
except ImportError:
    from unittest.mock import patch

from fixtures import provision_database  # noqa: F401
from utils import make_mock_message, getConnection
import contacts.handler as handler
from contacts.messaging import Sqs

from contacts.utils import IncomingOperations, OutgoingOperations, BorrowingStatus


@pytest.mark.usefixtures('provision_database')
class TestLendings(object):
    @patch.object(Sqs, "send_message")
    def test_handle_successful_borrower_validation(self, mock_send_message):
        mock_message = make_mock_message({
            'operation': IncomingOperations.VALIDATE_BOOK_BORROWER.value,
            'userId': 'user5',
            'contactId': '1005',
            'lendingId': '1',
            'bookId': '2000'
        }, 'mock-reply-address')
        handler.handle_messages(event=mock_message, context=None)

        # Assert the send_message method is called once, with correct parameters
        mock_send_message.assert_called_once_with({
            'operation': OutgoingOperations.VALIDATE_BOOK_BORROWER.value,
            'userId': 'user5',
            'lendingId': '1',
            'bookId': '2000',
            'result': {
                'status': BorrowingStatus.BORROWER_VALIDATED.value,
                'contact': 'contact-1005'
            }
        }, 'mock-reply-address')

        # Assert the borrowing is saved accodingly in database
        schema = os.environ['PGSCHEMA']
        connection = getConnection()
        with closing(connection):
            with closing(connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:
                cursor.execute(
                    f'SELECT * FROM "{schema}"."borrowing" WHERE user_id=%s AND lending_id=%s AND contact_id=%s AND book_id=%s', ('user5', '1', '1005', '2000'))
                assert cursor.rowcount == 1

    @patch.object(Sqs, "send_message")
    def test_handle_failed_borrower_validation(self, mock_send_message):

        # user does not exists
        mock_message = make_mock_message({
            'operation': IncomingOperations.VALIDATE_BOOK_BORROWER.value,
            'userId': 'no-user',
            'contactId': '1005',
            'lendingId': '1',
            'bookId': '2000'
        }, 'mock-reply-address')
        handler.handle_messages(event=mock_message, context=None)

        # Assert the send_message method is called once, with correct parameters
        mock_send_message.assert_called_once_with({
            'operation': OutgoingOperations.VALIDATE_BOOK_BORROWER.value,
            'userId': 'no-user',
            'lendingId': '1',
            'bookId': '2000',
            'result': {
                'status': BorrowingStatus.BORROWER_NOT_VALIDATED.value,
                'contact': None
            }
        }, 'mock-reply-address')

        # Assert the borrowing is NOT saved accodingly in database
        schema = os.environ['PGSCHEMA']
        connection = getConnection()
        with closing(connection):
            with closing(connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:
                cursor.execute(
                    f'SELECT * FROM "{schema}"."borrowing" WHERE user_id=%s AND lending_id=%s AND contact_id=%s AND book_id=%s', ('no-user', '1', '1005', '2000'))
                assert cursor.rowcount == 0

    def test_handle_returned_book(self):
        # user does not exists
        mock_message = make_mock_message({
            'operation': IncomingOperations.RETURN_LENT_BOOK.value,
            'userId': 'user6',
            'contactId': '1006',
            'lendingId': '2',
            'bookId': 'book-id-2'
        })
        handler.handle_messages(event=mock_message, context=None)
        schema = os.environ['PGSCHEMA']
        connection = getConnection()
        with closing(connection):
            with closing(connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:
                cursor.execute(
                    f'SELECT * FROM "{schema}"."borrowing" WHERE user_id=%s AND lending_id=%s AND contact_id=%s AND book_id=%s', ('user6', '2', '1006', 'book-id-2'))
                assert cursor.rowcount == 0
