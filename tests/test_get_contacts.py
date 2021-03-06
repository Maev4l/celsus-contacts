import json

import pytest

import contacts.handler as handler
from fixtures import provision_database  # noqa: F401
from utils import make_mock_event


@pytest.mark.usefixtures('provision_database')
class TestGetContacts(object):
    def test_get_contacts(self):

        userId = 'user2'
        mock_event = make_mock_event(userId, None)
        response = handler.get_contacts(mock_event, None)

        contacts = response['contacts']
        assert contacts is not None
        assert len(contacts) == 2

        contact = contacts[0]
        assert contact['id'] == '1002'
        assert contact['nickname'] == 'contact-a-2'
        assert contact['thumbnail'] == 'thumbnail-2'

        contact = contacts[1]
        assert contact['id'] == '1001'
        assert contact['nickname'] == 'contact-z-1'
        assert contact['thumbnail'] == 'thumbnail-1'

    def test_get_existing_contact(self):
        userId = 'user2'
        mock_event = make_mock_event(userId, {'id': '1001'})
        contact = handler.get_contact(mock_event, None)

        assert contact is not None
        assert contact['id'] == '1001'
        assert contact['nickname'] == 'contact-z-1'
        assert contact['thumbnail'] == 'thumbnail-1'

    def test_get_unknown_contact(self):
        userId = 'user2'
        mock_event = make_mock_event(userId, {'id': '9999'})
        contact = handler.get_contact(mock_event, None)

        assert contact is None
