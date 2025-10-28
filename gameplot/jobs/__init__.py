from gameplot.validatable import Validatable
from gameplot.db import get_db
from gameplot.queries import *
from typing import cast
import logging
from datetime import datetime

def download_game_title():
    pass

class Job(Validatable):
    payload: str
    status: str
    insert_ts: datetime
    pickup_ts: datetime
    completion_ts: datetime
    result: str


    def __init__(self, id: int):
        """Constructor: Returns a Job corresponding with the given ID, if it exists."""
        db = get_db()
        cur = db.execute(GET_JOB_BY_ID)
        job = cur.fetchone()
        if job is None:
            raise ValueError(f"No job with ID {id}")
        for fieldname in job._fields:
            fieldname = cast(str, fieldname)
            setattr(self, fieldname, getattr(job, fieldname))

    def kickoff(self):
        """Executes a job based on its payload.
        Payload should have 3 keys: function, kwargs, and args."""

        match self.payload:
            case "download":
                download_game_title()
            case _:
                logging.info("Got bad payload %s", self.payload)


