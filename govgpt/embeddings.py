import logging
logger = logging.getLogger(__name__)

from sentence_transformers import SentenceTransformer, util

logger.debug("loading model")
model = SentenceTransformer('models/multi-qa-MiniLM-L6-cos-v1/')
logger.debug("model loaded")

query_embedding = model.encode('How big is London')
passage_embedding = model.encode(['London has 9,787,426 inhabitants at the 2011 census',
                                  'London is known for its finacial district'])

print("Similarity:", util.dot_score(query_embedding, passage_embedding))