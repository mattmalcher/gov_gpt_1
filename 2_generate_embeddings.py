import logging
import logging.config

from govgpt.text_loader import PGLoader
from govgpt.embeddings import embeddings
from govgpt.db import conn_string

from transformers import AutoTokenizer
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.pgvector import PGVector

logging.config.fileConfig('logging_config.ini', disable_existing_loggers=True)
logger = logging.getLogger()

logger.debug("loading tokenizer")
tokenizer = AutoTokenizer.from_pretrained("models/multi-qa-MiniLM-L6-cos-v1/")
logger.debug("tokenizer loaded")

logger.debug("initialising PGLoader")
conn_string = "postgresql://" + conn_string

# with open("sql/pages_wo_embeddings.pgsql") as queryfile:
#     statement = queryfile.read()
    
with open("sql/pages_unique_content.pgsql") as queryfile:
    statement = queryfile.read()
    #statement = statement + "LIMIT 100"

loader = PGLoader( 
    query = statement, 
    database = conn_string,
    page_content_columns = ["content"],
    metadata_columns = ["link", "format", "updated_at", "public_timestamp"],
    rename_dict = {"link":"source"}
)

logger.debug("loading documents")
docs = loader.load()

logger.debug("loading splitter")
text_splitter = CharacterTextSplitter.from_huggingface_tokenizer(
    tokenizer, 
    chunk_size=200, 
    chunk_overlap=20,
    )

logger.debug("splitting documents")
texts = text_splitter.split_documents(docs)

# https://github.com/hwchase17/langchain/issues/2219
# edit $(virtualenv location)/lib/$(python version)/site-packages/langchain/vectorstores/pgvector.py
# change L22 to: ADA_TOKEN_COUNT = 384

# To fix the already created tables
# docker exec -it $(pg container id) sh
# psql --username embed_usr --dbname embed_db
# alter table embed_schema.langchain_pg_embedding alter column embedding type vector(384);

logger.debug("generating embeddings")
db = PGVector.from_documents(
    embedding=embeddings,
    documents=texts,
    collection_name = "sample_1",
    connection_string = conn_string,
    #pre_delete_collection=True
)

"done"