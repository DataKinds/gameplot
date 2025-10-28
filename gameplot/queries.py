from enum import Enum, auto
from typing import Callable, Any, TYPE_CHECKING, cast, LiteralString
from psycopg.sql import SQL, Composed

class I(Enum):
    """The Index of which queries exist"""
    GET_JOB_BY_ID = auto()
    GET_NEXT_JOB = auto()

_Q: dict[I, str] = {}
_Q[I.GET_JOB_BY_ID] = "SELECT * FROM jobs WHERE id = {}"
_Q[I.GET_NEXT_JOB] = """
SELECT * 
FROM jobs
WHERE status = 'pending'
ORDER BY insert_ts
LIMIT 1
"""

Q: dict[I, Callable[..., SQL | Composed]] = {} # All of the SQL queries that power Gameplot.
for i, q in _Q.items():
   Q[i] = lambda *args: SQL(cast(LiteralString,q)).format(args)
