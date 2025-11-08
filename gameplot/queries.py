import logging
from enum import Enum, auto
from typing import TYPE_CHECKING, Any, Callable, LiteralString, cast

from psycopg.sql import SQL, Composed

logger = logging.getLogger(__name__)

class I(Enum):
    """The Index of which queries exist"""
    # Job related queries
    GET_JOB_BY_ID       = auto()
    GET_NEXT_JOB        = auto()
    TRY_CLAIM_NEXT_JOB  = auto()
    GET_CLAIMED_JOB     = auto()
    POST_NEW_JOB        = auto()
    FINISH_JOB          = auto()
    # User session queries
    GET_USER_FROM_TOKEN = auto()
    CHECK_TOKEN = auto()
    NEW_TOKEN = auto()
    PRUNE_TOKENS = auto()
    # User queries
    NEW_USER = auto()
    GET_USER = auto()

_Q: dict[I, str] = {}
_Q[I.GET_JOB_BY_ID] = "SELECT * FROM jobs WHERE id = {}"

_Q[I.GET_NEXT_JOB] = """
SELECT *
FROM jobs
WHERE status = 'pending'
ORDER BY insert_ts
FOR NO KEY UPDATE
LIMIT 1
"""

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
RETURNING jobs.*
"""

_Q[I.GET_CLAIMED_JOB] = """
SELECT * from jobs
WHERE status = 'active' AND worker_id = {}
LIMIT 1
"""

_Q[I.POST_NEW_JOB] = """
INSERT INTO jobs (payload, status, insert_ts) VALUES ({}, 'pending', NOW())
RETURNING *
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
RETURNING jobs.*
"""

_Q[I.GET_USER_FROM_TOKEN] = """
SELECT * FROM users 
JOIN user_sessions ON user_id = id
WHERE session_id = {} AND expires_on > NOW()
LIMIT 1
"""

# Arguments: session ID to check, and the amount of time to bump the queried token's validity forward
_Q[I.CHECK_TOKEN] = """
WITH active_user AS (
    SELECT * FROM users 
    JOIN user_sessions ON user_id = id
    WHERE session_id = {} AND expires_on > NOW()
    LIMIT 1
)
UPDATE user_sessions SET expires_on = NOW() + {}
FROM active_user
WHERE active_user.session_id = user_sessions.session_id
RETURNING active_user.*
"""

# TODO: this should be scheduled every so often
_Q[I.PRUNE_TOKENS] = """
DELETE FROM user_sessions WHERE expires_on < NOW()
"""

_Q[I.NEW_TOKEN] = """
INSERT INTO user_sessions (session_id, user_id, expires_on) VALUES (uuidv4(), {}, NOW() + {})
RETURNING session_id
"""

_Q[I.GET_USER] = """
SELECT * FROM users WHERE email = {}
"""

_Q[I.NEW_USER] = """
INSERT INTO users (email, password) VALUES ({}, {}) RETURNING *
"""

def Q(selection: I, *args) -> Composed:
    logger.debug(f"Query handler produced: {SQL(_Q[selection]).format(*args)}")
    return SQL(_Q[selection]).format(*args)
