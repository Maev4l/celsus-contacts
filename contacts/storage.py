from abc import ABC, abstractmethod

import psycopg2
from contextlib import closing
from psycopg2.extras import NamedTupleCursor
import os
import logging


from contacts.utils import get_attribute

logger = logging.getLogger()

'''
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
'''


class Storage(ABC):

    @abstractmethod
    def remove_contact(self, user_id, contact_id):
        pass

    @abstractmethod
    def list_contacts(self, user_id):
        pass

    @abstractmethod
    def save_contact(self, user_id, id, contact):
        pass

    @abstractmethod
    def modify_contact(self, user_id, contact):
        pass


class DatabaseStorage(Storage):
    def __init__(self):
        hostname = os.environ['PGHOST']
        port = os.environ['PGPORT']
        database = os.environ['PGDATABASE']
        user = os.environ['PGUSER']
        password = os.environ['PGPASSWORD']

        self.connection = psycopg2.connect(
            host=f'{hostname}',
            port=f'{port}',
            database=f'{database}',
            user=f'{user}',
            password=f'{password}'
        )

        logger.debug(f'Connected successfully to database {database}')

    def remove_contact(self, user_id, contact_id):
        try:
            with closing(self.connection) as connection:
                with closing(connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:
                    schema = os.environ['PGSCHEMA']

                    cursor.execute(
                        f'DELETE FROM "{schema}"."contact"'
                        'WHERE "user_id"=%s AND "id"=%s AND '
                        f'NOT EXISTS (SELECT 1 FROM "{schema}"."borrowing" WHERE'
                        '"user_id"=%s AND "contact_id"=%s)',
                        [user_id, contact_id, user_id, contact_id])
                    connection.commit()
                    return cursor.rowcount >= 1
        except psycopg2.Error as e:
            logger.error(f"delete contact error: {e}")
            raise e

    def list_contacts(self, user_id):
        try:
            with closing(self.connection) as connection:
                with closing(connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:

                    schema = os.environ['PGSCHEMA']

                    cursor.execute(
                        f'SELECT "id", "nickname", "thumbnail" FROM "{schema}"."contact"'
                        'WHERE "user_id"=%s ORDER BY "nickname"',
                        [user_id])

                    result = {
                        'contacts': []
                    }
                    for record in cursor:
                        result['contacts'].append({
                            'id': record.id,
                            'nickname': record.nickname,
                            'thumbnail': record.thumbnail
                        })

                    return result
        except psycopg2.Error as e:
            logger.error(f"get contacts error: {e}")
            raise e

    def save_contact(self, user_id, id, contact):
        try:
            with closing(self.connection) as connection:
                with closing(connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:
                    schema = os.environ['PGSCHEMA']
                    nickname = get_attribute(contact, 'nickname', '')
                    thumbnail = get_attribute(contact, 'thumbnail', None)
                    cursor.execute(
                        f'INSERT INTO "{schema}"."contact"(id, user_id, nickname, thumbnail) '
                        "VALUES ( %s, %s, %s, %s); ",
                        (id, user_id, nickname, thumbnail))
                    connection.commit()
        except psycopg2.Error as e:
            logger.error(f"get contacts error: {e}")
            raise e

    def modify_contact(self, user_id, contact):
        try:
            with closing(self.connection) as connection:
                with closing(connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:
                    schema = os.environ['PGSCHEMA']
                    id = contact['id']
                    nickname = get_attribute(contact, 'nickname', '')
                    thumbnail = get_attribute(contact, 'thumbnail', None)
                    cursor.execute(
                        f'UPDATE "{schema}"."contact" '
                        'SET "nickname"=%s, "thumbnail"=%s WHERE "id" = %s AND "user_id"=%s ;',
                        (nickname, thumbnail, id, user_id))
                    connection.commit()
        except psycopg2.Error as e:
            logger.error(f"get contacts error: {e}")
            raise e

    def get_contact(self, user_id, contact_id):
        try:
            with closing(self.connection) as connection:
                with closing(connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:
                    schema = os.environ['PGSCHEMA']
                    cursor.execute(f'SELECT "id" from "{schema}"."contact"'
                                   'WHERE "id"= %s AND "user_id"= %s', (contact_id, user_id))
                    record = cursor.fetchone()
        except psycopg2.Error as e:
            logger.error(f"get contacts error: {e}")
            raise e


def get_storage():
    return DatabaseStorage()
