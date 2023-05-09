import logging
logger = logging.getLogger(__name__)

import nltk
from nltk.corpus import stopwords

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
     nltk.download('corpora/stopwords')

stopwords_list = stopwords.words('english')


def clean_response(text):
    cleantext = ' '.join([word for word in text.split() if word not in stopwords_list])

    return cleantext