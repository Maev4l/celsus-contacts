import json
import logging
import os
from contextlib import closing
import uuid
import psycopg2
from psycopg2.extras import execute_values, NamedTupleCursor
from contacts.utils import makeResponse
from contacts.utils import get_attribute

logger = logging.getLogger()


def getConnection():
    hostname = os.environ['PGHOST']
    port = os.environ['PGPORT']
    database = os.environ['PGDATABASE']
    user = os.environ['PGUSER']
    password = os.environ['PGPASSWORD']

    connection = psycopg2.connect(
        host=f'{hostname}',
        port=f'{port}',
        database=f'{database}',
        user=f'{user}',
        password=f'{password}'
    )

    logger.debug(f'Connected successfully to database {database}')
    return connection


def post_contact(event, context):
    try:
        with closing(getConnection()) as connection:
            with closing(connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:

                user_id = event['requestContext']['authorizer']['claims']['sub']
                payload = json.loads(event['body'])
                schema = os.environ['PGSCHEMA']
                nickname = get_attribute(payload, 'nickname', '')
                thumbnail = get_attribute(payload, 'thumbnail', None)
                id = get_attribute(payload, 'id', None)
                if id is None:
                    id = str(uuid.uuid4())
                    cursor.execute(
                        f'INSERT INTO "{schema}"."contact"(id, user_id, nickname, thumbnail) '
                        "VALUES ( %s, %s, %s, %s); ",
                        (id, user_id, nickname, thumbnail))
                    connection.commit()
                    return makeResponse(201, {'id': id})
                else:
                    cursor.execute(
                        f'UPDATE "{schema}"."contact" '
                        'SET "nickname"=%s, "thumbnail"=%s WHERE "id" = %s AND "user_id"=%s ;',
                        (nickname, thumbnail, id, user_id))
                    connection.commit()
                    return makeResponse(204)

    except psycopg2.Error as e:
        logger.error(f"post contact error: {e}")
        return makeResponse(500, {'message': str(e)})
