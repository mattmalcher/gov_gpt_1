import logging
import logging.config

from time import sleep 
from datetime import datetime
 
from govgpt import gov_search
from govgpt import db

from sqlalchemy import select, func
from sqlalchemy.orm import Session


logging.config.fileConfig('logging_config.ini', disable_existing_loggers=True)
logger = logging.getLogger()

if __name__ == "__main__":
    db.Base.metadata.create_all(bind=db.engine)
    logger.debug("Initialized the db")


# https://docs.sqlalchemy.org/en/20/orm/queryguide/api.html#fetching-large-result-sets-with-yield-per
# https://docs.sqlalchemy.org/en/20/core/connections.html#engine-stream-results
with Session( db.engine) as session:

    "do stuff"

