import logging
logger = logging.getLogger(__name__)

from datetime import datetime
from time import sleep 
import copy

from requests import HTTPError, Session, Request
from requests.adapters import HTTPAdapter, Retry

# Lots of scope to improve how we manage getting the XML - with timeouts and backoff
# # https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/

s = Session()
retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])

s.mount('https://', HTTPAdapter(max_retries=retries))

search_url = "https://www.gov.uk/api/search.json"
        
def build_search(
        query = None, 
        fields = [
            "link",
            "content_store_document_type",
            "indexable_content"            
        ], 
        filters = {"any_organisations":"hm-revenue-customs"}, 
        **kwargs
        ) -> Request:
    """Build gov.uk search API request.

    Args:
        query (str, optional): a query. Defaults to None.
        fields (list, optional): fields to return. Defaults to [ "link", "content_store_document_type", "indexable_content" ].
        filters (dict, optional): _description_. Defaults to {"any_organisations":"hm-revenue-customs"}.
        **kwargs: any additional parameters

    Returns:
        Request: a requests Request object, which can be prepared & sent.
    """
    params = {**kwargs}

    if query:
        params.update({"q": query})

    # https://docs.publishing.service.gov.uk/repos/search-api/using-the-search-api.html#returning-specific-document-fields
    if fields:
        params.update({"fields": fields})
    
    # https://docs.publishing.service.gov.uk/repos/search-api/using-the-search-api.html#using-faceted-search-parameters
    if filters:
        params.update({"filter_"+ k : v for (k, v) in filters.items() } )

    return Request(method = 'GET', url = search_url, params = params)

    
def add_page_params(req:Request, start:int = 0, count:int = 50, order:str = None) -> Request:
    """Add pagination parameters to an existing request.

    Args:
        req (Request): a requests Request object, which can be prepared & sent.
        start (int, optional): Position in search result list to start returning results (0-based) If the start offset is greater than the number of matching results, no results will be returned (but also no error will be returned). Defaults to 0.
        count (int, optional): Maximum number of search results to return. If insufficient documents match, as many as possible are returned (subject to the supplied start offset). This may be set to 0 to return no results (which may be useful if only, say, facet values are wanted). Setting this to 0 will reduce processing time. Defaults to 50.
        order (str, optional): The sort order. A field name, with an optional preceding "-" to sort in descending order. If not specified, sort order is relevance. Only some fields can be sorted on - an HTTP 422 error will be returned if the requested field is not a valid sort field. Defaults to None.

    Returns:
        Request: a requests Request object, with added pagination parameters, which can be prepared & sent.
    """
    
    params = copy.copy(req.params)

    new_params = {"start" :start, "count":count, "order": order}

    new_params = {k:v for (k,v) in new_params.items() if v is not None}

    params.update(new_params)

    return Request(method = 'GET', url = search_url, params = params)


def execute_search(req:Request):
    """Executes a request prepared with search_build / paginate.

    Following pattern from: https://requests.readthedocs.io/en/latest/user/advanced/#prepared-requests

    Args:
        req (Request): _description_

    Raises:
        SystemExit: _description_

    Returns:
        _type_: _description_
    """

    prepped =  s.prepare_request(req)

    try:
        resp = s.send(prepped)

    # if we got an invalid HTTP response
    except HTTPError as err:
        raise SystemExit(f"{err.response.reason}: {req.url}")

  
    return resp.json()


def page_query(chunk_size = 100, date_filt:datetime = None, rps = 1, limit = 1000):

    pause_time = 1/rps
    
    filter_dict = {
        "any_organisations":"hm-revenue-customs"
        }
    
    if date_filt:
        filter_dict.update({"updated_at" : f"from:{ date_filt.date() }"})

    initial_query = add_page_params(
        req = build_search(query = None, fields = None, filters = filter_dict),
        start = 0,  
        count = 0,  
        order= None
    )

    total = execute_search(initial_query)["total"]

    query = build_search(
            query = None, 
            fields = [
            "link",
            "format",
            "indexable_content",
            "updated_at",
            "public_timestamp"
            ],
            filters= filter_dict
            )

    results = []

    for i in range(0, total, chunk_size):

        if i > limit:
            return results
        
        range_query = add_page_params(req = query, start = i, count = chunk_size )
        
        logger.debug(f"retrieving results page, {i} / {total}")
        res = execute_search(range_query)

        results.extend(res['results'])

        sleep(pause_time)

    return results

def chunks(list:list, n:int = 10):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(list), n):
        yield list[i:i + n]