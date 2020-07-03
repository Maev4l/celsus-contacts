from contacts.utils import get_attribute
from abc import ABC, abstractmethod

import psycopg2
from contextlib import closing
from psycopg2.extras import NamedTupleCursor
import os
import logging


logger = logging.getLogger()


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


#    @abstractmethod
#    def get_borrowings(self, user_id, contact):
#        pass
#

    @abstractmethod
    def save_borrowing(self, user_id, contact_id, book_id, lending_id):
        pass

    @abstractmethod
    def remove_borrowing(self, user_id, contact_id, book_id, lending_id):
        pass


class DatabaseStorage(Storage):
    def __init__(self):
        self._hostname = os.environ['PGHOST']
        self._port = os.environ['PGPORT']
        self._database = os.environ['PGDATABASE']
        self._user = os.environ['PGUSER']
        self._password = os.environ['PGPASSWORD']
        self._connection = None

    def __enter__(self):
        self._connection = psycopg2.connect(
            host=f'{self._hostname}',
            port=f'{self._port}',
            database=f'{self._database}',
            user=f'{self._user}',
            password=f'{self._password}'
        )
        logger.debug(f'Connected successfully to database {self._database}')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._connection:
            self._connection.close()
            logger.debug(f'Connection to database {self._database} closed ')

    def remove_contact(self, user_id, contact_id):
        try:
            with closing(self._connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:
                schema = os.environ['PGSCHEMA']
                cursor.execute(
                    f'DELETE FROM "{schema}"."contact"'
                    'WHERE "user_id"=%s AND "id"=%s AND '
                    f'NOT EXISTS (SELECT 1 FROM "{schema}"."borrowing" WHERE'
                    '"user_id"=%s AND "contact_id"=%s)',
                    [user_id, contact_id, user_id, contact_id])
                self._connection.commit()
                return cursor.rowcount >= 1
        except psycopg2.Error as e:
            logger.error(f"delete contact error: {e}")
            raise e

    def list_contacts(self, user_id):
        try:
            with closing(self._connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:

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
            with closing(self._connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:
                schema = os.environ['PGSCHEMA']
                nickname = get_attribute(contact, 'nickname', '')
                thumbnail = get_attribute(contact, 'thumbnail', None)
                cursor.execute(
                    f'INSERT INTO "{schema}"."contact"(id, user_id, nickname, thumbnail) VALUES ( %s, %s, %s, %s);',
                    (id, user_id, nickname, thumbnail))
                self._connection.commit()
        except psycopg2.Error as e:
            logger.error(f"save contacts error: {e}")
            raise e

    def modify_contact(self, user_id, contact):
        try:
            with closing(self._connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:
                schema = os.environ['PGSCHEMA']
                id = contact['id']
                nickname = get_attribute(contact, 'nickname', '')
                thumbnail = get_attribute(contact, 'thumbnail', None)
                cursor.execute(
                    f'UPDATE "{schema}"."contact" '
                    'SET "nickname"=%s, "thumbnail"=%s WHERE "id" = %s AND "user_id"=%s ;',
                    (nickname, thumbnail, id, user_id))
                self._connection.commit()
        except psycopg2.Error as e:
            logger.error(f"modify contact error: {e}")
            raise e

    def get_contact(self, user_id, contact_id):
        try:
            with closing(self._connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:
                schema = os.environ['PGSCHEMA']
                cursor.execute(f'SELECT "id", "nickname", "thumbnail" FROM "{schema}"."contact"'
                               'WHERE "id"= %s AND "user_id"= %s', (contact_id, user_id))
                record = cursor.fetchone()
                if record is None:
                    return None
                else:
                    return {
                        'id': record.id,
                        'nickname': record.nickname,
                        'thumbnail': record.thumbnail
                    }
        except psycopg2.Error as e:
            logger.error(f"get contact error: {e}")
            raise e

#    def get_borrowings(self, user_id, contact):
#        try:
#            with closing(self._connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:
#                schema = os.environ['PGSCHEMA']
#                cursor.execute(f'SELECT * FROM "{schema}"."borrowing"'
#                               'WHERE "contact_id"= %s AND "user_id"= %s', (contact_id, user_id))
#                record = cursor.fetchone()
#        except psycopg2.Error as e:
#            logger.error(f"get borrowings error: {e}")
#            raise e

    def save_borrowing(self, user_id, contact_id, book_id, lending_id):
        try:
            with closing(self._connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:
                schema = os.environ['PGSCHEMA']
                cursor.execute(
                    f'INSERT INTO "{schema}"."borrowing" (user_id, lending_id, contact_id, book_id) VALUES ( %s, %s, %s, %s);',
                    (user_id, lending_id, contact_id, book_id))
                self._connection.commit()
        except psycopg2.Error as e:
            logger.error(f"save borrowing error: {e}")
            raise e

    def remove_borrowing(self, user_id, contact_id, book_id, lending_id):
        try:
            with closing(self._connection.cursor(cursor_factory=NamedTupleCursor)) as cursor:
                schema = os.environ['PGSCHEMA']
                cursor.execute(
                    f'DELETE FROM "{schema}"."borrowing" WHERE user_id=%s AND lending_id=%s AND contact_id=%s AND book_id=%s;',
                    (user_id, lending_id, contact_id, book_id))
                self._connection.commit()
        except psycopg2.Error as e:
            logger.error(f"save borrowing error: {e}")
            raise e


def get_storage():
    return DatabaseStorage()
