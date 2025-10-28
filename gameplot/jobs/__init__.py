from gameplot.validatable import Validatable
from gameplot.db import get_db
from gameplot.queries import *
from typing import cast, TYPE_CHECKING, NamedTuple, Optional
if TYPE_CHECKING:
    from collections import namedtuple
import logging
from datetime import datetime
from dataclasses import dataclass

def download_game_title():
    pass

@dataclass
class Job(Validatable):
    payload: str
    status: str
    insert_ts: datetime
    pickup_ts: datetime
    completion_ts: datetime
    result: str

    @classmethod
    def get(cls, id: int):
        """Constructor: Returns a Job corresponding with the given ID, if it exists."""
        db = get_db()
        cur = db.execute(Q[I.GET_JOB_BY_ID](id))
        job = cast(Optional[NamedTuple], cur.fetchone())
        if job is not None:
            return cls(**job._asdict())

    @classmethod
    def get_pending(cls): 
        """Constructor: Returns the next job to execute."""
        db = get_db()
        cur = db.execute(Q[I.GET_NEXT_JOB]())
        job = cast(Optional[NamedTuple], cur.fetchone())
        if job is not None:
            return cls(**job._asdict())

    def kickoff(self):
        """Executes a job based on its payload.
        Payload should have 3 keys: function, kwargs, and args."""

        match self.payload:
            case "download":
                download_game_title()
            case _:
                logging.info("Got bad payload %s", self.payload)


