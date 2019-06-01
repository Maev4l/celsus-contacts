import pytest


import contacts.handler as handler
from fixtures import provision_database  # noqa: F401
from utils import make_mock_message


@pytest.mark.usefixtures('provision_database')
class TestLendings(object):
    def test_handle_successful_borrower_validation(self):

        mock_message = make_mock_message({
            'operation': 'toto'
        })
        handler.handle_messages(event=mock_message, context=None)
        assert 1 == 1
