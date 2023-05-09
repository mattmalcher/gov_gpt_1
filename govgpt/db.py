"""
Things I think I want to store in this database

1. Pages - This is data about pages

2. Chunks & Embeddings - I think our embeddings will be at a sub-page level, so we will want a table of these chunks of text.

"""
import logging
logger = logging.getLogger(__name__)

from sqlalchemy import create_engine, text

from sqlalchemy import String, BigInteger, DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from pgvector.sqlalchemy import Vector


engine = create_engine('postgresql+psycopg2://embed_usr:ilovellms@127.0.0.1:54322/embed_db')

connection = engine.connect()

class Base(DeclarativeBase):
    pass


class Page(Base):
    """Pages
    
    """
    __tablename__ = "pages"
    __table_args__ = {"schema": "embed_schema"}

    link: Mapped[str] = mapped_column(String(), primary_key=True)
    format: Mapped[str] = mapped_column(String())
    content: Mapped[str] = mapped_column(String())
    updated_at: Mapped[str] = mapped_column(DateTime())
    public_timestamp: Mapped[str] = mapped_column(DateTime())
   

    def __repr__(self) -> str:
        return f"""Page(
            link={self.link!r}, 
            format={self.format!r},
            content={self.content[0:30]!r},
            updated_at={self.updated_at!r},
            
        )
        """

class Embedding(Base):
    """Embeddings

    """

    __tablename__ = "embeddings"
    __table_args__ = {"schema": "embed_schema"}

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    text_chunk: Mapped[str] = mapped_column(String()) 
    embedding: Mapped[str] = mapped_column(Vector(385))
    link: Mapped[str] = mapped_column(ForeignKey("embed_schema.pages.link"))
    
    ## TODO
    # possibly in future for efficiency we want to just store 
    # the position of the text in the linked content, but for 
    # now this is probably good for debugging.

    def __repr__(self) -> str:
        return f"""Embedding(
            link={self.link!r}, 
            text_chunk={self.text_chunk[0:30]!r},
            embedding={self.embedding[0:10]!r}           
        )
        """
