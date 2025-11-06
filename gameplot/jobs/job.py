from gameplot.validatable import Validatable
from gameplot.db import get_db
from gameplot.queries import *
from typing import NamedTuple
import logging
from datetime import datetime
from dataclasses import dataclass

def download_game_title():
    pass

@dataclass
class Job(Validatable):
    id: int
    payload: str
    status: str
    worker_id: str
    insert_ts: datetime
    pickup_ts: datetime
    completion_ts: datetime
    result: str

    @classmethod
    def from_namedtuple(cls, other: NamedTuple | None):
        if other is not None: return cls(**other._asdict()) 

    @classmethod
    def get(cls, id: int) -> Job | None:
        """Constructor: Returns a Job corresponding with the given ID, if it exists."""
        with get_db() as db:
            cur = db.execute(Q(I.GET_JOB_BY_ID, id))
            return cls.from_namedtuple(cur.fetchone())

    @classmethod
    def get_pending(cls) -> Job | None: 
        """Constructor: Returns the next job to execute."""
        with get_db() as db:
            q = Q(I.GET_NEXT_JOB)
            cur = db.execute(q)
            return cls.from_namedtuple(cur.fetchone())
        
    @classmethod
    def get_claimed(cls, worker_id: str) -> Job | None:
        """Constructor: gets a previously claimed job"""
        with get_db() as db:
            q = Q(I.GET_CLAIMED_JOB, worker_id)
            cur = db.execute(q)
            return cls.from_namedtuple(cur.fetchone())

    @classmethod
    def try_claim(cls, worker_id: str) -> Job | None: 
        """Constructor: Tries to claim the next pending job, updating its status. Returns if successful."""
        with get_db() as db:
            q = Q(I.TRY_CLAIM_NEXT_JOB, worker_id)
            cur = db.execute(q)
            return cls.from_namedtuple(cur.fetchone())
        
    @classmethod
    def post_result(cls, job_id: int, worker_id: str, result: str) -> Job | None:
        """Constructor: Posts the result from having completed a job, updating its status. Returns if successful."""
        with get_db() as db:
            q = Q(I.FINISH_JOB, job_id, worker_id, 'done', result)
            cur = db.execute(q)
            return cls.from_namedtuple(cur.fetchone())
    
    @classmethod
    def post_error(cls, job_id: int, worker_id: str, err: str) -> Job | None:
        """Constructor: Posts the result from having errored out a job, updating its status. Returns if successful."""
        with get_db() as db:
            q = Q(I.FINISH_JOB, job_id, worker_id, 'errored', err)
            cur = db.execute(q)
            return cls.from_namedtuple(cur.fetchone())

    def kickoff(self):
        """Executes a job based on its payload.
        Payload should have 3 keys: function, kwargs, and args."""

        match self.payload:
            case "download":
                download_game_title()
            case _:
                logging.info("Got bad payload %s", self.payload)


