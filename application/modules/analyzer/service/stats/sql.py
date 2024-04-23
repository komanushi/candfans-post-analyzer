from collections import namedtuple

import psycopg

from django.db import connection


def namedtuple_fetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


async def get_query_result(query: str, params: list = None) -> list:
    aconnection = await psycopg.AsyncConnection.connect(
        **{
            **connection.get_connection_params(),
            "cursor_factory": psycopg.AsyncCursor,
        },
    )

    async with aconnection:
        async with aconnection.cursor() as cursor:
            await cursor.execute(
                query.encode('utf-8'),
                params
            )
            desc = cursor.description
            nt_result = namedtuple('Result', [col[0] for col in desc])
            results = []
            async for row in cursor:
                nt_result(*row)
                results.append(nt_result)
            return results
