from contacts.storage import get_storage
from contacts.utils import get_attribute
from contacts.utils import makeResponse
import uuid
import json
import logging

from contacts.dispatcher import Dispatcher

logger = logging.getLogger()


def post_contact(event, context):
    user_id = event['userId']
    payload = event['payload']
    contact = payload['contact']
    id = get_attribute(contact, 'id', None)
    with get_storage() as storage:
        if id is None:
            id = str(uuid.uuid4())
            storage.save_contact(user_id, id, contact)
            return {'id': id}
        else:
            storage.modify_contact(user_id, contact)
            return True


def get_contacts(event, context):
    user_id = event['userId']
    with get_storage() as storage:
        result = storage.list_contacts(user_id)
        return result


def get_contact(event, context):
    user_id = event['userId']
    payload = event['payload']
    contact_id = payload['id']
    with get_storage() as storage:
        contact = storage.get_contact(user_id, contact_id)
        return contact


def delete_contact(event, context):
    user_id = event['userId']
    payload = event['payload']
    contact_id = payload['id']

    with get_storage() as storage:
        contact = storage.get_contact(user_id, contact_id)
        if contact is None:
            return False
        else:
            success = storage.remove_contact(user_id, contact_id)
            return success


def handle_messages(event, context):

    record = event['Records'][0]
    reply_address = None
    if 'replyAddress' in record['messageAttributes']:
        reply_address = record['messageAttributes']['replyAddress']['stringValue']

    payload = json.loads(record['body'])

    operation = payload['operation']

    dispatcher = Dispatcher()
    dispatcher.dispatch(operation, payload, reply_address)
