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
    def test_delete_contacts(self):

        userId = 'user3'
        id = '1003'
        mock_event = make_mock_event(userId, None, {'id': id})
        response = handler.delete_contact(mock_event, None)
        status_code = response['statusCode']
        assert status_code == 204

        body = json.loads(response['body'])
        assert body is None

        schema = os.environ['PGSCHEMA']
        connection = getConnection()
        with closing(connection):
            with closing(connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:
                cursor.execute(
                    f'SELECT * FROM "{schema}"."contact" WHERE id=%s', (id,))
                assert cursor.rowcount == 0

    def test_delete_contacts_with_incorrect_id(self):

        userId = 'user3'
        id = '9999'
        mock_event = make_mock_event(userId, None, {'id': id})
        response = handler.delete_contact(mock_event, None)
        status_code = response['statusCode']
        assert status_code == 404
