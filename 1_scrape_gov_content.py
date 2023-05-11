import logging
import logging.config

from datetime import datetime

from time import sleep 
from datetime import datetime
 
from govgpt import gov_search
from govgpt import db

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert 


logging.config.fileConfig('logging_config.ini', disable_existing_loggers=True)
logger = logging.getLogger()

if __name__ == "__main__":
    db.Base.metadata.create_all(bind=db.engine)
    logger.debug("initialized the db")


# Check if we already have data, and if so, what the newest updated date is
with Session( db.engine) as session:

    newest_content = (
        select(func.max(db.Page.updated_at))
    )

    res = session.scalars(newest_content).one()

    if res:
        logger.info("existing data found")
        date_filt = res     
        logger.info(f"retrieve content updated since {date_filt}")
    else:
        logger.info("page table is empty")
        date_filt = None

# bypass update for now
#date_filt = None

all_results = gov_search.page_query(
    chunk_size = 200, 
    date_filt = date_filt, 
    limit = 100000
)

with Session( db.engine) as session:

    for chunk in gov_search.chunks(all_results, n = 100):
        logger.debug("processing new chunk")

        for result in chunk:

            #logger.debug("creating page object")

            newdata = dict(
                link = result["link"],
                format = result.get("format", ""),
                content = result.get("indexable_content", ""),
                updated_at = result.get(
                    "updated_at",
                    result.get("public_timestamp", datetime.now())
                ),
                public_timestamp = result["public_timestamp"]
            )

            insert_stmt = insert(db.Page.__table__).values(newdata)
 
            do_update_stmt = insert_stmt.on_conflict_do_update(
                constraint=f"{db.Page.__tablename__}_pkey",
                set_= newdata
            )

            session.execute(do_update_stmt)
        
        logger.debug(f"comitting to db")
        session.commit()

"done"