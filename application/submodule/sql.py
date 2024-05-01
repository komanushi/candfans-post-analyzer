from collections import namedtuple
from typing import TypeVar, Callable

import psycopg

from django.db import connection
from pydantic import BaseModel

T = TypeVar('T')


class QueryModel(BaseModel):
    query: str
    row_to_model: Callable[[namedtuple], T]


async def get_query_result(query: str, params: list = None) -> list[namedtuple]:
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
                results.append(nt_result(*row))
            return results


async def get_query_results_via_model(sql_model: QueryModel, params: list) -> list[T]:
    results = await get_query_result(sql_model.query, params)
    return [sql_model.row_to_model(row) for row in results]
