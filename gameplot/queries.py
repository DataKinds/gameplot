from enum import Enum, auto
from typing import Callable, Any, TYPE_CHECKING, cast, LiteralString
from psycopg.sql import SQL, Composed

class I(Enum):
    """The Index of which queries exist"""
    # Job related queries
    GET_JOB_BY_ID       = auto()
    GET_NEXT_JOB        = auto()
    TRY_CLAIM_NEXT_JOB  = auto()
    GET_CLAIMED_JOB     = auto()
    FINISH_JOB          = auto()

_Q: dict[I, str] = {}
_Q[I.GET_JOB_BY_ID] = "SELECT * FROM jobs WHERE id = {}"

_Q[I.GET_NEXT_JOB] = """
SELECT *
FROM jobs
WHERE status = 'pending'
ORDER BY insert_ts
FOR NO KEY UPDATE
LIMIT 1"""

_Q[I.TRY_CLAIM_NEXT_JOB] = """
UPDATE jobs 
SET status = 'active', worker_id = {}, pickup_ts = NOW()
WHERE id = (
    SELECT id
    FROM jobs
    WHERE status = 'pending'
    ORDER BY insert_ts
    FOR NO KEY UPDATE
    LIMIT 1)
RETURNING jobs.*"""

_Q[I.GET_CLAIMED_JOB] = """
SELECT * from jobs
WHERE status = 'active' AND worker_id = {}
LIMIT 1
"""

_Q[I.FINISH_JOB] = """
UPDATE jobs 
SET status = {2}, completion_ts = NOW(), result = {3}
WHERE id = (
    SELECT id
    FROM jobs
    WHERE id = {0} AND status = 'active' AND worker_id = {1}
    ORDER BY insert_ts
    FOR NO KEY UPDATE
    LIMIT 1)
RETURNING jobs.*"""

def Q(selection: I, *args) -> Composed:
    return SQL(_Q[selection]).format(*args)
