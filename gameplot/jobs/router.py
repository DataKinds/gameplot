import logging
from typing import Any, List

logger = logging.getLogger(__name__)

def route_job(job_name: str, job_args: List[Any]) -> Any:
    """Executes a job, given a name and a list of arguments. Returns whatever the job returned."""
    match job_name:
        case "test":
            logger.warning("RUNNIN' THE TEST!")
            return "69"
        case "download_steam":
            logger.info("Downloading metadata from Steam...")
        case "download_itch":
            logger.info("Downloading metadata from Itch...")

        case _:
            err = "Got unexpected job name '%s'" % job_name
            logger.warning(err)
            raise ValueError(err)
