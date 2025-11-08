import logging
from typing import Any, NamedTuple

from gameplot.db import get_db
from gameplot.queries import *
from gameplot.validatable import Validatable

from . import router

logger = logging.getLogger(__name__)

import json
import traceback
from dataclasses import dataclass
from datetime import datetime


def download_game_title():
    pass

@dataclass
class Job(Validatable):
    id: int
    payload: Any
    status: str
    worker_id: str
    insert_ts: datetime
    pickup_ts: datetime
    completion_ts: datetime
    result: Any

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

    @classmethod
    def enqueue(cls, job_name: str, *job_args) -> Job:
        """Constructor: Adds a job to the job queue."""
        with get_db() as db:
            payload = json.dumps({'name': job_name, 'args': job_args})
            q = Q(I.POST_NEW_JOB, payload)
            cur = db.execute(q)
            return cls.from_namedtuple(cur.fetchone())

    def route(self) -> Job | None:
        """Routes and executes a job based on its payload. Payload should have 2 keys: name and args.
        Returns the updated job if we executed."""
        assert self.status == 'active', """If you're executing a job, it should be an active one. You can try calling something like Job.try_claim(id).route(id)."""
        if 'name' not in self.payload or 'args' not in self.payload:
            logger.error("Got a malformed payload from a job: %s", self.payload)
        try:
            result = router.route_job(self.payload['name'], self.payload['args'])
            return self.post_result(self.id, self.worker_id, json.dumps(result))
        except Exception as e:
            tb = traceback.format_exc()
            logger.error("Got a failure from a job! It looks like this: %s", tb)
            return self.post_error(self.id, self.worker_id, json.dumps(tb))
