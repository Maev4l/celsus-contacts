import json
import os
import pytest
from contextlib import closing
from psycopg2.extras import NamedTupleCursor

import contacts.handler as handler
from fixtures import provision_database  # noqa: F401
from utils import make_mock_event, getConnection


@pytest.mark.usefixtures('provision_database')
class TestPostContacts(object):
    def test_create_new_contact(self):
        nickname = 'contact-name-1'
        thumbnail = 'xxx'
        payload = {
            'contact': {
                'nickname': nickname,
                'thumbnail': thumbnail
            }
        }

        userId = 'user1'
        mock_event = make_mock_event(userId, payload)
        contact = handler.post_contact(mock_event, None)

        id = contact['id']
        assert id is not None

        schema = os.environ['PGSCHEMA']
        connection = getConnection()
        with closing(connection):
            with closing(connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:
                cursor.execute(
                    f'SELECT * FROM "{schema}"."contact" WHERE id=%s', (id,))
                assert cursor.rowcount == 1
                for record in cursor:
                    assert record.id == id
                    assert record.nickname == nickname
                    assert record.thumbnail == thumbnail
                    assert record.user_id == userId

    def test_update_contact(self):
        nickname = 'contact-name-1-bis'
        thumbnail = 'xxx-bis'
        id = '1000'
        payload = {
            'contact': {
                'id': id,
                'nickname': nickname,
                'thumbnail': thumbnail
            }
        }

        userId = 'user1'
        mock_event = make_mock_event(userId, payload)
        result = handler.post_contact(mock_event, None)

        assert result is True

        schema = os.environ['PGSCHEMA']
        connection = getConnection()
        with closing(connection):
            with closing(connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:
                cursor.execute(
                    f'SELECT * FROM "{schema}"."contact" WHERE id=%s', (id,))
                assert cursor.rowcount == 1
                for record in cursor:
                    assert record.id == id
                    assert record.nickname == nickname
                    assert record.thumbnail == thumbnail
                    assert record.user_id == userId
