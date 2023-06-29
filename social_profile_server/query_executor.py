# Copyright (c) 2022 Lightricks. All rights reserved.
from typing import Any, List, Optional

import psycopg2
from psycopg2.extras import RealDictCursor

CONNECTION_KWARGS = {
    "database": "postgres",
    "user": "omri",
    "password": "1234",
    "host": "postgres",
    "port": "5432",
    "cursor_factory": RealDictCursor,
    "connect_timeout": 5,
}


def execute_query(query: str) -> Optional[List[Any]]:
    with psycopg2.connect(**CONNECTION_KWARGS) as connection:
        connection.set_session(autocommit=True)
        with connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchall()


def execute_update(query: str) -> None:
    with psycopg2.connect(**CONNECTION_KWARGS) as connection:
        connection.set_session(autocommit=True)
        with connection.cursor() as cursor:
            cursor.execute(query)
