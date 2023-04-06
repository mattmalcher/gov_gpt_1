import requests


def search_gov_uk_with_content(query):
    """
    Perform a search on the Gov.UK website using the specified query, and retrieve the content of each search result using the content API.

    Parameters
    ----------
    query : str
        The search query to use.

    Returns
    -------
    list of strings
        A list of strings with the indexable content of each search result.

    Raises
    ------
    None

    """
    search_url = "https://www.gov.uk/api/search.json"

    params = {
        "q": query,
         "fields": "indexable_content"
         } 

    response = requests.get(search_url, params=params)
    print(response.request.url)
    if response.status_code == 200:
        results = response.json()["results"]
        content = []

        for r in results:

            try:
                content.append(r["indexable_content"])
            except:
                continue

        return content
    else:
        return None
        
