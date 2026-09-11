import requests
import logging
logger = logging.getLogger(__name__)


def read_tag(id: int):
    try:
        tag_id = str(id)
        #print(type(id)) # debug

        # creating request:
        url = "http://127.0.0.1:8001/LibraryTools/v1/tags/"
        endpoint = url + tag_id

        # Send request
        response = requests.get(endpoint)
        if response.status_code == 404:
            raise ValueError("qualcosa è andato storto")
    
    except Exception as e:
        logger.error(f"error: {e}", exc_info=True)
        raise Exception("errore generico")
    return response

def read_all_tags():
    try:
        # creating request
        url = "http://127.0.0.1:8001/LibraryTools/v1/tags/"

        # Send request
        response = requests.get(url)
        if response.status_code == 404:
            raise NotFoundError(f"Nothing found here")
        
    except Exception as e:
        logger.error(f"error: {e}", exc_info=True)
        raise AppError("Internal server error")
    return response
    

leggi = read_tag(1)
print(leggi.content)

leggi_tutto = read_all_tags()
print(leggi_tutto.content)

