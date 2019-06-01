import json
import logging


import uuid


from contacts.utils import makeResponse
from contacts.utils import get_attribute
from contacts.storage import get_storage

logger = logging.getLogger()


def post_contact(event, context):
    storage = get_storage()
    try:
        user_id = event['requestContext']['authorizer']['claims']['sub']
        payload = json.loads(event['body'])
        id = get_attribute(payload, 'id', None)
        if id is None:
            id = str(uuid.uuid4())
            storage.save_contact(user_id, id, payload)
            return makeResponse(201, {'id': id})
        else:
            storage.modify_contact(user_id, payload)
            return makeResponse(204)

    except Exception as e:
        return makeResponse(500, {'message': str(e)})


def get_contacts(event, context):
    storage = get_storage()
    try:
        user_id = event['requestContext']['authorizer']['claims']['sub']
        result = storage.list_contacts(user_id)
        return makeResponse(200, result)
    except Exception as e:
        return makeResponse(500, {'message': str(e)})


def delete_contact(event, context):
    storage = get_storage()
    try:
        user_id = event['requestContext']['authorizer']['claims']['sub']
        contact_id = event['pathParameters']['id']
        success = storage.remove_contact(user_id, contact_id)

        status = 204 if success is True else 404
        return makeResponse(status)
    except Exception as e:
        return makeResponse(500, {'message': str(e)})
