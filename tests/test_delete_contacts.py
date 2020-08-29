import json
import os
import pytest
from contextlib import closing
from psycopg2.extras import NamedTupleCursor

import contacts.handler as handler
from fixtures import provision_database  # noqa: F401
from utils import make_mock_event, getConnection


@pytest.mark.usefixtures('provision_database')
class TestDeleteContacts(object):
    def test_delete_contact(self):

        userId = 'user3'
        id = '1003'
        mock_event = make_mock_event(userId, {'id': id})
        result = handler.delete_contact(mock_event, None)

        assert result is True

        schema = os.environ['PGSCHEMA']
        connection = getConnection()
        with closing(connection):
            with closing(connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:
                cursor.execute(
                    f'SELECT * FROM "{schema}"."contact" WHERE id=%s', (id,))
                assert cursor.rowcount == 0

    def test_delete_contact_with_incorrect_id(self):
        userId = 'user3'
        id = '9999'
        mock_event = make_mock_event(userId, {'id': id})
        result = handler.delete_contact(mock_event, None)
        assert result is False

    def test_delete_contact_with_borrowed_book(self):
        userId = 'user4'
        id = '1004'
        mock_event = make_mock_event(userId, {'id': id})
        result = handler.delete_contact(mock_event, None)
        assert result is False
