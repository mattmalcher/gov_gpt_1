# We want a loader to grab our documents out of postgres
# example 1 - https://github.com/hwchase17/langchain/blob/master/langchain/document_loaders/bigquery.py
# example 2 - https://github.com/hwchase17/langchain/blob/master/langchain/document_loaders/duckdb_loader.py

# could keep using sqlalchemy as have been so far, or just just
# the key db library (psycopg2) as per the example loaders and 
# contribute this loader back to langchain?

# https://www.psycopg.org/docs/module.html

from datetime import datetime
from typing import Dict, List, Optional

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader


class PGLoader(BaseLoader):
    """Loads a query result from DuckDB into a list of documents.

    Each document represents one row of the result. The `page_content_columns`
    are written into the `page_content` of the document. The `metadata_columns`
    are written into the `metadata` of the document. By default, all columns
    are written into the `page_content` and none into the `metadata`.
    """

    def __init__(
        self,
        query: str,
        database: str,
        page_content_columns: Optional[List[str]] = None,
        metadata_columns: Optional[List[str]] = None,       
        rename_dict: Optional[Dict] = None
    ):
        """_summary_

        Args:
            query (str): A query to be run to return document rows.
            database (str): A connection string
            page_content_columns (Optional[List[str]], optional): _description_. Defaults to None.
            metadata_columns (Optional[List[str]], optional): _description_. Defaults to None.
            rename_dict Optional[Dict] = None: A dictionary of {'newname':'oldname'} to rename metadata keys. 
                Useful if for example you want to rename an item of metadata to a special name picked up 
                by langchain like 'source'
        """
        self.query = query
        self.database = database
        self.page_content_columns = page_content_columns
        self.metadata_columns = metadata_columns
        self.rename_dict = rename_dict
    
    def load(self) -> List[Document]:
        try:
            import psycopg2
        except ImportError:
            raise ValueError(
                "Could not import psycopg2 python package. "
                "Please install it with `pip install psycopg2`."
            )

        docs: List[Document] = []

        # Note, this method of passing a URI to connect to PG is only 
        # supported with newer versions of libpq with PG 9.2+. Could make this more 
        # robust by parsing the URI and then passing the components as named args?
        with psycopg2.connect(self.database) as con:

            cur = con.cursor()

            cur.execute(self.query)
            results = cur.fetchall()

            colnames = [desc[0] for desc in cur.description]
            
            if self.page_content_columns is None:
                page_content_columns = colnames
            else:
                page_content_columns = self.page_content_columns

            if self.metadata_columns is None:
                metadata_columns = []
            else:
                metadata_columns = self.metadata_columns

            for result in results:
                page_content = "\n".join(
                    f"{column}: {result[colnames.index(column)]}"
                    for column in page_content_columns
                )

                metadata = {
                    column: serialize_fix(result[colnames.index(column)])
                    for column in metadata_columns
                }

                if self.rename_dict:
                    metadata = {self.rename_dict.get(k, k): v for k, v in metadata.items()}

                doc = Document(page_content=page_content, metadata=metadata)
                docs.append(doc)

        return docs
    
def serialize_fix(obj):
    """ 
    Quick and dirty fix for modifying the format of 
    metadata that otherwise wont serialize nicely with json.dumps
    """

    if isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj