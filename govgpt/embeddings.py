# https://python.langchain.com/en/latest/modules/models/text_embedding/examples/sentence_transformers.html

import logging
logger = logging.getLogger(__name__)

from langchain.embeddings import HuggingFaceEmbeddings

logger.debug("loading model")
embeddings = HuggingFaceEmbeddings(model_name="models/multi-qa-MiniLM-L6-cos-v1/")
logger.debug("model loaded")
