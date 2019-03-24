import json
import os
import psycopg2


def make_mock_event(subject, body=None, path_parameters=None):
    mock_event = {
        'requestContext': {
            'authorizer': {
                'claims': {
                    'sub': subject
                }
            }
        },
        'body': json.dumps(body),
        'pathParameters': path_parameters
    }

    return mock_event


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

    return connection
