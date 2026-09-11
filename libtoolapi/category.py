import requests
import logging
import json
logger = logging.getLogger(__name__)


def read_category(id: int):
    try:
        category_id = str(id)
        #print(type(id)) # debug

        # creating request:
        url = "http://127.0.0.1:8001/LibraryTools/v1/categories/"
        endpoint = url + category_id

        # Send request
        response = requests.get(endpoint)

        if response.status_code == 404:
            raise ValueError("qualcosa è andato storto")
    
    except Exception as e:
        logger.error(f"error: {e}", exc_info=True)
        raise Exception("errore generico")
    return response

def read_all_categories():
    try:
        # creating request
        url = "http://127.0.0.1:8001/LibraryTools/v1/categories/"

        # Send request
        response = requests.get(url)
        if response.status_code == 404:
            raise Exception(f"Nothing found here")
        
    except Exception as e:
        logger.error(f"error: {e}", exc_info=True)
        raise Exception("Internal server error")
    return response
    

# leggi = read_category(1)
# print(leggi.content)

# leggi_tutto = read_all_categories()
# print(leggi_tutto.content)

